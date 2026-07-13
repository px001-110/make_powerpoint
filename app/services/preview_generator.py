import os
import shutil
import subprocess
from pathlib import Path
from pdf2image import convert_from_path


class PreviewGenerator:
    def __init__(self, libreoffice_path="soffice", dpi=160):

        self.libreoffice_path = libreoffice_path
        self.dpi = dpi

    def generate(self, pptx_path, output_dir):
        pptx_path = Path(pptx_path)
        output_dir = Path(output_dir)

        if output_dir.exists():
            shutil.rmtree(output_dir)
        
        output_dir.mkdir(parents=True)

        pdf_path = self._pptx_to_pdf(pptx_path)

        images = self._pdf_to_png(pdf_path, output_dir)

        return images
    
    def _pptx_to_pdf(self, pptx_path):

        pdf_dir = pptx_path.parent

        subprocess.run(
            [
                self.libreoffice_path,
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                str(pdf_dir),
                str(pptx_path)
                ],
            check=True,
        )

        pdf_path = pdf_dir / (pptx_path.stem + ".pdf")

        if not pdf_path.exists():
            raise FileNotFoundError("PDFへの変換に失敗しました。")
        
        return pdf_path
    
    def _pdf_to_png(self, pdf_path, output_dir):

        pages = convert_from_path(pdf_path, dpi=self.dpi)

        image_names = []

        for i, page in enumerate(pages):

            filename = f"slide_{i+1:03d}.png"

            path = output_dir / filename

            page.save(path, "PNG")

            image_names.append(filename)

        return image_names
    
