# coding: utf-8
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ExportConfig(AppConfig):
    name = 'export'
    verbose_name = _('Export')

    def ready(app):
        from . import urls
