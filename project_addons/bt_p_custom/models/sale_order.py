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