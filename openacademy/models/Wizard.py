# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'openacademy.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    #il ajoute au wizard la session courant
    def _default_sessions(self):
        return self.env['openacademy.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('openacademy.session', string="Sessions", required=True, default=_default_sessions)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    #lors d'un click sur subscride il ajoute les participants choisis à toutes les sessions séléctionnées
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
