
from odoo import models, fields, api

class Teachers(models.Model):
    _name = 'openacademy.teachers'

    name = fields.Char()
    biography = fields.Html()

    course_ids = fields.One2many('openacademy.course', 'teacher_id', string="Courses")
