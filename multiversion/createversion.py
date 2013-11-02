import os
import hashlib

from models import FileInfo


class CreateVersion:
    def __init__(self, directory):
        self.observer = None
        self.directory = directory
        self.files = []

    def setObserver(self, observer):
        self.observer = observer

    def create(self):
        stack = [self.directory]
        self.files = []
        while stack:
            directory = stack.pop()
            relpath = os.path.relpath(directory, self.directory)
            for file in os.listdir(directory):
                if file == 'deploy.xml':
                    continue
                fullname = directory + '/' + file
                if os.path.isdir(fullname):
                    stack.append(fullname)
                else:
                    f = FileInfo()
                    f.filepath = relpath
                    f.filename = file
                    self.files.append(f)
        if self.observer:
            self.observer.createmd5Code(self.directory, self.files)


