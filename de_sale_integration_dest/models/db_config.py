# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,date


class DataMigrtaionConfig(models.Model):
    _name = 'data.migration.config'
    _description = 'Data Migration Configuration'
    _rec_name = 'name_db_2'
    
    
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
        
    
    
    