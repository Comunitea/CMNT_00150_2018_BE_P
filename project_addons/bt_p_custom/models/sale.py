from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _onchange_product_id_check_availability(self):
        return super(SaleOrderLine, self.with_context(skip_stock=True))._onchange_product_id_check_availability()
