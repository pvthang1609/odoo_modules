from odoo import models, fields


class AskInfoProduct(models.Model):
    _name = "askinfo.product"
    _description = "Sản phẩm hỏi hàng"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    askinfo_product_line_ids = fields.One2many('askinfo.product.line', "askinfo_product_id", string="Thông tin chào bán từ các NCC")
    customer_id = fields.Many2one('res.partner', string="Khách hàng")

    common_name = fields.Char(string="Tên sản phẩm")
    product_id = fields.Many2one("product.product", string="Model sản phẩm")
    quantily = fields.Integer(string="Số lượng")
    product_origin = fields.Char(string="Xuất xứ yêu cầu")
    manufacturer = fields.Char(string="Nhà sản xuất yêu cầu")
    description = fields.Text(string="Mô tả")
    attachment_ids = fields.Many2many('ir.attachment', string='File đính kèm')

    price = fields.Float(string="Giá bán (KH)")
    purchase_price = fields.Float(string="Giá mua")
    local_price = fields.Float(string="Giá bán nội bộ")

    price_target = fields.Float(string="Giá bán mục tiêu (KH)")
    purchase_price_target = fields.Float(string="Giá mua mục tiêu")
    local_price_target = fields.Float(string="Giá bán nội bộ mục tiêu")

    note = fields.Text(string="Ghi chú")
    selected_askinfo_product_line = fields.Many2one('askinfo.product.line', string="Lựa chọn mua hàng")
    ei_executive_ids = fields.Many2many('res.users', string='NV XNK')
    state = fields.Selection([('cancel', 'Hủy'),
                              ('draft', 'Nháp'),
                              ('sent_sale_manager', 'Đã gửi TPKD'),

                              ('reject_draft', 'Từ chối [TPKD]'),
                              ('sent_ei_manager', 'Đã gửi QLXNK'),

                              ('reject_assign', 'Từ chối [TPXNK]'),
                              ('assigned', 'Đã phân công'),

                              ('had_price_to_partner', 'Có giá từ NCC'),
                              ('had_local_price', 'Có giá bán nội bộ'),

                              ('reject_local_price', 'Từ chối GBNB'),
                              ('confirmed_local_price', 'Đã xác nhận GBNB'),

                              ('had_price', 'Có giá bán (KH)'),

                              ('reject_price', 'Từ chối giá bán (KH)'),
                              ('confirmed_price', 'TPKD đã duyệt'),

                               ('manager_reject', 'Từ chối [BGĐ]'),
                              ('manager_confirmed', 'BGĐ đã duyệt'),
                              # TODO: state phải khác
                              ('sent', 'Đã gửi'),
                              ('had_local_price_target', 'Có GBNBMT'),
                              ('confirmed_local_price_target', 'Đã duyệt GBNBMT'),
                              ('had_purchase_price_target', 'Có giá mua mục tiêu'),
                              ('sale', 'Đã đề xuât'),
                              ('processing', 'Đang thực hiện'),
                              ('done', 'Hoàn thành')], string="Trạng thái")

    def action_print(self):
        print('is run')
