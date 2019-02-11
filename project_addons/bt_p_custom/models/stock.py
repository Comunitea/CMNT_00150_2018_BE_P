# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    use_date_date = fields.Date(compute='_compute_use_date_date', store=True)

    @api.depends('use_date')
    def _compute_use_date_date(self):
        for lot in self:
            if not lot.use_date:
                lot.use_date_date = None
                continue
            use_date_datetime = fields.Datetime.from_string(lot.use_date)
            lot.use_date_date = fields.Date.to_string(use_date_datetime.date())
