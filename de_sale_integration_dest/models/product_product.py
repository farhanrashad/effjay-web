# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _description = 'Product in DB Integration Sale'
    
    
    @api.depends('product_tmpl_id')
    def compute_matching_pattern(self):
        for rec in self:
            ids = ''
            
            if rec.product_tmpl_id.source_ref:
                if rec.product_template_attribute_value_ids:
                    for line in rec.product_template_attribute_value_ids:
                        print('---line---',line.attribute_id.id)
                        print('---line---',line.product_attribute_value_id.id)
                        ids = ids + str(line.attribute_id.source_ref)
                        ids = ids + str(line.product_attribute_value_id.source_ref)
                        print('------ids---',ids)
    
                    ids = sorted([i for i in str(ids)], reverse=False)
                    ids = str("".join(ids))
                rec.match_pattern = int(str(rec.product_tmpl_id.source_ref) + ids)
            else:
                rec.match_pattern = None
            

    
    match_pattern = fields.Char(string='Match Pattern', compute='compute_matching_pattern', store=True)
    source_ref = fields.Char(string='Source Ref', help='To store actual Product ID from source db.')
    