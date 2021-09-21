# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Data Migration Odoo 13 (Destination)",
    "category": 'Sale',
    "summary": 'Only Sales Order with customer and products Data',
    "description": """
	 
   
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    "version": '13.1.0.0',
    "depends": ['base','sale','stock','contacts'],
    "data": [
        'data/data.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/db_config_view.xml',
        'views/sale_order_view.xml',
        'views/product_product_view.xml',
        'views/res_partner_view.xml',
        'views/product_category_view.xml',
        'views/product_template_view.xml',
    ],
    
    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
