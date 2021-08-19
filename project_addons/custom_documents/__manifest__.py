# © 2021 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Document customizations',
    'version': '12.0.1.0.0',
    'author': 'comunitea',
    'website': 'www.comunitea.com',
    'license': 'AGPL-3',
    'depends': [
        'report_intrastat',
        'account_payment_partner',
        'account_invoice_report_due_list'
    ],
    'data': [
        'views/report_invoice.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

