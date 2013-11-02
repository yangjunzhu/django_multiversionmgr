import hashlib

def getFileMD5Code(fullname):
    message = ''
    try:
        with open(fullname, 'r') as f:
            message = f.read()
    except Exception:
        return ''
    m = hashlib.md5()
    m.update(message)
    return m.hexdigest()
