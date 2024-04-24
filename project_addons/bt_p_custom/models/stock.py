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


class StockMove(models.Model):
    _inherit = 'stock.move'

    show_check_availability = fields.Boolean(related='picking_id.show_check_availability')
    qty_available = fields.Float('Qty available', related='product_id.qty_available')
    reserved_qty = fields.Float('Reserved qty', related='product_id.reserved_qty')

    def indivual_action_assign(self):
        if not self.filtered(lambda move: move.state not in ('draft', 'cancel', 'done')):
            raise UserError(_('Nothing to check the availability for.'))
        for move in self.filtered(lambda move: move.state not in ('draft', 'cancel', 'done')):
            move._action_assign()

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    partner_id = fields.Many2one('res.partner', related='picking_id.partner_id')


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    use_date = fields.Datetime(string='Use date', related="lot_id.use_date")
