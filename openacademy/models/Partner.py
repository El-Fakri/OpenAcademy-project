# -*- coding: utf-8 -*-
from odoo import fields, models,_


class Partner(models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean("Instructor", default=False)#, domain=[('instructor', '=', True)])
    sessions = fields.One2many('openacademy.session', 'instructor_id', string="Sessions")
    session_ids = fields.Many2many('openacademy.session', string="Attended Sessions", readonly=True)
    num_sessions = fields.Integer(string='nbr_of_sessions', compute='comp_sess')

    def comp_sess(self):
        self.num_sessions = len(self.sessions)

