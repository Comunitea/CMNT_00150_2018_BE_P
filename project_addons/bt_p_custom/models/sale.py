from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _onchange_product_id_check_availability(self):
        return super(SaleOrderLine, self.with_context(skip_stock=True))._onchange_product_id_check_availability()

    @api.model
    def _check_move_state(self):
        """
            Al no reservar al momento de confirmar la venta,
            sobreescribimos la función para que no falle.
        """
        return True
