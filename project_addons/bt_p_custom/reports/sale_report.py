# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    tag_ids = fields.Many2many('crm.lead.tag', 'sale_order_tag_rel', 'order_id', 'tag_id', string='Tags')
    sale_type = fields.Selection([
        ('stock', 'STOCK'),
        ('lote', 'LOTE')
    ], string='Sale type', default="stock")

    def _select(self):
        return super(SaleReport, self)._select() + """,
            s.sale_type as sale_type"""
    
    def _group_by(self):
        return super(SaleReport, self)._group_by() + """,
            s.sale_type"""