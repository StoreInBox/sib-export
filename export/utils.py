import StringIO

from django.template.loader import render_to_string
import xhtml2pdf.pisa as pisa

from . import exceptions


def to_pdf(product_list, template):
    """ Create PDF file with product list """
    result = StringIO.StringIO()
    rendered_template = render_to_string(template, {'product_list': product_list})

    pdf = pisa.pisaDocument(StringIO.StringIO(rendered_template), result)
    if not pdf.err:
        return result.getvalue()
    else:
        raise exceptions.PDFExportError('Cannot convert product list to PDF: {}'.format(pdf.err))


def to_csv(product_list, template):
    pass


def to_xls(product_list, template):
    pass
