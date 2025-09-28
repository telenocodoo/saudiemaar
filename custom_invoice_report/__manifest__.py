{
    'name': 'Custom Invoice | PDF',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Nasereldin Omer',
    'website': 'nasrom9@gmail.com',
    'license': 'LGPL-3',
    'category': 'Accounting',
    'depends': [
        'account', 'l10n_sa', 'l10n_sa_edi', 'hr'
    ],
    'data': [
        'report/invoice_report.xml',
        'views/res_partner.xml',
        'views/hr_employee_views.xml',
    ],
    'auto_install': False,
    'application': False,

}