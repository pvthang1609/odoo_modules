# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools


class Partner(models.Model):
    _inherit = 'res.partner'

    rate = fields.Selection([('5', "5 sao"),
                             ('4', "4 sao"),
                             ('3', "3 sao"),
                             ('2', "2 sao"),
                             ('1', "1 sao")], string="Đánh giá", help="Đánh giá dựa trên số đơn hàng đúng hạn")