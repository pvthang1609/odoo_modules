# -*- coding: utf-8 -*-
from odoo import fields, models
from vnsolution.tool import create_notification_sticker

import logging

_logger = logging.getLogger(__name__)


class AskinfoProductActionsWizard(models.TransientModel):
    _name = "askinfo.product.actions.wizard"
    _description = "Hành động với sản phẩm hỏi hàng"

    action_type = fields.Selection([('create_order_sale', 'Tạo báo giá'),
                                    ('create_askinfo_product_line', 'Tạo thông tin hỏi hàng đến NCC'),
                                    # CHANGE STATE
                                    ('send_sale_manager', 'Trình TPKD'),
                                    ('approve', 'Duyệt SP'),
                                    ('reject_draft', 'Từ chối SP'),
                                    ('assign', 'Phân công'),
                                    ('fill_local_price', 'Nhập giá bán nội bộ'),
                                    ('confirm_local_price', 'Xác nhận giá bán nội bộ'),
                                    ('fill_price', 'Nhập giá bán (KH)'),
                                    ('confirm_fill_price', 'Xác nhận giá bán (KH)'),
                                    ('confirm', 'Xác nhận báo giá'),
                                    ('send_customer', 'Đã gửi báo giá'),
                                    ('customer_cancel', 'Khách hàng hủy đơn hàng'),
                                    ('customer_reject', 'Khách hàng từ chối báo giá'),
                                    ('fill_local_price_target', 'Nhập giá bán nội bộ mục tiêu'),
                                    ('confirm_local_price_target', 'Xác nhận giá bán nội bộ mục tiêu'),
                                    ('fill_purchase_price_target', 'Nhập giá mua mục tiêu'),], string='Loại hành động')
    user_ids = fields.Many2many('res.users', string="Những người dùng liên quan")
    partner_ids = fields.Many2many('res.partner', string="Những khách hàng liên quan")
    content = fields.Text(string="Nội dung liên quan")

    def _change_state(self, array, value):
        new_state = {"state": value}
        for record in array:
            record.write(new_state)

    def action_handle(self):
        ids = self.env.context['active_ids']
        askinfo_products = self.env["askinfo.product"].browse(ids)

        if self.action_type == 'create_order_sale':
            customer_id = askinfo_products[0].customer_id
            for record in askinfo_products:
                if record.state != 'manager_confirmed':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
                if record.customer_id != customer_id:
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s không khớp thông tin khách hàng.' % record.id,
                                                       'danger')
            # CREATE SALE ORDER
            sale_order = self.env['sale.order'].create({
                'partner_id': customer_id.id
            })
            for product in askinfo_products:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': product.selected_askinfo_product_line.product_id.id
                })

        if self.action_type == 'create_askinfo_product_line':
            for i in self.partner_ids:
                print(i)

        if self.action_type == 'send_sale_manager':
            for record in askinfo_products:
                if record.state != 'draft' or record.state != 'reject_draft':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'sent_sale_manager')

        if self.action_type == 'approve':
            for record in askinfo_products:
                if record.state != 'sent_sale_manager':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'sent_ei_manager')

        if self.action_type == 'reject_draft':
            for record in askinfo_products:
                if record.state != 'sent_sale_manager':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'reject_draft')
            # TODO: Thiếu tạo lý do

        if self.action_type == 'assign':
            for record in askinfo_products:
                if record.state != 'sent_ei_manager':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            new_data = {'ei_executive_ids': self.user_ids}
            for record in askinfo_products:
                record.write(new_data)
            self._change_state(askinfo_products, 'assigned')

        if self.action_type == 'fill_local_price':
            for record in askinfo_products:
                if record.state != 'had_price_to_partner':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
                if not record.local_price:
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s chưa có giá bán nội bộ.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'had_local_price')

        if self.action_type == 'confirm_local_price':
            for record in askinfo_products:
                if record.state != 'had_local_price':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'confirmed_local_price')

        if self.action_type == 'fill_price':
            for record in askinfo_products:
                if record.state != 'confirmed_local_price':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
                if not record.price:
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s chưa có giá bán (KH).' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'had_price')

        if self.action_type == 'confirm_fill_price':
            for record in askinfo_products:
                if record.state != 'had_price':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'sale_manager_confirmed')

        if self.action_type == 'confirm':
            for record in askinfo_products:
                if record.state != 'sale_manager_confirmed':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'manager_confirmed')

        if self.action_type == 'send_customer':
            for record in askinfo_products:
                if record.state != 'manager_confirmed':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'sent')

        if self.action_type == 'customer_cancel':
            for record in askinfo_products:
                if record.state != 'sent':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'cancel')

        if self.action_type == 'fill_local_price_target':
            for record in askinfo_products:
                if record.state != 'sent':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'had_local_price_target')

        if self.action_type == 'confirm_local_price_target':
            for record in askinfo_products:
                if record.state != 'had_local_price_target':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'confirmed_local_price_target')

        if self.action_type == 'fill_purchase_price_target':
            for record in askinfo_products:
                if record.state != 'confirmed_local_price_target':
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s sai trạng thái.' % record.id,
                                                       'danger')
                if not record.purchase_price:
                    return create_notification_sticker('Lỗi', 'Sản phẩm hỏi hàng - id: %s chưa có giá mua mục tiêu.' % record.id,
                                                       'danger')
            self._change_state(askinfo_products, 'had_purchase_price_target')




