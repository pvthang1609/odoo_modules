from odoo import fields, models, api, _
import os

class ExtSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'mail.thread']

    state = fields.Selection([
        ('reject_draft', 'Từ chối YCBG'),
        ('reject_list_price', 'Từ chối giá chào bán'),
        ('reject_quotation', 'Từ chối báo giá'),
        ('cancel', 'Hủy'),

        ('draft', 'YCHH'),
        ('sent_sale_manager', 'Đã gửi TPKD'),
        ('sent_ei_manager', 'Đã gửi QLXNK'),
        ('draft_assigned', 'Đã phân công'),
        ('had_price_to_partner', 'Có giá từ NCC'),
        ('had_list_price', 'Có GBNB'),
        ('confirm_list_price', 'Đã xác nhận GBNB'),
        ('quotation', 'Báo giá'),
        ('confirmed', 'Đã duyệt'),
        ('sent', 'Đã gửi'),
        # Bổ sung quy trình - start
        ('had_price_target', 'Có giá bán mục tiêu (KH)'),
        ('confirm_price_target', 'Duyệt giá bán mục tiêu (KH)'),
        ('had_standard_price', 'Có giá mua mục tiêu'),
        # Bổ sung quy trình - end
        ('sale', 'Đã đề xuât'),
        ('processing', 'Đang thực hiện'),
        ('done', 'Hoàn thành'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')

    purchase_order_count = fields.Integer()
    attachment_ids = fields.Many2many("ir.attachment", string="Attachments")
    ei_executive_ids = fields.Many2many("res.users", string="NV XNK liên quan", compute="_compute_ei_executive_ids")
    reason_ids = fields.One2many('reason', 'sale_order_id', string='Lý do từ chối')
    reason = fields.Text(string='Lý do từ chối')

    reason_last = fields.Text(string='Lý do từ chối', compute="_compute_reason_last", default="")

    def print_env(self):
        os.environ['USER'] = 'Bob'
        name = os.environ.get('USER')
        print(name)

    # Tạo mảng lưu các NVXNK liên quan đến đơn hàng
    @api.depends("order_line.ei_executive_ids")
    def _compute_ei_executive_ids(self):
        new_ei_executive_ids = []
        for order in self:
            for line in order.order_line:
                for ei_executive in line.ei_executive_ids:
                    new_ei_executive_ids.append(ei_executive.id)
            order.ei_executive_ids = new_ei_executive_ids
        return True

    @api.depends("reason_ids")
    def _compute_reason_last(self):
        reasons = self.env['reason'].search([], order='id desc')
        for order in self:
            order.reason_last = "" if len(reasons) == 0 else reasons[0].content
        return True

    def _create_notification(self):
        message = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Warning!'),
                'message': 'You cannot do this action now',
                'sticky': False,
            }
        }
        return message

    def _create_activity_mail(self, document_id, document_name, summary, note, user_sent_to):
        model_sale_order_id = self.env['ir.config_parameter'].sudo().get_param('model_sale_order_id')
        self.env['mail.activity'].create({
            'res_model': 'sale.order',
            'res_model_id': int(model_sale_order_id),
            'res_id': document_id,
            'res_name': document_name,
            'activity_type_id': 4,
            'summary': summary,
            'note': '<p>%s</p>' % (note),
            'user_id': user_sent_to
        })

    def _create_reason(self, sale_order_id, state):
        return {
            'name': 'Lý do từ chối',
            'view_mode': 'form',
            'res_model': 'reason',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_sale_order_id': sale_order_id,
                        'default_new_document_state': state}
        }

    def action_sale_sent_sale_manager(self):
        for order in self:
            order.state = 'sent_sale_manager'
            self._create_activity_mail(order.id, order.name, 'Duyệt', 'YCBG %s đã được trình.' % order.name,
                                       order.team_id.user_id.id)
        return True

    def action_sale_sent_ei_manager(self):
        team_purchase_id = self.env['ir.config_parameter'].sudo().get_param('team_purchase_id')
        # id trưởng phòng mua hàng
        ei_manager_id = self.env['crm.team'].search([('id', '=', team_purchase_id)]).user_id.id
        for order in self:
            order.state = 'sent_ei_manager'
            self._create_activity_mail(order.id, order.name, 'Xác nhận phân công', 'YCBG %s đã được duyệt.' % order.name,
                                       ei_manager_id)
        return True

    def action_ei_manager_assigns(self):
        for order in self:
            order.state = 'draft_assigned'
            for user in order.ei_executive_ids:
                self._create_activity_mail(order.id, order.name, 'Phân công', 'YCBG %s đã phân công.' % order.name,
                                           user.id)
        return True

    def action_ei_manager_fill_list_price(self):
        for order in self:
            order.state = 'had_list_price'
             # TODO: Gửi thông báo đến trưởng phòng kinh doanh xác nhận
            self._create_activity_mail(order.id, order.name, 'Xác nhận giá bán nội bộ', 'YCBG %s đã có giá nội bộ.' % order.name,
                                       order.team_id.user_id.id)
        return True

    def action_sale_manager_confirm_list_price(self):
        for order in self:
            order.state = 'confirm_list_price'
            # Gửi thông báo đến TPXNK
            self._create_activity_mail(order.id, order.name, 'Thêm giá bán',
                                       'YCBG %s đã có giá bán nội bộ.' % order.name, order.user_id.id)
        return True

    def action_sale_fill_price(self):
        manager_group_id = self.env['ir.config_parameter'].sudo().get_param('manager_group_id')
        # ids của nhóm ban giám đốc
        manager_ids = self.env['res.users'].search([('groups_id.id', '=', manager_group_id )])
        for order in self:
            order.state = 'quotation'
            # Gửi thông báo đến TP KD và BGĐ
            self._create_activity_mail(order.id, order.name, 'Thêm giá bán',
                                       'YCBG %s đã có giá bán (KH).' % order.name, order.team_id.user_id.id)
            for user in manager_ids:
                self._create_activity_mail(order.id, order.name, 'Thêm giá bán',
                                           'YCBG %s đã có giá bán (KH).' % order.name, user.id)
        return True

    def action_manager_approve(self):
        for order in self:
            order.state = 'confirmed'
            self._create_activity_mail(order.id, order.name, 'Gửi YCBG cho KH',
                                       'YCBG %s đã được duyệt.' % order.name, order.user_id.id)
        return True

    def action_sale_sent(self):
        for order in self:
            order.state = 'sent'
        return True
    # HERE
    def action_customer_approve(self):
        for order in self:
            # TODO: khi khách hàng xác nhận NVKD nhập giá mục tiêu và xác nhận giá mục tiêu
            order.state = 'had_price_target'
            # Thông báo đến TPKD
            self._create_activity_mail(order.id, order.name, 'Xác nhận giá bán mục tiêu (KH)',
                                       'Đơn hàng %s đã có giá mục tiêu (KH).' % order.name, order.team_id.user_id.id)
        return True

    def action_sale_manager_confirm_price_target(self):
        for order in self:
            # TODO: TPKD xác nhận giá mục tiêu
            order.state = 'confirm_price_target'
            # Thông báo đến TPXNK
            # self._create_activity_mail(order.id, order.name, 'Xác nhận giá mua mục tiêu',
            #                            'Đơn hàng %s đã được xác nhận giá mục tiêu (KH).' % order.name, order.team_id.user_id.id)
        return True

    def action_ei_manager_fill_standard_price_target(self):
        for order in self:
            # TODO: Khi TPKD xác nhận giá bán mục tiêu thì TPXNK xác nhận giá mua mục tiêu
            order.state = 'had_standard_price'
            # Thông báo đến các NVXNK liên quan
            # self._create_activity_mail(order.id, order.name, 'Đề xuất mua hàng theo giá mua mục tiêu',
            #                            'Đơn hàng %s đã có giá mua mục tiêu.' % order.name, ei_manager_id)
        return True

    def action_customer_refuse(self):
        for order in self:
            _create_reason(order.id, 'cancel')

    # Khi khởi yêu cầu mua hàng được chấp thuận thì sẽ chuyển sang trạng thái này
    # TODO: Chưa có xử lý đoạn đổi state này.
    def action_order_process(self):
        for order in self:
            order.state = 'processing'
        return True

    # Khi đơn hàng được thanh toán hết, NV kinh doanh có thể hoàn thành đơn hàng
    def action_order_finish(self):
        for order in self:
            order.state = 'done'
        return True

    def action_reject_draft(self):
        for order in self:
            return self._create_reason(order.id, 'reject_draft')

    def action_reject_quotation(self):
        for order in self:
            return self._create_reason(order.id, 'reject_quotation')

    # ===> TEST <===

    def action_test(self):
        for record in self:
            data = {
                res_model: 'sale.order',
                res_id: 14,
                res_model_id: 495,
                res_name: 'S00014',
                activity_tye_id: 4,
                user_id: 2
            }
        return True
