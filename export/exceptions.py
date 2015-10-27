class ExportError(Exception):
    pass


class ExportSettingsError(ExportError):
    pass


class PDFExportError(ExportError):
    pass
