from datetime import timedelta
from odoo import models, fields, api, exceptions,_


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)
    color = fields.Integer()
    state = fields.Selection([('draft', "Draft"), ('progress', "In_Progress"), ('confirmed', "Confirmed"), ], default='draft')

    instructor_id = fields.Many2one('res.partner', string="Instructor",  domain=[('instructor', '=', True)])
                                    # ('category_id.name', 'ilike', "Teacher")])

    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End Date", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    date_today = fields.Date(required=True, default=fields.Date.context_today)
    price_for_one_hour = fields.Integer(help="Price For One hour in One Session")
    total_price = fields.Integer(help="prix total", compute='SUM')

    invoice_ids = fields.One2many("account.move", "session_id")
    nbr_of_invoices = fields.Integer(string="count invoice", compute="nbr_invoices")

    def SUM(self):
        self.total_price = self.duration * self.price_for_one_hour

    def nbr_invoices(self):
        self.nbr_of_invoices = self.env['account.move'].search_count([('session_id', '=', self.id)])

    def generer_facture(self):

        id_product_template = self.env['product.template'].search([('name', 'ilike', 'Session')]).id
        id_product_product = self.env['product.product'].search([('product_tmpl_id', '=', id_product_template)]).id
        # print(id_product_product)
        
        data = {
            'session_id': self.id,
            'partner_id': self.instructor_id.id,
            'type': 'in_invoice',
            'invoice_date': self.date_today,
            "invoice_line_ids": [],
        }

        line = {
            "name": self.name,
            "product_id": id_product_product,
            "quantity": self.duration,
            "price_unit": self.price_for_one_hour,

        }
        data["invoice_line_ids"].append((0, 0, line))
        invoice = self.env['account.move'].create(data)

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


    def goto_draft(self):
        self.state = 'draft'

    def goto_confirm(self):
        self.state = 'progress'

    def goto_done(self):
        self.state = 'confirmed'

    # lorsque la liste des participants se modifie , il faut changer donc la valeur du nombre des participants
    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

# lorsque le nbr des places ou la liste des participants se modifie , il faut changer donc la valeur places réservé
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

#si le nbr des places ou la liste des participants se modifie , il faut vérifié le nbr des places , s'il est < 0 ==> warning
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue

            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            r.duration = (r.end_date - r.start_date).days + 1

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")
