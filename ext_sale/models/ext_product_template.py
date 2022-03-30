from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # variable more
    _default_description = """<ul><li><span style="font-weight: bolder;">Nhà SX:</span> chưa có thông tin</li><li><span style="font-weight: bolder;">Xuất xứ: </span>
chưa có thông tin
</li><li><span style="font-weight: bolder;">SL tối thiểu:</span> 
chưa có thông tin
</li><li><span style="font-weight: bolder;">Chi tiết:</span>
chưa có thông tin
 </li></ul>"""

    name = fields.Char(string='Model')
    common_name = fields.Char(string='Tên chung')
    state = fields.Selection(string='Status', selection=[('global', 'Toàn hệ thống'), ('local', 'Cục bộ')], default="local")
    service_to_purchase = fields.Boolean("Subcontract Service",
                                         help="If ticked, each time you sell this product through a SO, a RfQ is automatically created to buy the product. Tip: don't forget to set a vendor on the product.")
    invoice_policy = fields.Selection([
        ('order', 'Ordered quantities'),
        ('delivery', 'Delivered quantities')], string='Invoicing Policy',
        help='Ordered Quantity: Invoice quantities ordered by the customer.\n'
             'Delivered Quantity: Invoice quantities delivered to the customer.',
        default='delivery')
    description = fields.Html(default=_default_description)

    _sql_constraints = [
        ('check_unique', 'unique(name)',
         'Model đã tồn tại')
    ]

    def action_approve_product(self):
        for record in self:
            record.state = "global"
        return True
