from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _onchange_product_id_check_availability(self):
        context = self._context
        if context:
            context = dict(context)
        else:
            context = {}
        context['skip_stock'] = True
        res = super()._onchange_product_id_check_availability()
        return res