from odoo import api, fields, models


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

