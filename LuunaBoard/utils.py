from LuunaBoard.config import ALLOWED_EXTENSIONS

def allowed_image(filename):
    extension = filename.split('.')[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False