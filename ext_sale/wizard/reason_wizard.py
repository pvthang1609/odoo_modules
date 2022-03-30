# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class ReasonWizard(models.TransientModel):
    _name = "sale.order.reason.wizard"
    _description = "Lý do hủy"

    content = fields.Text(string='Nội dung')

    def update(self):
        id = self.env.context['active_id']
        sale_order = self.env["sale.order"].browse(id)
        new_data = {}
        if self.content:
            new_data["reason"] = self.content

        sale_order.write(new_data)