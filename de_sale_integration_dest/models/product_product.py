# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product in DB Integration Sale'
    
    
    def auto_archive_product(self):
        products = self.search([('barcode','=',False),('active','=', True)])
        
        for product in products:
            product.active = False
            
        products = self.search([('barcode','!=',False),('active','=', False)])
        
        for product in products:
            product.active = True
    
           
    
    def synch_product_info(self):
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
             
                
        products = self.browse(self.ids)
        
        for product in products:
            if product.match_pattern != False:
                db1_product_id = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.product','search_read',
                                                    [[['match_pattern','=',product.match_pattern]]],
                                                    {'fields': ['id', 'default_code', 'barcode'], 'limit': 1})

                print('----db1_product_id2----',db1_product_id)
                if db1_product_id != []:
                    if db1_product_id[0]:
                        if db1_product_id[0].get('id'):
                            product.source_ref = db1_product_id[0].get('id')
                            product.default_code = db1_product_id[0].get('default_code')
                            if db1_product_id[0].get('barcode') != '':
                                product.barcode = db1_product_id[0].get('barcode')
            
            
    def update_pattern(self):
        for record in self.browse(self.ids):
            record.compute_matching_pattern()
            
    
    @api.depends('product_tmpl_id')
    def compute_matching_pattern(self):
        for rec in self:
            ids = ''
            
            if rec.product_tmpl_id.source_ref:
                print('**************************************')
                print('-----rec.product_template_attribute_value_ids-----',rec.product_template_attribute_value_ids)
                if rec.product_template_attribute_value_ids:
                    for line in rec.product_template_attribute_value_ids:
                        print('---line---',line.attribute_id.id)
                        print('---line---',line.product_attribute_value_id.id)
                        if line.attribute_id.source_ref != False:
                            ids = ids + str(line.attribute_id.source_ref)
                        if line.product_attribute_value_id.source_ref != False:
                            ids = ids + str(line.product_attribute_value_id.source_ref)
                        
                        print('------ids---',ids)
    
#                     ids = sorted([i for i in str(ids)], reverse=False)
#                     ids = str("".join(ids))
                rec.match_pattern = int(str(rec.product_tmpl_id.source_ref) + ids)
            else:
                rec.match_pattern = None
            
            print('match_pattern---',rec.match_pattern)
            

    
    match_pattern = fields.Char(string='Match Pattern', compute='compute_matching_pattern', store=True)
    source_ref = fields.Char(string='Source Ref', help='To store actual Product ID from source db.')
    