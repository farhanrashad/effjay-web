# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product in DB Integration Sale'
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Product ID from source db.')
    