from sched import scheduler
import threading
from django.apps import AppConfig


class FileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'file'

    def ready(self) -> None:
        from . import signals
        
        def sched_job():
            from file.models import File
            import sched
            import time

            s = sched.scheduler(time.time, time.sleep)
            while True:
                s.enter(60 * 60, 1, lambda: File.objects.expired().delete())
                s.run(blocking=True)
            
        self.scheduling_thread = threading.Thread(target=sched_job, daemon=True)
        self.scheduling_thread.name = 'scheduling_thread'
        self.scheduling_thread.start()