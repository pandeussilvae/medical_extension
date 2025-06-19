# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class medical_extension(models.Model):
#     _name = 'medical_extension.medical_extension'
#     _description = 'medical_extension.medical_extension'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
from odoo import models, fields, api

class MedicalPatientHistory(models.Model):
    _name = 'medical.patient.history'
    _description = 'Patient Admission History'

    patient_id = fields.Many2one('res.partner', string='Paziente', ondelete='cascade')
    admission_date = fields.Date(string='Data di Carico')
    discharge_date = fields.Date(string='Dimissioni')
    notes = fields.Text(string='Note')
