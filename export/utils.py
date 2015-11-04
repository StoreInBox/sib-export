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


class Common(object):
    def __init__(self, product_list, template):
        self.result = StringIO.StringIO()
        rendered_template = render_to_string(template, {'product_list': product_list})
        self.doc = html.document_fromstring(rendered_template)


class CsvObject(Common):
    def get(self):
        writer = csv.writer(self.result)

        for table_row in self.doc.findall('.//tr'):
            table_row_text = [el.text_content() for el in table_row]
            writer.writerow(table_row_text)

        return self.result.getvalue()


class XlsObject(Common):
    def get(self):
        workbook  = xlsxwriter.Workbook(self.result)
        worksheet = workbook.add_worksheet()

        row_counter = 0
        for table_row in self.doc.findall('.//tr'):

            column_counter = 0
            for el in table_row:
                worksheet.write(row_counter, column_counter, el.text_content() )
                column_counter += 1

            row_counter += 1
        format1 = workbook.add_format({'bold': True})
        format1.set_align('center')
        format2 = workbook.add_format({'num_format': True})
        format2.set_align('right')
        worksheet.set_row(0, 15, format1)
        worksheet.set_column('B:B', 10, format2)
        worksheet.set_column('A:A', 20)
        workbook.close()
        return self.result.getvalue()


def to_csv(product_list, template):
    """ Create CSV file with product list """
    return CsvObject(product_list, template).get()


def to_xls(product_list, template):
    """ Create xls file with product list """
    return XlsObject(product_list, template).get()
