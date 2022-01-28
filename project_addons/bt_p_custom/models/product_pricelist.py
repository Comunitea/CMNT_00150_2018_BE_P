# © 2022 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"
    name = fields.Char(store=True)
    price = fields.Char(store=True)

    @api.one
    @api.depends(
        'categ_id', 'product_tmpl_id', 'product_id', 'compute_price',
        'fixed_price', 'pricelist_id', 'percent_price', 'price_discount',
        'price_surcharge')
    def _get_pricelist_item_name_price(self):
        if self.categ_id:
            self.name = _("Category: %s") % (self.categ_id.name)
        elif self.product_tmpl_id:
            self.name = self.product_tmpl_id.display_name
        elif self.product_id:
            self.name = self.product_id.display_name
        else:
            self.name = _("All Products")

        if self.compute_price == 'fixed':
            self.price = ("%s %s") % (self.fixed_price, self.pricelist_id.currency_id.name)
        elif self.compute_price == 'percentage':
            self.price = _("%s %% discount") % (self.percent_price)
        else:
            self.price = _("%s %% discount and %s surcharge") % (self.price_discount, self.price_surcharge)
