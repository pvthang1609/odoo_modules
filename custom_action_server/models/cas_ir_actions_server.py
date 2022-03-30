from odoo import models, fields


class ServerAction(models.Model):
    _name = 'ir.actions.server'
    _inherit = 'ir.actions.server'

    icon = fields.Char()
