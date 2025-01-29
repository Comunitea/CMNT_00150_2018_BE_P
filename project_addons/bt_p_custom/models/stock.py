# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil import relativedelta
from odoo import api, fields, models, _


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

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lot_alert = fields.Char(compute='_compute_lot_alert')

    @api.depends('move_line_ids.lot_id', 'scheduled_date')
    def _compute_lot_alert(self):
        for picking in self:
            alert_message = ""
            show_alert = False
            if picking.state == 'assigned':
                lot_ids = picking.move_line_ids.mapped('lot_id')
                for lot in lot_ids.filtered(lambda x: x.use_date):
                    lot_date = fields.datetime.strptime(lot.use_date, '%Y-%m-%d %H:%M:%S')
                    now = fields.datetime.strptime(fields.Datetime.now(), '%Y-%m-%d %H:%M:%S')
                    time_diff = relativedelta.relativedelta(lot_date,now)
                    if lot.use_date and time_diff.months < 6:
                        alert_message += _("Lot {} close to expire date: {} \n".format(lot.name, lot.use_date))
                        show_alert = True
            if show_alert:
                picking.lot_alert = alert_message
