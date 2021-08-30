# -*- coding: utf-8 -*-
{
    'name': 'Odoo EmailRep Users Control',
    'summary': 'Simple Email Reputation integration for res.users',
    'description': "Simple Email Reputation integration for res.users",
    'depends': [
        'base',
    ],
    'external_dependencies': {
        'python': [
            'emailrep',
        ],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/emailrep_conf.xml',
        'views/menu.xml'
    ],
    'author': 'Giuseppe Checchia',
    'support': 'giuseppechecchia@gmail.com',
    'auto_install': False,
    'application': False,
    'installable': True
}
