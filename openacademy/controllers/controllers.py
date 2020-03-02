# -*- coding: utf-8 -*-
from odoo import http



# def do_before():
#     print("test")

# class Openacademy(http.Controller):
#     @http.route('/openacademy/openacademy/', auth='public')
#     def index(self, **kw):
# #         return "Hello, Mahdi"
# #return ci-dessous permet de passer une liste des profs au template
# #         return http.request.render('openacademy.index', {
# #             'teachers': ["Diana Padilla", "Jody Caroll", "Lester Vaughn"],
# #         })
#         Teachers = http.request.env['openacademy.teachers']
#         return http.request.render('openacademy.index', {
#             'teachers': Teachers.search([])
#         })


class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy/', auth='public', website=True)
    def index(self, **kw):

        Teachers = http.request.env['openacademy.teachers'] # ici http.request.env['openacademy.teachers'] pointe sur objet teacher
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([])
        })
    #si on passe l'url : /openacademy/openacademy/mahdi , il affichera mahdi en <h1>
    # @http.route('/openacademy/openacademy/<name>/', auth='public', website=True)
    # def teacher(self, name):
    #     return '<h1>{}</h1>'.format(name)

    # si on passe l'url : /openacademy/openacademy/2 , il affichera 2 en <h1> avec son type qui est int
    # @http.route('/openacademy/openacademy/<int:id>/', auth='public', website=True)
    # def teacher(self, id):
    #     return '<h1>{} ({})</h1>'.format(id, type(id).__name__)


    @http.route('/openacademy/openacademy/<model("openacademy.teachers"):teacher>/', auth='public', website=True)
    def teacher(self, teacher):
        return http.request.render('openacademy.biography', {
            'person': teacher
        })
