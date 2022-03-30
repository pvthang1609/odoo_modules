from odoo import models, fields, api, _

class Currency(models.Model):
    _name = "currency"
    _description = "Đơn vị tiền tệ"

    name = fields.Char(string="Tên")
    current_exchange_rate = fields.Float(string='Tỷ giá hiện tại')
