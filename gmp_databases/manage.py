#!/usr/bin/env python
import os
import sys

os.environ["PYTHON_EGG_CACHE"] = os.path.abspath(os.path.dirname(__file__))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gmp_databases.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
