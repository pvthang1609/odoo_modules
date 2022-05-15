# -*- coding: utf-8 -*

from odoo.addons.bus.controllers.main import BusController
from odoo.http import request


class VNSNotificationBusController(BusController):
    # --------------------------
    # Extends BUS Controller Poll
    # --------------------------
    def _poll(self, dbname, channels, last, options):
        if request.session.uid:
            channels = list(channels)
            channels.append((request.db, f'vns_notify_{request.env.user.id}'))
        return super(VNSNotificationBusController, self)._poll(dbname, channels, last, options)