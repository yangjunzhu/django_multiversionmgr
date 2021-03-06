﻿#coding=utf-8
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DirEventHandler(FileSystemEventHandler):
    """监视目录状态变化事件."""

    def __init__(self, listener=None):
        self.listener = listener

    def on_moved(self, event):
        super(DirEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

        self._changed(event)

        #if self.listener:
        #    self.listener.changeFiles((event.src_path, evnet.dest_path))

        #def on_created(self, event):
        #  super(dirEventHandler, self).on_created(event)

        #  what = 'directory' if event.is_directory else 'file'
        #  logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(DirEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

        self._changed(event)

    def on_modified(self, event):
        super(DirEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)

        self._changed(event)

    def _changed(self, event):
        if self.listener:
            if event.is_directory:
                self.listener.changedir(event.src_path)
            else:
                self.listener.changefile(event.src_path)


class WatchDir(object):
    """监视目录下文件状态."""

    def __init__(self, rootpath='', listener=None):
        self.rootpath = rootpath
        self.observer = None
        self.listener = listener

    def start(self):
        event_handler = DirEventHandler(self.listener)
        self.observer = Observer()
        self.observer.schedule(event_handler, self.rootpath, recursive=True)
        self.observer.start()
        self.observer.join()

    def stop(self):
        self.observer.stop()


if __name__ == "__main__":
    watch = WatchDir('./')
    watch.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        watch.stop()
