# -*- coding: utf-8 -*-
from odoo import models, fields


class HMSaleOrder(models.Model):
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[
        ('had_technical_drawings', 'Có bản vẽ'),
        ('sample_production', 'Sản xuất mẫu'),
        ('send_samples', 'Gửi mẫu'),
    ])

    def action_change_state_had_technical_drawings(self):
        for record in self:
            record.write({
                'state': 'had_technical_drawings'
            })

    def action_change_state_sample_production(self):
        for record in self:
            record.write({
                'state': 'sample_production'
            })

    def action_change_state_send_samples(self):
        for record in self:
            record.write({
                'state': 'send_samples'
            })
