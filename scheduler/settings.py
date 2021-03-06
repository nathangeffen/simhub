import tempfile
from django.conf import settings

OUTPUT_FILE_DIR = getattr(settings, 'SCHEDULER_OUTPUT_FILE_DIR',
                          tempfile.gettempdir())
OUTPUT_FILE_PREFIX = getattr(settings, 'SCHEDULER_OUTPUT_FILE_PREFIX', "out_")
OUTPUT_FILE_SUFFIX = getattr(settings, 'SCHEDULER_OUTPUT_FILE_SUFFIX', ".txt")
MAX_JOBS_RUNNING = getattr(settings, 'SCHEDULER_MAX_JOBS_RUNNING', 2)
MAX_JOBS_WAITING = getattr(settings, 'SCHEDULER_MAX_JOBS_WAITING', 100)
LINES_TO_READ = getattr(settings, 'SCHEDULER_LINES_TO_READ', 128)
TIMEOUT = getattr(settings, 'SCHEDULER_TIMEOUT', 60)
NO_PING_TIMEOUT = getattr(settings, 'SCHEDULER_NO_PING_TIMEOUT', 60)
ZOMBIE_REMOVAL_QUEUE_SIZE = getattr(settings,
                                    'SCHEDULER_ZOMBIE_REMOVAL_QUEUE_SIZE', 10)
