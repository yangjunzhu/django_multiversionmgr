import os

from models import FileInfo


class CreateVersion:
    def __init__(self, directory):
        self.observer = None
        self.directory = directory
        self.files = []

    def setobserver(self, observer):
        self.observer = observer

    def create(self):
        stack = [self.directory]
        self.files = []
        while stack:
            directory = stack.pop()
            relpath = os.path.relpath(directory, self.directory)
            for filename in os.listdir(directory):
                if filename == 'deploy.xml':
                    continue
                fullname = directory + '/' + filename
                if os.path.isdir(fullname):
                    stack.append(fullname)
                else:
                    f = FileInfo()
                    f.filepath = relpath
                    f.filename = filename
                    self.files.append(f)
        if self.observer:
            self.observer.createmd5code(self.directory, self.files)
