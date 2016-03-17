import logging

import watchdog.events

logger = logging.getLogger(__name__)


class DoneEvent(object):
    """Fired when done"""
    pass


class NetCDFHandler(watchdog.events.FileSystemEventHandler):
    """handle filesystem changes"""
    def __init__(self,  *args, **kwargs):
        super(NetCDFHandler, self).__init__(*args, **kwargs)
        # allow methods to be added when netcdf files change
        self.processors = []
        # allow to extend with extra handlers when done
        self.done_handlers = []
        # mark if we don't expect anymore changes
        self.done = False
        self.fname_nc = '.nc'

    def on_created(self, event):
        """file created on file system"""
        if isinstance(event, watchdog.events.FileCreatedEvent):
            if event.src_path.endswith('done'):
                logger.info("we're done %s", event)
                # raise an event
                event = DoneEvent()
                self.on_done(event)

    def on_done(self, event):
        """call this when done"""
        for handler in self.done_handlers:
            handler()
        self.done = True
        logger.info("All handling is done")

    def on_modified(self, event):
        """file modified on filesystem"""
        if isinstance(event, watchdog.events.FileModifiedEvent):
            if event.src_path.endswith(self.fname_nc):
                for processor in self.processors:
                    processor(event.src_path)
            elif event.src_path.endswith('done'):
                logger.info("we're done %s", event)
                self.done = True
                event = DoneEvent()
                self.on_done(event)