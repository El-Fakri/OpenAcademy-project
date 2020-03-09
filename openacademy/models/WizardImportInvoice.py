# -- coding: utf-8 --

from odoo import models, fields, exceptions
import csv
import os
from io import StringIO
import logging
import base64
from tempfile import TemporaryFile
from datetime import datetime
_logger = logging.getLogger(__name__)


class WizardImportInvoice(models.TransientModel):
    _name = 'openacademy.import'
    _description = "Wizard: Quick Import of Invoices"

    File = fields.Binary(string="Select File", required=True)

    def import_file(self):

        csv_datas = self.File
        fileobj = TemporaryFile('wb+')
        csv_datas = base64.decodestring(csv_datas)
        fileobj.write(csv_datas)
        fileobj.seek(0)
        str_csv_data = fileobj.read().decode('utf-8')
        lis = csv.reader(StringIO(str_csv_data), delimiter=',')

        rownum = 0
        a = 0
        invoice_name = ""
        invoice_date = ""
        invoice_salesperson = ""
        invoice_company = ""
        invoice_dueDate = ""
        invoice_untaxedAmount = ""
        invoice_TOT = ""
        invoice_amountDueSigned = ""
        invoice_status = ""
        invoice_createdOn = ""
        invoice_lineLabel = ""
        invoice_linePartner = ""
        invoice_lineProductName = ""
        invoice_lineProduct = ""

        for row in lis:

            if rownum == 0:
                # ici le header est une liste qui contient les tete de column
                header = row
            else:
                #avec cette boucle on affiche chaque element de la liste
                # for i in row:
                #     print(i)
                # avec cette print on affiche le premier element de la ligne 0 qui est la premiere ligne après le header
                #     print(row[0])
                while a <= 13:
                    if header[a] == "Invoice Partner Display Name":
                        invoice_name = row[a]
                    elif header[a] == "Invoice/Bill Date":
                        invoice_date = row[a]
                    elif header[a] == "Salesperson":
                        invoice_salesperson = row[a]
                    elif header[a] == "Company":
                        invoice_company = row[a]
                    elif header[a] == "Due Date":
                        invoice_dueDate = row[a]
                    elif header[a] == "Untaxed Amount Signed":
                        invoice_untaxedAmount = row[a]
                    elif header[a] == "Total Signed":
                        invoice_TOT = row[a]
                    elif header[a] == "Amount Due Signed":
                        invoice_amountDueSigned = row[a]
                    elif header[a] == "Status":
                        invoice_status = row[a]
                    elif header[a] == "Invoice lines/Created on":
                        invoice_createdOn = row[a]
                    elif header[a] == "Invoice lines/Label":
                        invoice_lineLabel = row[a]
                    elif header[a] == "Invoice lines/Partner":
                        invoice_linePartner = row[a]
                    elif header[a] == "Invoice lines/Product/Name":
                        invoice_lineProductName = row[a]
                    elif header[a] == "Invoice lines/Product/Product":
                        invoice_lineProduct = row[a]
                    a = a+1
            rownum += 1

        id_product_template = self.env['product.template'].search([('name', 'ilike', invoice_lineProductName)]).id
        id_product_product = self.env['product.product'].search([('product_tmpl_id', '=', id_product_template)]).id

        context = self._context

        current_uid = context.get('uid')

        user = self.env['res.partner'].browse(current_uid)
        data = {
            'partner_id': user,
            'type': 'in_invoice',
            'invoice_date': invoice_date,
            "invoice_line_ids": [],
        }

        line = {
            "name": invoice_name,
            "product_id": id_product_product,
            "quantity": 10,
            "price_unit": invoice_TOT,

        }
        data["invoice_line_ids"].append((0, 0, line))
        invoice = self.env['account.move'].create(data)

        return {}
