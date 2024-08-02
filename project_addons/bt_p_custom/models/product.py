from odoo import api, fields, models
from odoo.osv import expression

class Product(models.Model):
    _inherit = 'product.template'

    reserved_qty = fields.Float('Reserved qty', compute='_compute_reserved_qty')
    pvp_stock = fields.Float('PVP stock', digits=(16, 2))
    pvp_lote = fields.Float('PVP lote', digits=(16, 2))
    pvp_stock_min_qty = fields.Float('PVP stock min. qty')
    pvp_lote_min_qty = fields.Float('PVP lote min. qty')
    shelf_life = fields.Integer('Shelf life (months)')
    palet_size = fields.Text('Palet size')

    @api.multi
    def _compute_reserved_qty(self):
        for template in self:
            stock_quants = self.env['stock.quant'].search([
                ('product_tmpl_id', '=', template.id),
                ('quantity', '>', 0)
            ])
            template.reserved_qty = sum(quant.reserved_quantity for quant in stock_quants) or 0.0

class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('product_pricelist'):
            pricelist_id = self._context.get('pricelist')
            pricelist = self.with_context(product_pricelist = False).env['product.pricelist'].browse(pricelist_id)
            products = pricelist.mapped('item_ids.product_tmpl_id.product_variant_ids')
            products += pricelist.mapped('item_ids.product_id')

            args = expression.AND([args,[('id', 'in', products._ids)]])
        res = super(Product,self)._search(args, offset=0, limit=None, order=None, count=False, access_rights_uid=None)

        return res

    @api.multi
    def _compute_reserved_qty(self):
        for product in self:
            stock_quants = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('quantity', '>', 0)
            ])
            product.reserved_qty = sum(quant.reserved_quantity for quant in stock_quants)
