#!/usr/bin/python
###############################################################################
# Copyleft (K) 2020-2022
# Developer: Giuseppe Checchia @eldoleo (<https://github.com/giuseppechecchia>)
###############################################################################

from odoo import models, fields
from emailrep import EmailRep

import logging

_logger = logging.getLogger(__name__)


class MailRepResUsers(models.Model):

    _inherit = 'res.company'

    emailrep_api_key = fields.Char(
        'EmailRep API Key'
    )


class OdooEmailRepResUsers(models.Model):

    _name = 'odoo.emailrep.checks'

    _description = 'res.users validated users'

    res_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Odoo user'

    )

    is_checked = fields.Boolean(
        'User just checked',
        default=False,
        readonly=True
    )

    reputation = fields.Char(
        'Address reputation'
    )

    suspicious = fields.Boolean(
        'Is suspicious',
        default=False
    )

    blacklisted = fields.Boolean(
        'Is blacklisted',
        default=False
    )


class OdooEmailRep(models.AbstractModel):

    _name = 'odoo.emailrep.datas'

    _description = 'EmailRep methods'

    def emailrep_my_users(self):

        companies = self.env['res.company'].search([])

        # assuming we had just one company
        company = companies[0]
        emailrep = EmailRep(company.emailrep_api_key)

        users_obj = self.env['res.users'].search(
            [
                ('active', '=', 1)
            ]
        )

        for u in users_obj:

            # I'm working on not check only
            my_checked_user = self.env['odoo.emailrep.checks'].search(
                [
                    ('res_user_id', '=', u.id),
                    ('is_checked', '=', False)
                ]
            )

            if my_checked_user:
                r = emailrep.query(u.login)
                # email = r['email']
                reputation = r['reputation']
                suspicious = r['suspicious']
                blacklisted = r['details']['blacklisted']

            # diff on update nor insert
            if my_checked_user:
                # update
                my_checked_user.write(
                    {
                        'res_user_id': u.id,
                        'reputation': reputation,
                        'suspicious': suspicious,
                        'blacklisted': blacklisted,
                        'is_checked': True
                    })
            else:
                # create
                my_checked_user.create(
                    {
                        'res_user_id': u.id,
                        'is_checked': True,
                        'reputation': reputation,
                        'suspicious': suspicious,
                        'blacklisted': blacklisted
                    }
                )

            # update immediately to avoid losing data on
            # long running / big res.users table cases
            self.env.cr.commit()

            # just logging something in a dummy way
            _logger.info(f"{u.login} checked and done!")
