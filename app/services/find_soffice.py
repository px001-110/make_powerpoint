import platform
import shutil
import os

def find_soffice():
    # PATHの登録されている場合（Linux/Renderなど）
    soffice = shutil.which("soffice")
    if soffice:
        return soffice
    
    # MacOS
    if platform.system() == "Darwin":
        path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if os.path.exists(path):
            return path
        
    raise FileNotFoundError("LibreOffice(soffice)が見つかりませんでした。")
    
