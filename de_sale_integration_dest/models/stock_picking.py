# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockQuantInh(models.Model):
    _inherit = 'stock.quant'


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'
    _description = 'Stock Picking in DB Integration Sale'
    
    
    @api.constrains('transition_state')
    def _check_transition_state(self):
        for order in self:
            if order.transition_state == 'assigned':
                order.action_assign()
            if order.transition_state == 'done':
                order.button_validate()
            if order.transition_state == 'cancel':
                order.action_cancel()
                
    
    
    def button_validate(self):
        if self.state != 'done':
            if self.move_ids_without_package:
                for move in self.move_ids_without_package:
                    move.quantity_done = move.product_uom_qty
        res = super(StockPickingInh,self).button_validate()
        return res
    
                
    transition_state = fields.Selection([('draft', 'Draft'),('waiting', 'Waiting'),
                                     ('confirmed', 'Confirmed'),('assigned', 'Assigned'), 
                                     ('done', 'Done'),('cancel', 'Cancelled'),])
    