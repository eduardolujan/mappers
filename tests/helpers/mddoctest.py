# -*- coding: utf-8 -*-
from doctest import testfile
from glob import glob
from os import environ
from sys import exit

from django.apps import apps
from django.conf import settings
from django.core import management


def _setup():
    environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
    apps.populate(settings.INSTALLED_APPS)
    management.call_command("migrate")
    management.call_command("loaddata", "examples.yaml")


def _main():
    markdown_files = glob("**/*.md", recursive=True)
    exit_code = 0
    for markdown_file in markdown_files:
        failed, attempted = testfile(markdown_file, module_relative=False)
        exit_code += failed
    exit(exit_code)


if __name__ == "__main__":  # pragma: no branch
    _setup()
    _main()
