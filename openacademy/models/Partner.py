# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions,_
from odoo.tools.misc import formatLang, format_date, get_lang
import base64
import csv
from io import StringIO


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)#, domain=[('instructor', '=', True)])
    sessions = fields.One2many('openacademy.session', 'instructor_id', string="Sessions")
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
    num_sessions = fields.Integer(string='nbr_of_sessions', compute='comp_sess')
    nbr_of_invoices = fields.Integer(string="count invoice", compute="nbr_invoices")
    id_of_latest_invoice = fields.Integer(string='id_of_latest_invoice')
    session_facturee = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_facturee = []

    def nbr_invoices(self):
        self.nbr_of_invoices = self.env['account.move'].search_count([('partner_id', '=', self.id)])

    def comp_sess(self):
        self.num_sessions = len(self.sessions)


    def generer_facture(self):

        # id_product_template = self.env['product.template'].search([('name', 'ilike', 'Session')]).id
        id_product_template = self.env['product.template'].search([('name', 'ilike', 'Session Article')]).id
        id_product_product = self.env['product.product'].search([('product_tmpl_id', '=', id_product_template)]).id
        name = "Session"
        quantity = 0
        unit_price = 0
        test = 0
        data = {
            'partner_id': self.id,
            'type': 'out_invoice',
            "invoice_line_ids": [],
        }

        for session in self.session_ids:

            if session.id in self.session_facturee:
                continue

            if session.state == "confirmed":
                test = test + 1
                quantity = quantity + session.duration
                self.session_facturee.append(session.id)
                print(self.session_facturee)
                # print(quantity)
            unit_price = session.price_for_one_hour

        if test == 0:
            print("No Session to put Invoice For this Costumer")
            raise exceptions.ValidationError("No Session to put Invoice For this Costumer")

        line2 = {
            "name": name,
            "quantity": quantity,
            "product_id": id_product_product,
            "price_unit": unit_price,

        }

        data["invoice_line_ids"].append((0, 0, line2))
        invoice = self.env['account.move'].create(data)
        self.id_of_latest_invoice = invoice.id
        # print(self.id_of_latest_invoice)

        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        form_view = [(self.env.ref('account.view_move_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = invoice.id

        context = {
            'default_type': 'out_invoice',
        }

        action['context'] = context
        return action

    def view_invoice(self):
        invoices = self.mapped('invoice_ids')
        action = self.env.ref('account.action_move_out_invoice_type').read()[0]
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_type': 'out_invoice',
        }

        action['context'] = context
        return action

    def print_invoices(self):
        invoice = self.env['account.move'].search([('id', '=', self.id_of_latest_invoice)])
        print(invoice.id)
        print(self.id)
        return self.env.ref('account.account_invoices').report_action(invoice)
