from odoo import models, fields, api


class AskInfoProductLine(models.Model):
    _name = "askinfo.product.line"
    _description = "Thông tin chào bán từ các nhà cung cấp"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    askinfo_product_id = fields.Many2one("askinfo.product", string="ID sản phẩm chào bán")
    delivery_time = fields.Char(string='Thời gian giao hàng')
    state = fields.Selection([('b', 'Đã mua'), ('s', 'Đã chọn'), ('ns', 'Chưa chọn')], string="Trạng thái")
    customer_id = fields.Many2one('res.partner', string="Khách hàng", compute="_compute_customer_id")

    partner_id = fields.Many2one('res.partner', string="Nhà cung cấp")
    common_name = fields.Char(string="Tên sản phẩm")
    product_id = fields.Many2one("product.product", string="Model sản phẩm")
    quantily = fields.Integer(string="Số lượng")
    product_origin = fields.Char(string="Xuất xứ")
    manufacturer = fields.Char(string="Nhà sản xuất")
    description = fields.Text(string="Mô tả")
    attachment_ids = fields.Many2many('ir.attachment', string='File đính kèm')

    price = fields.Float(string="Đơn giá")
    unit_currency = fields.Many2one("currency", string="ĐV tiền tệ", required=True)
    exchange_rate = fields.Float(string='Tỷ giá', required=True, store=True, readonly=False,
                                 compute="_compute_exchange_rate")
    price_vnd = fields.Float(string="Đơn giá(VNĐ)", readonly=True, compute="_compute_price_vnd")
    total = fields.Float(string="Tổng giá trị", readonly=True, compute="_compute_total")

    note = fields.Text(string="Ghi chú")

    @api.depends('unit_currency')
    def _compute_exchange_rate(self):
        for line in self:
            line.exchange_rate = line.unit_currency.current_exchange_rate
        return True

    @api.depends('exchange_rate', 'price', 'quantily')
    def _compute_price_vnd(self):
        for line in self:
            line.price_vnd = line.price * line.exchange_rate
        return True

    @api.depends('quantily', 'price_vnd', 'exchange_rate')
    def _compute_total(self):
        for line in self:
            line.total = line.price_vnd * line.quantily
        return True

    @api.depends('askinfo_product_id')
    def _compute_customer_id(self):
        for line in self:
            line.customer_id = line.askinfo_product_id.customer_id
        return True

    @api.depends('partner_id', 'product_id', 'price')
    def name_get(self):
        res = []
        for record in self:
            if record.partner_id.name and record.product_id.name and record.price:
                res.append((record.id, "%s - %s - %s" % (record.partner_id.name, record.product_id.name, record.price)))
        return res
