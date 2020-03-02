# -*- coding: utf-8 -*-
from odoo import fields, models,_


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False, domain=[('instructor', '=', True)])
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)

