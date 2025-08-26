{
    'name': 'Custom Sales Report',
    'version': '1.0',
    'description': '',
    'summary': '',
    'author': 'Nasreldin Omer',
    'website': 'nasrom9@gmail.com',
    'license': 'LGPL-3',
    'category': '',
    'depends': [
        'sale', 'report_xlsx', 'account', 'purchase'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/action_report_custom_sales.xml',
        'wizard/custom_sale_report_wizard.xml',
        
    ],
    
    'auto_install': False,
    'application': False,
}