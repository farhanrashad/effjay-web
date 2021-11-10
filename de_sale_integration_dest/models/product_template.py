# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template in DB Integration Sale'
    
    
    def synch_template_info(self):
        products = self.browse(self.ids)
        
        for product in products:
            if product.source_ref != False:
                
                config_rec = self.env['data.migration.config'].search([], order="id desc", limit=1)
          
                if config_rec:
                    host_name = config_rec.url_db_2
                    database_name = config_rec.name_db_2
                    user_name = config_rec.username_2
                    password = config_rec.password_2
                else:
                    raise UserError('Connection settings not configured!')
                          
                try: 
                    #db 2
                    url_odoo132 = host_name
                    db_odoo132 = database_name
                    user_name_db_odoo132 = user_name
                    password_db_odoo132 = password
                    common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_odoo132))
                    model_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_odoo132))
                    version_db_odoo132 = common_2.version()
                    print('version_db_odoo132---',version_db_odoo132)
                except:
                    raise UserError('Wrong connection setting!')
                  
                #authentication
                odoo_132 = common_2.authenticate(db_odoo132, user_name_db_odoo132,password_db_odoo132, {})
                
                
                
                
                db1_product_id = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.template','search_read',
                                                    [[['id','=',product.source_ref]]],
                                                    {'fields': ['id', 'default_code', 'barcode'], 'limit': 1})

                print('----db1_product_id2----',db1_product_id)
                if db1_product_id != []:
                    if db1_product_id[0]:
                        if db1_product_id[0].get('default_code'):
                            product.default_code = db1_product_id[0].get('default_code')
#                             product.barcode = db1_product_id[0].get('barcode')
    
    
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Product Template ID from destination db.')

    
          
