{
    'name': 'Custom Sales Module',
    'version': '1.0',
    'depends': ['sale', 'product', 'contacts', 'purchase', 'account'],  
    'data': [
        'views/sales_person_form.xml',
        'views/product_views.xml',
        'views/product_slug_name.xml',
        'views/contact_filter.xml',
        "views/purchase_vendor.xml",
        "views/custom_settings.xml",
        "views/invoice_views.xml",
    ],
    'installable': True,
    'application': True,
}
