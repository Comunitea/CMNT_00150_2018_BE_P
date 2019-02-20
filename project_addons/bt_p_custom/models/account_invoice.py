# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    def write(self, vals):
        if vals.get('state', '') == 'draft' and 'date' in vals:
            del vals['date']
        return super().write(vals)
