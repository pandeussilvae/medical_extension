# -*- coding: utf-8 -*-
# from odoo import http


# class MedicalExtension(http.Controller):
#     @http.route('/medical_extension/medical_extension/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/medical_extension/medical_extension/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('medical_extension.listing', {
#             'root': '/medical_extension/medical_extension',
#             'objects': http.request.env['medical_extension.medical_extension'].search([]),
#         })

#     @http.route('/medical_extension/medical_extension/objects/<model("medical_extension.medical_extension"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('medical_extension.object', {
#             'object': obj
#         })
