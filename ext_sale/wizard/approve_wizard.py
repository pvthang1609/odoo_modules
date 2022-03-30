# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class ApproveWizard(models.TransientModel):
    _name = "sale.order.line.approve.wizard"
    _description = "Phân công cho NV XNK"

    ei_executive_ids = fields.Many2many('res.users', string='NV XNK')

    def multi_update(self):
        ids = self.env.context['active_ids']  # selected record ids
        sale_order_lines = self.env["sale.order.line"].browse(ids)
        new_data = {}

        if self.ei_executive_ids:
            new_data["ei_executive_ids"] = self.ei_executive_ids

        sale_order_lines.write(new_data)
