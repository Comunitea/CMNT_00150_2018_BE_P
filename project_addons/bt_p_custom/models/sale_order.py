# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ready_to_send = fields.Boolean('Ready to send', default=False)
    sale_type = fields.Selection([
        ('stock', 'STOCK'),
        ('lote', 'LOTE')
    ], string='Sale type', default="stock")

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    qty_available = fields.Float('Qty available', related='product_id.qty_available')
    virtual_available = fields.Float('Virtual available', related='product_id.virtual_available')
    reserved_qty = fields.Float('Reserved qty', related='product_id.reserved_qty')
    commercial_agreement = fields.Integer('Commercial agreement', compute='_compute_commercial_agreement')

    @api.multi
    def _compute_commercial_agreement(self):
        for line in self:
            if not line.product_id or not line.order_id.pricelist_id:
                line.commercial_agreement = 0.0

            product = line.order_id.pricelist_id.item_ids.filtered(
                lambda x: (x.product_id and x.product_id.id == line.product_id.id) or (x.product_tmpl_id and x.product_tmpl_id.id == line.product_id.product_tmpl_id.id)
            )
            line.commercial_agreement = min(product.mapped('commercial_agreement')) if product and product.mapped('commercial_agreement') else 0.0

    @api.onchange('product_id')
    def product_id_change(self):
        for line in self:
            line._compute_commercial_agreement()
        return super().product_id_change()
