{
    'name': 'Custom Sales Module',
    'version': '1.0',
    'depends': ['sale', 'product'],  # ensure 'product' is listed
    'data': [
        'views/sales_person_form.xml',
        'views/product_views.xml',
        'views/product_slug_name.xml'  # this should contain the filter extension
    ],
    'installable': True,
    'application': True,
}
