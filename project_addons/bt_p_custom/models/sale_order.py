# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    ready_to_send = fields.Boolean('Ready to send', default=False)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    qty_available = fields.Float('Qty available', related='product_id.qty_available')
    virtual_available = fields.Float('Virtual available', related='product_id.virtual_available')
    reserved_qty = fields.Float('Reserved qty', related='product_id.reserved_qty')
    pricelist_qty = fields.Float('Pricelist qty', compute='_compute_pricelist_qty')

    @api.multi
    def _compute_pricelist_qty(self):
        for line in self:
            if not line.product_id or not line.order_id.pricelist_id:
                line.pricelist_qty = 0.0
            
            product = line.order_id.pricelist_id.item_ids.filtered(
                lambda x: (x.product_id and x.product_id.id == line.product_id.id) or (x.product_tmpl_id and x.product_tmpl_id.id == line.product_id.product_tmpl_id.id)
            )
            line.pricelist_qty = min(product.mapped('min_quantity')) if product and product.mapped('min_quantity') else 0.0
    
    @api.onchange('product_id')
    def product_id_change(self):
        for line in self:
            line._compute_pricelist_qty()
        return super().product_id_change()