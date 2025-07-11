{   

    'name': 'My First Module',
    'version': '1.0',
    'author': 'Dipak',
    'category': 'Tools',
    'summary': 'A simple custom module for CRUD operations',
    'depends': ['base', 'mail', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/list_view.xml',
        'views/cart_views.xml',
        'views/students_views.xml',
        'views/email_template.xml'
    ],
    'installable': True,
    'application': True,
}
