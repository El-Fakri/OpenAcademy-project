# -*- coding: utf-8 -*-
from odoo import http



# def do_before():
#     print("test")

class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public')
    def index(self, **kw):
         return "Hello, Mahdi"

# class Extension(Openacademy):
#     @http.route('/openacademy/openacademy/2', auth='user')
#     def handler(self):
#         do_before()
#         return super(Extension, self).index()

#     @http.route('/openacademy/openacademy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('openacademy.listing', {
#             'root': '/openacademy/openacademy',
#             'objects': http.request.env['openacademy.openacademy'].search([]),
#         })

#     @http.route('/openacademy/openacademy/objects/<model("openacademy.openacademy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openacademy.object', {
#             'object': obj
#         })
