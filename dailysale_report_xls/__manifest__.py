# -*- coding: utf-8 -*-
{
    'name': 'Daily Sale Report XLS',
    'summary': 'Generate XLS report for daily sale',
    'version': '12.0.1.0.0',
    'category': 'Sales',
    'website': 'https://www.blogger.com/profile/14877879550922602186',
    'author': 'A',
    'maintainer': 'A',
    'installable': True,
    'depends': [
        'base',
        'sale',
        'sale_management',
        'report_xlsx',
    ],
    'data': [
        'report/templates.xml',
        'wizard/dailysale_xls_wizard.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
