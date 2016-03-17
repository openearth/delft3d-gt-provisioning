import logging
import time
import itertools

from watchdog.observers import Observer
import watchdog.events

logger = logging.getLogger(__name__)


class NetCDFHandler(watchdog.events.FileSystemEventHandler):
    """handle filesystem changes"""
    def __init__(self,  *args, **kwargs):
        super(NetCDFHandler, self).__init__(*args, **kwargs)
        self.processors = []
        self.observer = None
        # mark if we don't expect anymore changes
        self.done = False
        self.fname_nc = ''

    def on_created(self, event):
        """file created on file system"""
        if isinstance(event, watchdog.events.FileCreatedEvent):
            if event.src_path.endswith('done'):
                logger.info("we're done %s", event)
                self.done = True

    def on_modified(self, event):
        """file modified on filesystem"""
        if isinstance(event, watchdog.events.FileModifiedEvent):
            if event.src_path.endswith(self.fname_nc):
                for processor in self.processors:
                    processor(event.src_path)
            elif event.src_path.endswith('done'):
                logger.info("we're done %s", event)
                self.done = True
