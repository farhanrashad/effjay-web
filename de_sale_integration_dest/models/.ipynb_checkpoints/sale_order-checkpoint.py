# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class SaleOrderInh(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale in DB Integration Sale'
    
    
    is_migrated = fields.Boolean(string='Is Migrated Successfully', default=False)
    transition_state = fields.Selection([('draft', 'Quotation'),('sent', 'Quotation Sent'),
                                     ('sale', 'Sales Order'),('done', 'Locked'),('cancel', 'Cancelled'),])
    
    
#     def action_confirm(self):
#         imediate_obj = self.env['stock.immediate.transfer']
#         res = super(SaleOrderInh,self).action_confirm()
            
#         for order in self:
#             for picking in self.picking_ids:
#                 picking.action_confirm()
#                 picking.action_assign()


#                 imediate_rec = imediate_obj.create({'pick_ids': [(4, order.picking_ids.id)]})
#                 imediate_rec.process()
#                 if picking.state !='done':
#                     for move in picking.move_ids_without_package:
#                         move.quantity_done = move.product_uom_qty
#                     picking.button_validate()

#         self._cr.commit()
    
    
    
    
    
    
    
    
    @api.constrains('transition_state')
    def _check_transition_state(self):
        for order in self:
            if order.transition_state == 'draft':
                order.action_draft()
            if order.transition_state == 'sale':
                order.action_confirm()
            if order.transition_state == 'cancel':
                order.action_cancel()
                
    
    def auto_migrate_sale_orders(self):
        orders = self.search([('is_migrated','=',False)])
        for order in orders:
            order.transfer_db_data()
    
    
    def check_partner(self, model_2, db_odoo132, odoo_132, password_db_odoo132, name):
        exists = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'res.partner', 'search', [[['name', '=', name]]])
         
        if exists == []:
            exists = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'res.partner', 'create', [[{'name': name}]])
    
        return exists[0]
    
    
    def check_tax(self, model_2, db_odoo132, odoo_132, password_db_odoo132, name):
        exists = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'account.tax', 'search', [[['name', '=', name]]])
           
        if exists == []:
            raise UserError('Tax by name of ('+str(name)+') is not available! \n Please create before proceeding.')
      
        return [exists[0]]


    def check_product(self, model_2, db_odoo132, odoo_132, password_db_odoo132, name):
        exists = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.product', 'search', [[['name', '=', name]]])
         
        if exists == []:
#             exists = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'product.product', 'create', [[{'name': name}]])
            raise UserError('Product by name of ('+str(name)+') is not available! \n Please create before proceeding.')
    
        return exists[0]
    
    
    def just_verify_sale_data(self, model_2, db_odoo132, odoo_132, password_db_odoo132):
        partner_id = self.check_partner(model_2, db_odoo132, odoo_132, password_db_odoo132, self.partner_id.name)
        
        if self.order_line:
            for line in self.order_line:
                product_id = self.check_product(model_2, db_odoo132, odoo_132, password_db_odoo132, line.product_id.name)

                if line.tax_id: 
                    tax_id = self.check_tax(model_2, db_odoo132, odoo_132, password_db_odoo132, line.tax_id.name)
                else:
                    tax_id = []
                    
                    
        
    def transfer_db_data(self):
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
         
         
         
#         self.just_verify_sale_data(model_2, db_odoo132, odoo_132, password_db_odoo132)
#         partner_id = self.check_partner(model_2, db_odoo132, odoo_132, password_db_odoo132, self.partner_id.name)
        if self.partner_id.source_ref:
            sale_vals = {
                'partner_id': int(self.partner_id.source_ref),
                'old_db_ref': self.name,
                'migration_state': self.state,
                }
              
            sale_order = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'sale.order', 'create', [[sale_vals]])
            print('sale_order--',sale_order)
            
            
            if self.order_line:
                for line in self.order_line:
    #                 product_id = self.check_product(model_2, db_odoo132, odoo_132, password_db_odoo132, line.product_id.name)
    
                    if line.tax_id: 
                        tax_id = self.check_tax(model_2, db_odoo132, odoo_132, password_db_odoo132, line.tax_id.name)
                    else:
                        tax_id = []
                    
                    
                    line_vals = {
                        'product_id': int(line.product_id.source_ref),
                        'name': line.name,
                        'product_uom_qty': line.product_uom_qty,  
                        'price_unit': line.price_unit,
                        'discount': line.discount,
                        'tax_id': tax_id,
                        'order_id': sale_order[0],
                    }
                
                    sale_order_line = model_2.execute_kw(db_odoo132, odoo_132, password_db_odoo132,'sale.order.line', 'create', [[line_vals]])
                    print('sale_order_line--',sale_order_line)
            self.is_migrated = True
          
