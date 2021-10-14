# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,date
import xmlrpc.client



class DataMigrtaionConfig(models.Model):
    _name = 'data.migration.config'
    _description = 'Data Migration Configuration'
    _rec_name = 'name_db_2'
    
    
    """-------------------cron jobs start----------------------"""
    def auto_synch_product_ids(self):
        self.search([], order="id desc", limit=1).get_product_ids()
    
    
    def get_authenticate(self):
        host_name = self.url_db_2
        database_name = self.name_db_2
        user_name = self.username_2
        password = self.password_2

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
        return [model_2, db_odoo132, user_name_db_odoo132, password_db_odoo132, odoo_132]
    
    
    
    def get_product_ids(self):
        model_2 = self.get_authenticate()[0]
        db_odoo132 = self.get_authenticate()[1]
        user_name_db_odoo132 = self.get_authenticate()[2]
        password_db_odoo132 = self.get_authenticate()[3]
        odoo_132 = self.get_authenticate()[4]
        
        products = self.env['product.product'].search([('source_ref','=',False)], order="id desc", limit=300)
        
        if products:
            for product in products:
                print('product.match_pattern------',product.match_pattern)#Juice,2-3
                
                db1_product_id = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.product', 'search', [[['match_pattern','=',product.match_pattern]]])
                print('----db1_product_id----',db1_product_id)
                
                if db1_product_id != []:
                    db1_product_id = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.product','search_read',
                                                        [[['id','=',db1_product_id[0]]]],
                                                        {'fields': ['id', 'default_code', 'barcode'], 'limit': 1})
    
                    print('----db1_product_id2----',db1_product_id)
                    if db1_product_id != []:
                        if db1_product_id[0]:
                            if db1_product_id[0].get('id'):
                                product.source_ref = db1_product_id[0].get('id')
                            if db1_product_id[0].get('barcode'):
                                product.default_code = db1_product_id[0].get('barcode')
                                
                                barcode_exists = self.env['product.product'].search([('barcode','=',db1_product_id[0].get('barcode'))], order="id desc", limit=1)
                                
                                """for same barcode message"""
#                                 if barcode_exists:
#                                     raise UserError('Same barcode exists as '+(barcode_exists.barcode))
                                if not barcode_exists:
                                    product.barcode = db1_product_id[0].get('barcode')
                                
#                             if db1_product_id[0].get('default_code'):
#                                 product.default_code = db1_product_id[0].get('default_code')
        
        products = self.env['product.product'].search([('source_ref','=',False),('barcode','!=',False)], order="id desc", limit=30)
        print('products---- here',products)
        if products:
            for product in products:
                print('product------',product.name)
                db1_product_id = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.product','search_read',
                                                        [[['barcode','=',product.barcode]]],
                                                        {'fields': ['id'], 'limit': 1})
    
                print('----db1_product_id2----',db1_product_id)
                if db1_product_id != []:
                    if db1_product_id[0]:
                        if db1_product_id[0].get('id'):
                            product.source_ref = db1_product_id[0].get('id')
    
    
    @api.model
    def create(self, vals):
        exists = self.search([])
        
        if exists:
            raise UserError(('Configuration Already Exists!'))
        else:
            pass
           
        rec = super(DataMigrtaionConfig, self).create(vals)
        return rec
    
    
    url_db_2 = fields.Char(string='URL', required=True, help='Odoo access link / URL.')
    name_db_2 = fields.Char(string="Database Name", required=True, help='Database name on login screen of odoo.')
    username_2 = fields.Char(string='Username', required=True, help='Login username to odoo.')
    password_2 = fields.Char(string='Password', required=True, help='Login password to odoo.')    
#     company_2 = fields.Char(string='Company', required=True, help='Copy paste company name from the DB, where you need to send data.')
        
    
    
    