{
    'name': 'UD Custom CRM',
    'summary': '',
    'version': '11.0.1.0.0',
    'category': 'Uncategorized',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'crm_lead_product',
        'sale_crm'
    ],
    'data': [
        'reports/crm_lead_templates.xml',
        'reports/crm_report.xml',
        'wizard/sale_order_from_lead_view.xml',
        'views/crm_lead_views.xml',
    ],
}
