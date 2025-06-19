# -*- coding: utf-8 -*-
{
    'name': 'Medical Extension',
    'summary': 'Estende le funzionalità di contatto per il modulo medicale',
    'author': "Paolo Nugnes",
    'website': "https://www.techlab.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Medical',
    'version': '14.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'contacts',
        'calendar',
        'partner_contact_birthplace',
        'partner_contact_birthdate'
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'security/ir.model.access.csv',
#        'security/medical_extension.xml',
#        'security/medical_access_rules.xml',
        'views/res_partner.xml',  # Aggiungi questo file per configurare le viste dei contatti con i nuovi campi
#        'views/medical_actions.xml',
        'views/medical_menu.xml'  # Aggiungi questo file per configurare le viste e i menu
    ],
    'assets': {
        'web.assets_common': [
            'medical_extension/static/src/img/signature.png',
        ],
        'web.assets_backend': [
            'medical_extension/static/src/img/logo_white.png'
#        ],
#        'web.assets_frontend': [
#            'medical_extension/static/src/css/custom_styles.css',
#            'medical_extension/static/src/js/custom_behavior.js'
        ]
    },
    'installable': True,
    'application': True,
    'images': [
        'medical_extension/static/src/img/logo_module.png'
    ],
    'icon': 'medical_extension/static/src/img/logo_module.png',
    'license': 'LGPL-3'
}
