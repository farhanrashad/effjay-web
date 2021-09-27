# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import xmlrpc.client
import psycopg2
from odoo.exceptions import UserError
import json


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Partner in DB Integration Sale'
    
    
    source_ref = fields.Char(string='Source Ref', help='To store actual Partner ID from source db.')
    