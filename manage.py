#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    if 'test' in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "symposion.settings_test")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "symposion.settings")

    from django.core.management import execute_from_command_line
    
    execute_from_command_line(sys.argv)
