import csv
import StringIO
from lxml import html

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
    """ Create CSV file with product list """
    result = StringIO.StringIO()
    writer = csv.writer(result)
    rendered_template = render_to_string(template, {'product_list': product_list})
    doc = html.document_fromstring(rendered_template)

    for table_row in doc.find_class('row'):
        table_row_text = [el.text_content() for el in table_row]
        writer.writerow(table_row_text)

    return result.getvalue()


def to_xls(product_list, template):
    pass
