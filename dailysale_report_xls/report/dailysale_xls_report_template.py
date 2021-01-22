# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.dailysale_report_xls.dailysale_xls_report_template'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        domain = []

        # Formats
        grey_format = workbook.add_format({
            'bg_color': '#b2beb5'
        })
        grey_border_format = workbook.add_format({
            'bg_color': '#b2beb5',
            'bottom': 1,
        })
        grey_bold_format = workbook.add_format({
            'bg_color': '#b2beb5',
            'bold': True,
        })

        # Worksheet
        sheet = workbook.add_worksheet('Daily Sales')

        sheet.set_row(0, None, grey_format)
        sheet.set_row(1, None, grey_format)
        sheet.set_row(2, None, grey_border_format)
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 1, 40)

        sheet.write(0, 0, 'Daily Sales', grey_bold_format)
        sheet.write(1, 0, 'Company', grey_bold_format)
        sheet.write(1, 1, 'A Company', grey_format)
        sheet.write(2, 0, 'Run Date & User :', grey_bold_format)
        user_date = str((datetime.today()
                         + timedelta(hours=4)).strftime("%d-%b-%Y %H:%M: %S"))\
            + ', ' \
            + str(self.env.user.name)
        sheet.write(2, 1, user_date, grey_border_format)

        # Daily Sales table headers
        sheet.write(4, 0, 'Invoice Date', grey_bold_format)
        sheet.write(4, 1, 'Journal', grey_bold_format)
        sheet.write(4, 2, 'Customer Name', grey_bold_format)
        sheet.write(4, 3, 'Customer ID', grey_bold_format)
        sheet.write(4, 4, 'Invoice Number', grey_bold_format)
        sheet.write(4, 5, 'SO Number', grey_bold_format)
        sheet.write(4, 6, 'Product Name', grey_bold_format)
        sheet.write(4, 7, 'Product ID', grey_bold_format)
        sheet.write(4, 8, 'Quantity', grey_bold_format)
        sheet.write(4, 9, 'Price Unit', grey_bold_format)
        sheet.write(4, 10, 'SubTotal', grey_bold_format)
        sheet.write(4, 11, 'Amount Without Tax', grey_bold_format)
        sheet.write(4, 12, 'Amount Before Discount', grey_bold_format)
        sheet.write(4, 13, 'State', grey_bold_format)
        sheet.write(4, 14, 'Payment Terms', grey_bold_format)
        sheet.write(4, 15, 'Account', grey_bold_format)
        sheet.write(4, 16, 'Invoice Type', grey_bold_format)
        sheet.write(4, 17, 'Unit of Measure', grey_bold_format)
       
        if data['data']['date_start']:
            domain.append(('date', '>=', data['data']['date_start']))
        if data['data']['date_end']:
            domain.append(('date', '<=', data['data']['date_end']))
        lines = self.env['account.invoice.line'].search(domain)
        row = 5
        
        #Account move and account move line table
        for obj in lines:
            sheet.write(row, 0, lines.Invoice_Date)
            sheet.write(row, 1, lines.Journal)
            sheet.write(row, 2, lines.CustomerName)
            sheet.write(row, 3, lines.CustomerID)
            sheet.write(row, 4, lines.InvoiceNumber)
            sheet.write(row, 5, lines.SONumber)
            sheet.write(row, 6, lines.ProductName)
            sheet.write(row, 7, lines.ProductID)
            sheet.write(row, 8, lines.Quantity)
            sheet.write(row, 9, lines.Price_unit)
            sheet.write(row, 10, lines.Subtotal)
            sheet.write(row, 11, lines.AmountWithoutTax)
            sheet.write(row, 12, lines.Amountbeforediscount)
            sheet.write(row, 13, lines.State)
            sheet.write(row, 14, lines.PaymentTerms)
            sheet.write(row, 15, lines.Account)
            sheet.write(row, 16, lines.InvoiceType)
            sheet.write(row, 17, lines.UOM)
                        
            row += 1

