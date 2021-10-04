# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ProductCategory(models.Model):
    _inherit = 'product.category'
    _description = 'Product Category in DB Integration Sale'
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Category ID from destination db.')
    
    
    
class ProductAttribute(models.Model):
    _inherit = 'product.attribute'
    _description = 'Product Attribute in DB Integration Sale'
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Product Attribute ID from destination db.')
    

    
class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'
    _description = 'Product Attribute Value in DB Integration Sale'
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Product Attribute Value ID from destination db.')
    