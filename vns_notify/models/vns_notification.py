from odoo import fields, models, api


class VNSNotification(models.Model):
    _name = "vns.notification"
    _description = "Thông báo - vns"
    _order = "id desc"

    name = fields.Text(string="Tiêu đề", default="Thông báo hệ thống")
    content = fields.Text(string="Nội dung")
    is_read = fields.Boolean(string="Đã đọc ?", default=False)
    link = fields.Text(string="Liên kết chuyển hướng", default=False)
    receiver_id = fields.Many2one('res.users', string="Người nhận")
    target = fields.Selection([('self', 'Tại trang tab hiện tại'), ('new', 'Mở trên tab mới')], string="Cách thức mở",
                              default='new')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        self.env['res.users'].browse(vals['receiver_id']).actions_create_notify()
        return res

    def compute_count_unread(self):
        return self.env['vns.notification'].search_count([('is_read', '=', False), ('receiver_id', '=', self.env.user.id)])
