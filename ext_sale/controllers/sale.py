from odoo import http


class MyController(http.Controller):
    @http.route('/get_order', type="json", auth='user', methods=['POST'])
    def handler_get_order(self):
        sale_order_rec = http.request.env['sale.order'].search([])
        sale_orders = []
        for record in sale_order_rec:
            val = {
                'id': record.id,
                'name': record.name
            }
            sale_orders.append(val)

        res = {
            'success': True,
            'data': {
                'code': 200,
                'data': sale_orders,
                'message': 'success'
            }
        }
        return res

    @http.route('/create_currency', type="json", auth='user', methods=['POST'])
    def handler_create_order(self, **rec):
        # Create record in table currency
        result = http.request.env['currency'].create({
            'name': rec['name'],
            'current_exchange_rate': rec['price']
        })

        res = {
            'success': True,
            'data': {
                'code': 200,
                'data': result.id,
                'message': 'success'
            }
        }
        return res
