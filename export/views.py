from django import http
from django.views.generic import View

from . import utils
from .settings import external_models


class ProductListExportView(View):
    template = 'export/product_list.html'
    implemented_export_formats = {
        'pdf': utils.to_pdf,
    }

    def get(self, request, export_format, *args, **kwargs):
        product_list = external_models.Product.objects.all()
        export_function = self.implemented_export_formats[export_format]
        exported_file = export_function(product_list, self.template)

        filename = 'exported_product_list.{}'.format(export_format)
        response = http.HttpResponse(exported_file, content_type='application/{}'.format(export_format))
        if request.GET.get('download'):
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)

        return response
