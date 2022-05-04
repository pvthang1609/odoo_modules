from odoo import fields, models


class ActWindowView(models.Model):
    _inherit = 'ir.actions.act_window.view'

    view_mode = fields.Selection(selection_add=[('owl_tree_view', 'Cây thư mục')],
                                 ondelete={'owl_tree_view': 'cascade'})
