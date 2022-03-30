from odoo import models, tools
from odoo.exceptions import MissingError, AccessError

from collections import defaultdict


class IrActions(models.Model):
    _name = 'ir.actions.actions'
    _inherit = 'ir.actions.actions'

    @tools.ormcache('frozenset(self.env.user.groups_id.ids)', 'model_name', 'debug')
    def _get_bindings(self, model_name, debug=False):
        """ Retrieve the list of actions bound to the given model.

           :return: a dict mapping binding types to a list of dict describing
                    actions, where the latter is given by calling the method
                    ``read`` on the action record.
        """
        cr = self.env.cr
        IrModelAccess = self.env['ir.model.access']

        # discard unauthorized actions, and read action definitions
        result = defaultdict(list)
        user_groups = self.env.user.groups_id
        if not debug:
            user_groups -= self.env.ref('base.group_no_one')

        self.flush()
        cr.execute("""
                SELECT a.id, a.type, a.binding_type
                  FROM ir_actions a
                  JOIN ir_model m ON a.binding_model_id = m.id
                 WHERE m.model = %s
              ORDER BY a.id
            """, [model_name])
        for action_id, action_model, binding_type in cr.fetchall():
            try:
                action = self.env[action_model].sudo().browse(action_id)
                action_groups = getattr(action, 'groups_id', ())
                action_model = getattr(action, 'res_model', False)
                if action_groups and not action_groups & user_groups:
                    # the user may not perform this action
                    continue
                if action_model and not IrModelAccess.check(action_model, mode='read', raise_exception=False):
                    # the user won't be able to read records
                    continue
                fields = ['name', 'binding_view_types']
                server_fields = ['name', 'binding_view_types', 'icon']
                if 'sequence' in action._fields:
                    fields.append('sequence')
                if action._name == 'ir.actions.server':
                    result[binding_type].append(action.read(server_fields)[0])
                else:
                    result[binding_type].append(action.read(fields)[0])
            except (AccessError, MissingError):
                continue

        # sort actions by their sequence if sequence available
        if result.get('action'):
            result['action'] = sorted(result['action'], key=lambda vals: vals.get('sequence', 0))

        return result
