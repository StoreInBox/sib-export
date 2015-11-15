import csv
import StringIO

from django.template.loader import render_to_string
from lxml import html
import xhtml2pdf.pisa as pisa
import xlsxwriter

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


def _to_html(product_list, template):
    rendered_template = render_to_string(template, {'product_list': product_list})
    return html.document_fromstring(rendered_template)


def to_csv(product_list, template):
    """ Create CSV file with product list """
    result = StringIO.StringIO()
    doc = _to_html(product_list, template)
    writer = csv.writer(result)

    for row_index in doc.findall('.//tr'):
        row_index_text = [el.text_content() for el in row_index]
        writer.writerow(row_index_text)

    return result.getvalue()


def to_xls(product_list, template):
    """ Create XLS file with product list """
    result = StringIO.StringIO()
    doc = _to_html(product_list, template)
    workbook = xlsxwriter.Workbook(result)
    worksheet = workbook.add_worksheet()

    for row_index, row in enumerate(doc.findall('.//tr')):
        for column_index, el in enumerate(row):
            worksheet.write(row_index, column_index, el.text_content())

    header_format = workbook.add_format({'bold': True})
    header_format.set_align('center')
    worksheet.set_row(0, 15, header_format)
    workbook.close()

    return result.getvalue()
