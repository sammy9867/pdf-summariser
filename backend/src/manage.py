#!/usr/bin/env python

import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # This allows easy import of modules from the parent directory
    current_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(current_path)

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
