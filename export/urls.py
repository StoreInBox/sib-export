from django.conf.urls import patterns, url

from . import views

export_formats = '|'.join(views.ProductListExportView.implemented_export_formats.keys())

urlpatterns = patterns(
    '',
    url(
        r'^products/export/(?P<export_format>{})/$'.format(export_formats),
        views.ProductListExportView.as_view(),
        name='products-export'
    ),
)
