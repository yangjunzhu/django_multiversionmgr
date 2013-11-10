import hashlib


def getfilemd5code(fullname):
    message = ''
    with open(fullname, 'r') as f:
        message = f.read()
    m = hashlib.md5()
    m.update(message)
    return m.hexdigest()
