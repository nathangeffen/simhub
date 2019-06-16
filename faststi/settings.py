from django.conf import settings


DATA_DIR = getattr(settings, "FSTI_DATA_DIR", "")
EXE_DIR = getattr(settings, "FSTI_EXE_DIR", "")
EXE_NAME = getattr(settings, "FSTI_EXE_NAME", "faststi")
