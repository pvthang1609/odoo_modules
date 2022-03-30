from odoo import fields, models, api


class ExtSalePriceLine(models.Model):
    _name = "sale.order.price.line"
    _description = "Danh sách giá"

    common_name = fields.Char(string="Tên sản phẩm")
    product_id = fields.Many2one("product.product", string="Model")
    partner_id = fields.Many2one("res.partner", string="Nhà cung cấp", required=True)
    partner_rate = fields.Integer(string='Đánh giá ncc', readonly=True, compute="_compute_partner_rate")
    ei_executive_id = fields.Many2one('res.users', string="NV XNK", default=lambda self: self.env.user, readonly=True)
    delivery_time_partner = fields.Char(string='Thời gian giao hàng (NCC)')

    price_list_product_id = fields.Many2one("sale.order.price.list.product", required=True)
    state = fields.Selection([
        ('selected', 'Đã chọn'),
        ('not_select', ''),
    ], string='Trạng thái',  default='not_select', readonly=True)

    unit_currency = fields.Many2one("currency", string="ĐV tiền tệ", required=True)
    price = fields.Float(string="Giá", required=True)
    exchange_rate = fields.Float(string='Tỷ giá', required=True, store=True, readonly=False, compute="_compute_exchange_rate")
    subtotal = fields.Float(string='Thành tiền', readonly=True, compute="_compute_subtotal")

    product_origin = fields.Char(string="Xuất xứ")
    manufacturer = fields.Char(string="Nhà sản xuất")
    min_quantity = fields.Char(string="Số lượng tối thiểu", )
    payment_term = fields.Text(string="Điều kiện thanh toán")
    delivery_term = fields.Text(string="Điều kiện giao hàng")
    description = fields.Text(string="Mô tả", required=True)
    attachments = fields.Binary(string="File đính kèm", attachment=True)
    note = fields.Text(string="Ghi chú")
    other_costs = fields.Float(string="Chi phí khác")
    is_proposed = fields.Boolean(string="Đã được đề xuất")

    def action_confirm_price(self):
        for record in self:
            for price_line in record.price_list_product_id.price_lines:
                price_line.state = "not_select"
            record.price_list_product_id.selected_price_lines = record.id
            record.state = 'selected'
            record.price_list_product_id.state = "selected"
            # TODO: sau khi TPXNK chọn giá thì sẽ thông báo đến NVXNK đã chọn giá đó (chưa có thông báo)
        return True

    def action_propose(self):
        for record in self:
            record.is_proposed = not record.is_proposed
        return True

    def action_restore_confirmed(self):
        for record in self:
            record.state = "not_select"
            record.price_list_product_id.state = "processing"
        return True

    def _create_activity_mail(self, document_id, document_name, summary, note, user_sent_to):
        model_price_list_id = int(self.env['ir.config_parameter'].sudo().get_param('model_price_list_id'))
        self.env['mail.activity'].create({
            'res_model': 'sale.order.price.list.product',
            'res_model_id': model_price_list_id,
            'res_id': document_id,
            'res_name': document_name,
            'activity_type_id': 4,
            'summary': summary,
            'note': '<p>%s</p>' % note,
            'user_id': user_sent_to
        })

    @api.depends('exchange_rate', 'price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.price * line.exchange_rate
        return True

    @api.depends('unit_currency')
    def _compute_exchange_rate(self):
        for line in self:
            line.exchange_rate = line.unit_currency.current_exchange_rate
        return True

    # Lúc create thì cần check xem price line có phải là đầu tiên hay không
    @api.model
    def create(self, vals):
        record = super().create(vals)
        count_record = len(record.price_list_product_id.price_lines)
        document_id = record.price_list_product_id.id
        document_name = record.price_list_product_id.name
        if count_record == 1:
            sale_order = record.price_list_product_id.origin
            if sale_order:
                sale_order.write({'state': 'had_price_to_partner'})
                team_purchase_id = self.env['ir.config_parameter'].sudo().get_param('team_purchase_id')
                # id trưởng phòng XNK, gửi thông báo đến trưởng phòng XNK
                ei_manager_id = self.env['crm.team'].search([('id', '=', team_purchase_id)]).user_id.id
                self._create_activity_mail(document_id, document_name, 'Lựa chọn NCC', 'Bảng giá %s đã có giá NCC.'
                                           % document_name, ei_manager_id)
        return record

    @api.depends('partner_id')
    def _compute_partner_rate(self):
        for line in self:
            line.partner_rate = line.partner_id.rate
        return True
