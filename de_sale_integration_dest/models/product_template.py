# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ProductTemplateInh(models.Model):
    _inherit = 'product.template'
    _description = 'Product Template in DB Integration Sale'
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Product Template ID from destination db.')

        
          
