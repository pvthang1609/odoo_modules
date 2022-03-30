from odoo import fields, models, api, _


class Reason(models.Model):
    _name = 'reason'
    _description = "Lý do từ chối"

    content = fields.Text(string='Nội dung')
    sale_order_id = fields.Many2one("sale.order", string="Id YCBG/ĐH")
    new_document_state = fields.Char(string='Trạng thái mới của document')

    def action_change_state(self, document_id, state):
        sale_order = self.env['sale.order'].search([('id', '=', document_id)])
        sale_order.write({'state': state})

    # Sau khi thêm lý do thì sẽ chạy callback để thay đổi state của sale_order
    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record:
            self.action_change_state(vals['sale_order_id'], vals['new_document_state'])
            return record