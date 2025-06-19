# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class MedicalPatientHistory(models.Model):
    _name = 'medical.patient.history'
    _description = 'Storico periodi terapici effettuati'

    patient_id = fields.Many2one('res.partner', string='Paziente', ondelete='cascade')
    admission_date = fields.Date(string='Data di Carico')
    discharge_date = fields.Date(string='Dimissioni')
    notes = fields.Text(string='Note')

class RelationType(models.Model):
    _name = 'patient.relation.type'
    _description = 'Tipo di Relazione'

    name = fields.Char(string='Nome relazione', required=True)
    description = fields.Char(string='Descrizione')


class PatientRelation(models.Model):
    _name = 'patient.relation'
    _description = 'Crea la relazione tra il Paziente e gli altri Contatti'

    main_model_id = fields.Many2one('res.partner', string='Paziente', required=True, ondelete='cascade')
    contact_id = fields.Many2one('res.partner', string='Contatto Relazione', required=True, ondelete='cascade')
    relation_type_id = fields.Many2one('patient.relation.type', string='Tipo di Relazione', required=True)

class MedicalDiagnosis(models.Model):
    _name = 'medical.diagnosis'
    _description = 'Tipi di Diagnosi'

    name = fields.Char('Diagnosis Name', required=True)
    description = fields.Text('Description')

class PatientDiagnosis(models.Model):
    _name = 'patient.diagnosis'
    _description = 'Diagnosi del Paziente'

    patient_diag_id = fields.Many2one('res.partner', string='Paziente', required=False, ondelete='cascade')
    diagnosis_id = fields.Many2one('medical.diagnosis', string='Diagnosi')
    severity = fields.Selection([
        ('not applicable', 'Non Applicabile'),
        ('low', 'Basso'),
        ('medium', 'Medio'),
        ('high', 'Alto')
    ], string='Gravità', required=False)


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_patient = fields.Boolean(string='è Paziente')
    is_doctor = fields.Boolean(string='è Medico')
    is_nurse = fields.Boolean(string='è Infermiere')
    is_therapist = fields.Boolean(string='è Terapista')

    # Campo computed per determinare se il paziente è attualmente in carico
    is_currently_admitted = fields.Boolean(
        string='Paziente in carico',
        compute='_compute_is_currently_admitted',
        store=True,
        help='Indica se il paziente ha un periodo terapico attivo (caricato ma non dimesso)'
    )

    # Campo computed per determinare se il paziente è dimesso
    is_discharged = fields.Boolean(
        string='Paziente Dimesso',
        compute='_compute_is_discharged',
        store=True,
        help='Indica se il paziente è stato dimesso e non ha nuovi periodi terapici aperti'
    )

    # Campo computed per determinare se il paziente non è mai stato preso in carico
    never_admitted = fields.Boolean(
        string='Mai preso in carico',
        compute='_compute_never_admitted',
        store=True,
        help='Indica se il paziente non è mai stato preso in carico (nessun periodo terapico registrato)'
    )

    # Modificato per fare riferimento ai campi esistenti nel modulo partner_contact_birthplace
    patient_birthplace = fields.Char(related='birth_city', string='Città di nascita', readonly=False)
    patient_birth_state_id = fields.Many2one(related='birth_state_id', comodel_name="res.country.state", string='Provincia di nascita', readonly=False)
    patient_birth_country_id = fields.Many2one(related='birth_country_id', comodel_name="res.country", string='Stato di nascita', readonly=False)

    patient_birthdate = fields.Date(related='birthdate_date', string='Data di nascita', readonly=False)
    patient_age = fields.Integer(related='age', string='Età')

    @api.depends('patient_history_ids')
    def _compute_never_admitted(self):
        """Calcola se il paziente non è mai stato preso in carico"""
        for partner in self:
            if not partner.is_patient:
                partner.never_admitted = False
                continue
            
            partner.never_admitted = not bool(partner.patient_history_ids)

    @api.depends('patient_history_ids.admission_date', 'patient_history_ids.discharge_date')
    def _compute_is_currently_admitted(self):
        """Calcola se il paziente è attualmente in carico"""
        for partner in self:
            if not partner.is_patient:
                partner.is_currently_admitted = False
                continue
                
            # Cerca se esiste almeno un periodo terapico con data di carico ma senza dimissioni
            active_periods = partner.patient_history_ids.filtered(
                lambda h: h.admission_date and not h.discharge_date
            )
            partner.is_currently_admitted = bool(active_periods)

    @api.depends('patient_history_ids.admission_date', 'patient_history_ids.discharge_date')
    def _compute_is_discharged(self):
        """Calcola se il paziente è dimesso"""
        for partner in self:
            if not partner.is_patient:
                partner.is_discharged = False
                continue

            # Ordina i periodi terapici per data di ammissione decrescente
            sorted_periods = partner.patient_history_ids.sorted(lambda h: h.admission_date or fields.Date.min, reverse=True)
            
            # Se non ci sono periodi, non è dimesso
            if not sorted_periods:
                partner.is_discharged = False
                continue

            # Prendi l'ultimo periodo
            last_period = sorted_periods[0]
            
            # Il paziente è dimesso se l'ultimo periodo ha una data di dimissione
            # e non ci sono periodi aperti successivi
            partner.is_discharged = bool(last_period.discharge_date and not partner.is_currently_admitted)

    patient_relations = fields.One2many('patient.relation', 'main_model_id', string='Relazioni Paziente')
    patient_diagnosis_ids = fields.One2many('patient.diagnosis', 'patient_diag_id', string='Diagnosi del Paziente')
    patient_history_ids = fields.One2many('medical.patient.history', 'patient_id', string='Storico Periodi terapici')
