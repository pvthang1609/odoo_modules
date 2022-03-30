from odoo import fields, models, api, _
from vnsolution.tool import create_notification_sticker


class ExtSalePriceListProduct(models.Model):
    _name = "sale.order.price.list.product"
    _description = "Bảng giá"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Chung
    name = fields.Char(string='Mã số', required=True, readonly=True, default=lambda self: _('New'))
    state = fields.Selection([
        ('processing', 'Trong quá trình'),
        ('selected', 'Đã chọn giá'),
        ('buyed', 'Đã mua'),
    ], string='Trạng thái',  default='processing', readonly=True)
    origin = fields.Many2one("sale.order", string="Yêu cầu hỏi hàng", required=True)
    price_lines = fields.One2many("sale.order.price.line", "price_list_product_id", string="Chi tiết bảng giá")
    ei_executive_ids = fields.Many2many('res.users', string="NV XNK")
    is_sent_notify = fields.Boolean(default=False, readonly=True)
    count_price_lines = fields.Integer(string="Tổng NCC", readonly=True, compute='_compute_count_price_lines')

    # Yêu cầu
    origin_common_name = fields.Char(string="Tên yêu cầu", readonly=True)
    origin_product_id = fields.Many2one("product.product", string="Model yêu cầu")
    origin_description = fields.Text(string="Mô tả yêu cầu", readonly=True)
    origin_attachments = fields.Binary(string="File đính kèm yêu cầu", attachment=True, readonly=True)
    origin_product_origin = fields.Char(string="Xuất xứ yêu cầu", readonly=True)
    origin_manufacturer = fields.Char(string="Nhà SX yêu cầu", readonly=True)

    standard_price_target = fields.Float(string="Giá nhập mục tiêu", readonly=True)

    # Chào bán
    selected_common_name = fields.Char(string="Tên chào bán", readonly=True, compute='_compute_selected_common_name')
    selected_product_id = fields.Many2one("product.product", string="Model chào bán", readonly=True, compute='_compute_selected_product_id')
    selected_description = fields.Text(string="Mô tả chào bán", readonly=True, compute='_compute_selected_description')
    selected_attachments = fields.Binary(string="File đính kèm chào bán", attachment=True, readonly=True, compute='_compute_selected_attachments')
    selected_product_origin = fields.Char(string="Xuất xứ chào bán", default="Chưa chọn", readonly=True, compute='_compute_selected_product_origin')
    selected_manufacturer = fields.Char(string="Nhà sản xuất chào bán", default="Chưa chọn", readonly=True, compute='_compute_selected_manufacturer')

    selected_price = fields.Float(string="Giá mua", readonly=True, compute='_compute_selected_price')
    selected_partner = fields.Many2one('res.partner',string="NCC mua hàng", readonly=True, compute='_compute_selected_partner', store=True)
    selected_price_lines = fields.Many2one("sale.order.price.line", string="Chi tiết bảng giá lựa chọn")
    note = fields.Text(string="Ghi chú", compute='_compute_note')
    other_costs = fields.Float(string="Chi phí khác", readonly=True, compute='_compute_other_costs')

    @staticmethod
    def price_line_has_state_selected(price_line):
        if price_line.state == "selected":
            return True
        else:
            return False

    # Func calc selected fields
    @api.depends("price_lines.state")
    def _compute_selected_common_name(self):
        for record in self:
            record.selected_common_name = record.selected_price_lines.common_name
        return True

    @api.depends("price_lines.state")
    def _compute_selected_product_id(self):
        for record in self:
            record.selected_product_id = record.selected_price_lines.product_id
        return True

    @api.depends("price_lines.state")
    def _compute_selected_description(self):
        for record in self:
            record.selected_description = record.selected_price_lines.description
        return True

    @api.depends("price_lines.state")
    def _compute_selected_attachments(self):
        for record in self:
            record.selected_attachments = record.selected_price_lines.attachments
        return True

    @api.depends("price_lines.state")
    def _compute_selected_product_origin(self):
        for record in self:
            record.selected_product_origin = record.selected_price_lines.product_origin
        return True

    @api.depends("price_lines.state")
    def _compute_selected_manufacturer(self):
        for record in self:
            record.selected_manufacturer = record.selected_price_lines.manufacturer
        return True

    @api.depends("price_lines.state")
    def _compute_selected_price(self):
        for record in self:
            record.selected_price = record.selected_price_lines.subtotal
        return True

    @api.depends("price_lines.state")
    def _compute_selected_partner(self):
        for record in self:
            record.selected_partner = record.selected_price_lines.partner_id
        return True

    @api.depends("price_lines.state")
    def _compute_note(self):
        for record in self:
            record.note = record.selected_price_lines.note
        return True

    @api.depends("price_lines.state")
    def _compute_other_costs(self):
        for record in self:
            record.other_costs = record.selected_price_lines.other_costs
        return True


    @api.depends("price_lines")
    def _compute_count_price_lines(self):
        for record in self:
            record.count_price_lines = len(record.price_lines)
        return True

    # Override create method - add value field name
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.price.list.product') or _('New')
        return super().create(vals)

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()

    team_id = fields.Many2one('crm.team', 'Purchase Team', default=_get_default_team)

    def action_create_purchase(self):
        partner = self[0].selected_partner.id
        origin = self[0].origin.name
        # Check nhà cung cấp và chọn NCC
        for list_price in self:
            if (list_price.selected_partner.id != partner and list_price.selected_price_lines) or list_price.state == "buyed":
                return create_notification_sticker('Lỗi', 'Nhà cung cấp lựa chọn không giống nhau hoặc chưa chọn NCC trong 1 số bảng giá hoặc bảng giá đã mua',
                                                   'danger')
        # Tạo yêu cầu mua hàng
        res_purchase_order = self.env['purchase.order'].create({
            'origin': origin,
            'partner_id': partner,
        })

        # Tạo chi tiết yêu cầu mua hàng rồi thêm vào yêu cầu mua hàng
        for list_price in self:
            price_line = list_price.selected_price_lines
            purchase_order_line = {
                    'name': price_line.description,
                    'order_id': res_purchase_order.id,
                    'price_unit': price_line.subtotal,
                    'product_qty': price_line.min_quantity,
                    'product_id': price_line.product_id.id,
            }
            self.env['purchase.order.line'].create(purchase_order_line)

        # Thông báo
        if res_purchase_order:
            for list_price in self:
                list_price.state = "buyed"
            return create_notification_sticker('Thành công', 'Đã tạo yêu cầu mua hàng %s thành công' % res_purchase_order.name,
                                                'success')
        else:
            return create_notification_sticker('Lỗi',
                                               'Thất bại khi tạo yêu cầu mua hàng', 'danger')

