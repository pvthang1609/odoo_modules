from odoo import models, fields, api, _
from odoo.tools.misc import get_lang

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    _col_no_data = "<span style='font-style: italic;color:#71717A'>Chưa có</span>"

    selected_description = fields.Text(string='Mô tả chào bán')
    list_price = fields.Monetary(string='Giá bán nội bộ', default=0)
    standard_price = fields.Monetary(string='Giá mua', default=0)
    ei_executive_ids = fields.Many2many('res.users', string='NV XNK')
    is_expense = fields.Boolean('Is expense',
                                help="Is true if the sales order line comes from an expense or a vendor bills",
                                default=False)
    name = fields.Text(string='Mô tả yêu cầu')
    exp_date = fields.Date(string="Hạn hỏi hàng")
    price_target = fields.Monetary(string="Giá bán mục tiêu (KH)")
    standard_price_target = fields.Monetary(string="Giá mua mục tiêu")
    list_price_target = fields.Monetary(string="Giá bán nội bộ mục tiêu")

    standard_price_subtotal = fields.Monetary(string="Thành tiền nhập", store=False, readonly=True, compute="_compute_standard_price_subtotal")
    list_price_subtotal = fields.Monetary(string="Thành tiền chào bán", store=False, readonly=True, compute="_compute_list_price_subtotal")

    standard_price_target_subtotal = fields.Monetary(string="Thành tiền nhập mục tiêu", store=False, readonly=True, compute="_compute_standard_price_target_subtotal")
    list_price_target_subtotal = fields.Monetary(string="Thành tiền chào bán mục tiêu", store=False, readonly=True, compute="_compute_list_price_target_subtotal")
    price_target_subtotal = fields.Monetary(string="Thành tiền mục tiêu", store=False, readonly=True, compute="_compute_price_target_subtotal")

    product_origin = fields.Char(string="Xuất xứ yêu cầu")
    manufacturer = fields.Char(string="Nhà sản xuất yêu cầu")
    selected_product_origin = fields.Char(string="Xuất xứ chào bán")
    selected_manufacturer = fields.Char(string="Nhà sản xuất chào bán")
    selected_model = fields.Char(string="Model chào bán")
    selected_partner_id = fields.Many2one("res.partner", string="NCC đã chọn")

    min_quantity = fields.Char(string="Số lượng chào bán")
    attachments = fields.Binary(string="Tài liệu đính kèm", attachment=True)

    common_name = fields.Char(string="Tên yêu cầu", compute="_compute_common_name", readonly=False)
    selected_common_name = fields.Char(string="Tên chào bán", compute="_compute_common_name", readonly=False)

    price_list_id = fields.Many2one('sale.order.price.list.product', string='Bảng giá', readonly=True)

    delivery_time_customer = fields.Char(string='Thời gian giao hàng (KH)')
    delivery_time_partner = fields.Char(string='Thời gian giao hàng (NCC)')

    # field combine
    combine_product = fields.Html(string="Sản phẩm yêu cầu", store=False, compute="_compute_combine_product")
    combine_product_target = fields.Html(string="Sản phẩm chào bán", store=False, compute="_compute_combine_product_target")
    combine_price = fields.Html(string="Giá", store=False, compute="_compute_combine_price")
    combine_price_target = fields.Html(string="Giá mục tiêu", store=False, compute="_compute_combine_price_target")
    combine_request = fields.Html(string="Tổng hợp yêu cầu", store=False, compute="_compute_combine_request")
    combine_selected = fields.Html(string="Tổng hợp thực tế", store=False, compute="_compute_combine_selected")

    def _convertNumber(self, value):
        if value:
            str =  f"{value:,}"
            return str[0:-2]
        else:
            return False

    def _create_price_list_product(self, vals):
        return self.env['sale.order.price.list.product'].create(vals)

    def action_create_price_list_product(self):
        for order_line in self:
            if not order_line.price_list_id:
                init_price_list_product = {
                    'origin': order_line.order_id.id,
                    'origin_common_name': order_line.common_name,
                    'origin_product_id': order_line.product_id.id,
                    'origin_description': order_line.name,
                    'ei_executive_ids': [user.id for user in order_line.ei_executive_ids],
                    'standard_price_target': order_line.standard_price_target,
                    'origin_product_origin': order_line.product_origin,
                    'origin_manufacturer': order_line.manufacturer,
                    'origin_attachments': order_line.attachments
                }
                price_list = self._create_price_list_product(init_price_list_product)
                order_line.price_list_id = price_list
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thành công',
                        'message': 'Bạn đã tạo thành công bảng giá %s vui lòng kiểm tra trong menu "Bảng giá"' % (price_list.name),
                        'type': 'success',
                        'sticky': False
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thất bại',
                        'message': 'Đã tồn tại bảng giá %s' % order_line.price_list_id.name,
                        'type': 'danger',
                        'sticky': False
                    }
                }

    @api.depends('standard_price','product_uom_qty')
    def _compute_standard_price_subtotal(self):
        for line in self:
            line.standard_price_subtotal = line.standard_price * line.product_uom_qty
        return True

    @api.depends('list_price','product_uom_qty')
    def _compute_list_price_subtotal(self):
        for line in self:
            line.list_price_subtotal = line.list_price * line.product_uom_qty
        return True

    @api.depends('standard_price_target','product_uom_qty')
    def _compute_standard_price_target_subtotal(self):
        for line in self:
            line.standard_price_target_subtotal = line.standard_price_target * line.product_uom_qty
        return True

    @api.depends('list_price_target','product_uom_qty')
    def _compute_list_price_target_subtotal(self):
        for line in self:
            line.list_price_target_subtotal = line.list_price_target * line.product_uom_qty
        return True

    @api.depends('price_target','product_uom_qty')
    def _compute_price_target_subtotal(self):
        for line in self:
            line.price_target_subtotal = line.price_target * line.product_uom_qty
        return True

    @api.depends('product_id')
    def _compute_common_name(self):
        for line in self:
            line.common_name = line.product_id.common_name
        return True

    @api.depends('standard_price_target_subtotal','list_price_target_subtotal','price_target_subtotal')
    def _compute_combine_price(self):
        for line in self:
            line.combine_price = "<div style='font-size: 11px; width: 250px'><p class='white-space-nor'>" \
                                 "<span style='font-weight: 600'>Giá bán (KH): </span><span>%s x %s = %s</span></p>" \
                                 "<p class='white-space-nor'><span style='font-weight: 600'>Giá nhập: </span>" \
                                 "<span>%s x %s = %s</span> </p><p class='white-space-nor'>" \
                                 "<span style='font-weight: 600'>Giá bán nội bộ: </span><span>%s x %s = %s</span></p></div>"\
                                 % (self._convertNumber(line.price_unit) or self._col_no_data,
                                    self._convertNumber(line.product_uom_qty) or self._col_no_data,
                                    self._convertNumber(line.price_subtotal) or self._col_no_data,
                                    self._convertNumber(line.standard_price) or self._col_no_data,
                                    self._convertNumber(line.product_uom_qty) or self._col_no_data,
                                    self._convertNumber(line.standard_price_subtotal) or self._col_no_data,
                                    self._convertNumber(line.list_price) or self._col_no_data,
                                    self._convertNumber(line.product_uom_qty) or self._col_no_data,
                                    self._convertNumber(line.list_price_subtotal) or self._col_no_data,)
        return True

    @api.depends('standard_price_target_subtotal', 'list_price_target_subtotal', 'price_target_subtotal')
    def _compute_combine_price_target(self):
        for line in self:
            line.combine_price_target = "<div style='font-size: 11px; width: 250px'><p class='white-space-nor'>" \
                                 "<span style='font-weight: 600'>GBMT (KH): </span><span>%s x %s = %s</span></p>" \
                                 "<p class='white-space-nor'><span style='font-weight: 600'>GNMT: </span>" \
                                 "<span>%s x %s = %s</span> </p><p class='white-space-nor'>" \
                                 "<span style='font-weight: 600'>GBNBMT: </span><span>%s x %s = %s</span></p></div>"\
                                 % (self._convertNumber(line.price_target) or self._col_no_data,
                                    self._convertNumber(line.product_uom_qty) or self._col_no_data,
                                    self._convertNumber(line.price_target_subtotal) or self._col_no_data,
                                    self._convertNumber(line.standard_price_target) or self._col_no_data,
                                    self._convertNumber(line.product_uom_qty) or self._col_no_data,
                                    self._convertNumber(line.standard_price_target_subtotal) or self._col_no_data,
                                    self._convertNumber(line.list_price_target) or self._col_no_data,
                                    self._convertNumber(line.product_uom_qty) or self._col_no_data,
                                    self._convertNumber(line.list_price_target_subtotal) or self._col_no_data,)
        return True

    @api.depends('product_origin', 'manufacturer')
    def _compute_combine_request(self):
        for line in self:
            line.combine_request = "<div style='font-size: 11px; width: 250px'><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Xuất xứ: </span><span>%s</span> </p><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Nhà sản xuất: </span><span>%s</span> </p><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Mô tả: </span><span>%s</span></p></div>" % \
                                    (line.product_origin or self._col_no_data,
                                    line.manufacturer or self._col_no_data,
                                    line.name or self._col_no_data,)
        return True

    @api.depends('selected_product_origin', 'selected_manufacturer')
    def _compute_combine_selected(self):
        for line in self:
            line.combine_selected = "<div style='font-size: 11px; width: 250px'><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>NCC: </span><span>%s</span></p><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Thời gian giao hàng (NCC): </span><span>%s</span> </p><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Xuất xứ: </span><span>%s</span> </p><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Nhà sản xuất: </span><span>%s</span> </p><p class='white-space-nor'>" \
                                    "<span style='font-weight: 600'>Mô tả: </span><span>%s</span></p></div>" % \
                                    (line.selected_partner_id.name or self._col_no_data,
                                     line.delivery_time_partner or self._col_no_data,
                                     line.selected_product_origin or self._col_no_data,
                                    line.selected_manufacturer or self._col_no_data,
                                    line.selected_description or self._col_no_data)
        return True

    @api.depends('selected_product_origin', 'selected_manufacturer')
    def _compute_combine_product(self):
        for line in self:
            combine_variant_value = ""
            for variant_value in line.product_id.product_template_variant_value_ids:
                combine_variant_value = combine_variant_value + variant_value.name if combine_variant_value == "" else ", %s" % variant_value.name
            line.combine_product = "<div style='font-size: 11px; width: 250px'><p class='white-space-nor'>" \
                                    "<span>%s</span></p><p class='white-space-nor'><span style='font-weight: 600'>%s</span></p></div>"% \
                                    (line.common_name or self._col_no_data,
                                    "%s %s %s" % (line.product_id.product_tmpl_id.name, "-" if combine_variant_value else "", combine_variant_value)or self._col_no_data,)
        return True

    @api.depends('selected_product_origin', 'selected_manufacturer')
    def _compute_combine_product_target(self):
        for line in self:
            line.combine_product_target = "<div style='font-size: 11px; width: 250px'><p class='white-space-nor'>" \
                                        "<span>%s</span></p><p class='white-space-nor'><span style='font-weight: 600'>%s</span></p></div>"% \
                                        (line.selected_common_name or self._col_no_data,
                                        line.selected_model or self._col_no_data,)
        return True