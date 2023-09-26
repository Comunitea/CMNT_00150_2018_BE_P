from odoo import api, fields, models
from odoo.osv import expression

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