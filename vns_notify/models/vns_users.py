from odoo import fields, models, api


class VNSUsers(models.Model):
    _inherit = "res.users"

    def actions_create_notify(self):
        self.env['bus.bus']._sendone(f'vns_notify_{self.id}', 'create', {})
