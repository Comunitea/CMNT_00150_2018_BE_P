from odoo import _, api, fields, models
from datetime import datetime, timedelta


class Lead(models.Model):
    _inherit = 'crm.lead'
    validity_date = fields.Date(string='Expiration Date',copy=False)
    is_expired = fields.Boolean(compute='_compute_is_expired', string="Is expired")

    def _compute_is_expired(self):
        now = datetime.now()
        for lead in self:
            if lead.validity_date and fields.Datetime.from_string(lead.validity_date) < now:
                lead.is_expired = True
            else:
                lead.is_expired = False
