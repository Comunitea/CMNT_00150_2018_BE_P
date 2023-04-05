from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderFromLead(models.TransientModel):
    _name = 'sale.order.from.lead'

    lead_id = fields.Many2one('crm.lead',string="Leads")
    lead_line_ids = fields.One2many(
        comodel_name='sale.order.from.lead.line',
        inverse_name='lead_id',
        string='Lead Lines',
        readonly=False,
    )

    @api.model
    def default_get(self, default_fields):
        model = self._context.get('active_model')
        active_ids = self._context.get('active_ids')
        lead = self.env[model].browse(active_ids)
        res = super().default_get(default_fields)
        if lead:
            res['lead_id'] = lead[0].id
            if 'lead_line_ids' in lead[0]:
                lines = []
                for line in lead[0]['lead_line_ids']:
                    lines.append((0, 0, {
                        'lead_id':lead[0].id,
                        'name': line.name,
                        'product_id': line.product_id.id,
                        'product_qty': line.product_qty,
                        'price_unit': line.price_unit,
                        # 'discount':
                        }))
                res['lead_line_ids']=lines
        return res

    def create_sale_order(self):
        self.ensure_one()
        so_lines =[(0, 0, {
            'name': l.name,
            'product_id': l.product_id.id,
            'product_uom_qty': l.product_qty,
            'price_unit': l.price_unit,
            # 'discount':l.discount
        }) for l in self.lead_line_ids.
                    filtered(lambda x: x.product_qty > 0)]
        so = self.env['sale.order'].create({
            'partner_id': self.lead_id.partner_id.id,
            'team_id': self.lead_id.team_id.id,
            'campaign_id': self.lead_id.campaign_id.id,
            'medium_id': self.lead_id.medium_id.id,
            'source_id': self.lead_id.source_id.id,
            'opportunity_id':self.lead_id.id,
            'order_line': so_lines,
            'validity_date': self.lead_id.validity_date
        })
        action = self.env.ref(
            'sale.action_quotations')
        form = self.env.ref('sale.view_order_form')
        action = action.read()[0]
        action['views'] = [(form.id, 'form')]
        action['res_id'] = so.id
        return action

class SaleOrderFromLeadLine(models.TransientModel):
    _name = 'sale.order.from.lead.line'

    lead_id = fields.Many2one('sale.order.from.lead')
    name = fields.Char('Name')
    product_id = fields.Many2one('product.product',string='Product')
    product_qty = fields.Float('Quantity')
    price_unit = fields.Float('Price Unit')
    # discount = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.name = self.product_id.name
        self.product_qty = 0
        self.price_unit = self.product_id.lst_price
