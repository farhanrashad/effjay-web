# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking in DB Integration Sale'
    
    
    @api.constrains('transition_state')
    def _check_transition_state(self):
        for order in self:
            if order.transition_state == 'assigned':
                order.action_assign()
            if order.transition_state == 'cancel':
                order.action_cancel()
    
                
    transition_state = fields.Selection([('draft', 'Draft'),('waiting', 'Waiting'),
                                     ('confirmed', 'Confirmed'),('assigned', 'Assigned'), 
                                     ('done', 'Done'),('cancel', 'Cancelled'),])
    