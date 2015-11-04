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


def _to_string(product_list, template):
    result = StringIO.StringIO()
    rendered_template = render_to_string(template, {'product_list': product_list})
    doc = html.document_fromstring(rendered_template)
    return [result, doc]


def to_csv(product_list, template):
    """ Create CSV file with product list """
    result, doc = _to_string(product_list, template)
    writer = csv.writer(result)

    for row_index in doc.findall('.//tr'):
        row_index_text = [el.text_content() for el in row_index]
        writer.writerow(row_index_text)

    return result.getvalue()


def to_xls(product_list, template):
    """ Create xls file with product list """
    result, doc = _to_string(product_list, template)
    workbook  = xlsxwriter.Workbook(result)
    worksheet = workbook.add_worksheet()

    for row_index, row in enumerate(doc.findall('.//tr')):
        for column_index, el in enumerate(row):
            worksheet.write(row_index, column_index, el.text_content())

    header_format = workbook.add_format({'bold': True})
    header_format.set_align('center')
    column_format = workbook.add_format({'num_format': True})
    column_format.set_align('right')
    worksheet.set_row(0, 15, header_format)
    worksheet.set_column('B:B', 10, column_format)
    worksheet.set_column('A:A', 20)
    workbook.close()

    return result.getvalue()
