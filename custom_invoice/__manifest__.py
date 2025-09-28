{
    'name': 'Custom Invoice Print',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Nasreldin Omar',
    'website': 'nasrom9@gmail.com',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'account_accountant'
    ],
    'data': [
       'report/custom_invoice_report.xml',
       'report/custom_invoice_report_template.xml',
    ],
    
    'auto_install': False,
    'application': False,
}