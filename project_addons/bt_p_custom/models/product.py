from odoo import api, fields, models
from odoo.osv import expression

class Product(models.Model):
    _inherit = 'product.product'

    def _compute_quantities(self):
        res = super()._compute_quantities()
        if self._context.get('skip_stock'):
            for product in self:
                product.qty_available = 9999999999
                product.incoming_qty = 9999999999
                product.outgoing_qty = 0
                product.virtual_available = 999999999
        return res

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