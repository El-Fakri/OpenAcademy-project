# -*- coding: utf-8 -*-
from odoo import http

class Openacademy(http.Controller):
    @http.route(['/my/', '/my/home/'], auth='user', website=True)
    def index(self, **kw):

        # instructors = http.request.env['res.partner'].sudo() # ici si on fait sudo() on va recevoir tt les res.partner
        id_user = http.request.env.user.partner_id.id
        instructor = http.request.env['res.partner'].search([('id', '=', id_user)])
        name_instructor = instructor.name
        num_sess_instructor = instructor.num_sessions

        return http.request.render('openacademy.index', {
            # 'instructors': instructors.search([])
            # 'instructors': instructors,
            'name': name_instructor,
            'nbr_sess': num_sess_instructor,
            'slugg': id_user,

        })

    # @http.route(['/my/<model("res.partner"):instructor>/', '/my/home/<model("res.partner"):instructor>/'], auth='user', website=True)
    @http.route(['/my/home/<model("res.partner"):instructor>/'], auth='user', website=True)
    def instructor(self, instructor):

        sessions = list(instructor.sessions)
        instructor_id = sessions[0].instructor_id

        return http.request.render('openacademy.sessions', {
            'session': sessions,
            'instructor_id': instructor_id
        })

    # @http.route(['/my/session/<model("openacademy.session"):session>/', '/my/home/session/<model("openacademy.session"):session>/'], auth='user', website=True)
    @http.route(['/my/home/session/<model("openacademy.session"):session>/'], auth='user', website=True)
    def session(self, session):
        return http.request.render('openacademy.sessionsForm', {
            'session': session
        })

    @http.route(['/my/home/session/edit/<model("openacademy.session"):session>/'], auth='user', website=True)
    def session_edit(self, session):

        return http.request.render('openacademy.sessionsEdit', {
            'session': session
        })

    @http.route(['/my/home/session/edit/done/'], auth='user', website=True, methods=['POST'], csrf=False)
    def session_edit_done(self, **kw):

        # print(kw['InstId'])
        # print(kw['duration'])
        id_sess = kw['SessId']
        session = http.request.env['openacademy.session'].search([('id', '=', id_sess)])
        session.start_date = kw['StartDate']
        session.seats = kw['seats']
        session.end_date = kw['EndDate']

        return http.request.render('openacademy.sessionsForm', {
            'session': session
        })

    @http.route(['/my/home/session/add/<model("res.partner"):instructor>/'], auth='user', website=True)
    def session_add(self, instructor):

        courses = http.request.env['openacademy.course'].search([])

        return http.request.render('openacademy.sessionsAdd', {
            'instructor': instructor,
            'courses': courses,
        })

    @http.route(['/my/home/session/add/done/'], auth='user', website=True, methods=['POST'], csrf=False)
    def session_add_done(self, **kw):
        # print(kw['InstId'])
        # print(kw['SessId'])
        id_instructor = kw['InstId']
        id_course = int(kw['CourseId'])
        instructor = http.request.env['res.partner'].search([('id', '=', id_instructor)])
        start_date = kw['StartDate']
        name = kw['name']
        seats = kw['seats']
        end_date = kw['EndDate']

        http.request.env['openacademy.session'].create({'start_date': start_date,
                                                        'seats': seats, 'end_date': end_date, 'name': name,
                                                        'course_id': id_course ,'instructor_id': instructor.id})
        sessions = list(instructor.sessions)
        instructor_id = sessions[0].instructor_id

        return http.request.render('openacademy.sessions', {
            'session': sessions,
            'instructor_id': instructor_id
        })
