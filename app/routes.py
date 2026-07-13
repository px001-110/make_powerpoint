from flask import (
    Blueprint,
    render_template,
    request,
    send_file,
    current_app,
    session
)
from pptx import Presentation
from urllib.parse import quote
from pathlib import Path
from datetime import datetime
import re

from .services.generator import make_powerpoint
from .services.file_service import (
    save_upload_file,
    cleanup_old_files
)

from .services.preview_generator import PreviewGenerator
from .services.find_soffice import find_soffice

main = Blueprint("main", __name__)


@main.before_app_request
def auto_cleanup():
    cleanup_old_files()


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/upload", methods=["POST"])
def upload():

    upload_files = request.files.getlist("files")

    output_name = request.form.get("output_name", "").strip()

    if not output_name:
        today = datetime.now().strftime("%Y-%m-%d")
        output_name = f"{today}-自動生成"

    output_name = re.sub(r'[\\/*?:"<>|]', "", output_name)

    if not output_name:
        output_name = "自動生成"

    BASE_DIR = Path(__file__).resolve().parent.parent

    template_path = ( BASE_DIR / "app" / "templates" / "template.pptx")
    print(template_path.exists())
    print(template_path)

    prs = Presentation(str(template_path))

    for file in upload_files:

        save_path = save_upload_file(
            file,
            current_app.config["UPLOAD_DIR"]
        )

        try:
            make_powerpoint(
                str(save_path),
                prs
            )

        except Exception as e:
            current_app.logger.error(
                f"PowerPoint生成エラー: {e}"
            )

    output_path = (
        current_app.config["OUTPUT_DIR"]
        / f"{output_name}.pptx"
    )

    output_path = output_path.resolve()

    prs.save(output_path)

    session["ppt_path"] = str(output_path)
    session["download_name"] = f"{output_name}.pptx"

    preview = PreviewGenerator(
        libreoffice_path=find_soffice()
    )

    preview_dir = current_app.static_folder / Path("previews") / "session123"

    images = preview.generate(
        output_path,
        preview_dir
    )
    print(images)

    return render_template(
        "preview.html",
        images=images,
        preview_dir="previews/session123",
    )

@main.route("/download")
def download():
    ppt_path = session.get("ppt_path")
    
    if not ppt_path:
        return "PowerPointファイルが見つかりません。", 404
    
    download_name = session.get("download_name", "自動生成.pptx")

    return send_file(
        ppt_path,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )