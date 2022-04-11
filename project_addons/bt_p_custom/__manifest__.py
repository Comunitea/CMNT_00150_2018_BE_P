# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'BT customizations',
    'summary': '',
    'version': '11.0.1.0.0',
    'category': 'Uncategorized',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'product',
        'purchase',
        'sale_order_lot_selection',
        'sale_stock_picking_note'
    ],
    'data': [
        'views/product_view.xml',
        'views/sale.xml',
        'views/account_invoice.xml',
        'views/report_saleorder.xml',
        'views/res_partner.xml',
        'views/stock.xml',
    ],
}
