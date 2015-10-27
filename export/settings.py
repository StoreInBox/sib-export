from django.apps import apps
from django.conf import settings

from .exceptions import ExportSettingsError


class ExternalModels(object):
    PRODUCT_MODEL_KEY = 'Product'

    EXTERNAL_MODELS_MAP = {
        'Product': PRODUCT_MODEL_KEY,
    }

    def __getattr__(self, name):
        return self.get_model(name)

    def get_model(self, name):
        if not hasattr(self, name):
            path = self.get_model_path(name)
            try:
                model = apps.get_model(path)
            except LookupError as e:
                raise ExportSettingsError(
                    'Cannot import model "%s" for export application: %s' % (name, e))
            setattr(self, name, model)
        return getattr(self, name)

    def get_model_path(self, name):
        if name not in self.EXTERNAL_MODELS_MAP:
            raise ExportSettingsError('Model %s is not defined as external model' % name)
        key = self.EXTERNAL_MODELS_MAP[name]
        try:
            export_settings = settings.EXPORT
        except AttributeError:
            raise ExportSettingsError(
                'Cannot find EXPORT variable in settings. It need to be configured for application "export"')
        try:
            path = export_settings[key]
        except KeyError:
            raise ExportSettingsError(
                'Cannot find model "%s" in EXPORT settings. It has to be configured with key "%s"' % (name, key))
        return path


external_models = ExternalModels()
