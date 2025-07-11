from os import name
from werkzeug import Response
from odoo import http
from odoo.http import request

class MyApi(http.Controller):
    
    def count_parent(self, employee):
        count = 0
        current = employee.parent_id
        while current:
            count += 1
            current = current.parent_id
        return count
        
    def get_employee_hierarchy(self, employee):
        h = []

        for emp in employee:
            h.append({
                'name': emp.name,
                'work_email': emp.work_email,
                'job_title': emp.job_id.name,
                'possible parents count': self.count_parent(emp),
                'subordinates': self.get_employee_hierarchy(emp.child_ids)
            })

        return h

    @http.route('/api/fetch_employee_details', type='json', auth='public', methods=['POST'], csrf=False)
    def fetch_employee_details(self, **data):
        emp_id = data.get('emp_id')

        if not emp_id:
            return {'error': 'Please provide employee ID'}
        
        employee = request.env['hr.employee'].sudo().browse(emp_id)
        
        if not employee.exists():
            return {'error': 'employee not found'}


        if not employee.parent_id:
            manager = 'No Manager'

        manager = employee.parent_id.name

        if not employee.coach_id:
            coach = 'No Coach'

        coach = employee.coach_id.name

        hierarchy = self.get_employee_hierarchy(employee)

        return {
            'employee': {
                'Name': employee.name,
                'Work Email': employee.work_email,
                'Company': employee.company_id.name,
                'Manager': manager,
                'Coach': coach,
                'Subordinates': hierarchy
            }
        }

    @http.route('/api/fetch_settings', type='json', auth='public', methods=['POST'], csrf=False)
    def set_settings(self, **data):
        config = request.env['ir.config_parameter'].sudo()
        f1 = data.get('custom_field_1')
        f2 = data.get('custom_field_2')
        f3 = data.get('custom_field_3')
        
        print(type(f1))

        
        config.set_param('custom_sales_module.custom_field_1', f1)
        config.set_param('custom_sales_module.custom_field_2', f2)
        config.set_param('custom_sales_module.custom_field_3', f3)

        return {
            'status': 'success',
            'data': {
                'custom_field_1': f1,
                'custom_field_2': f2,
                'custom_field_3': f3
            }
        }

    @http.route('/api/create_invoice', type='json', auth='public', methods=['POST'], csrf=False)
    def create_invoice(self, **data):
        sale_order_id = data.get('sale_order_id')
        
        if not sale_order_id:
            return {
                "result": False,
                "error": "Sales order ID is required"
            }
                
        sale_order = request.env['sale.order'].sudo().browse(sale_order_id)

        if not sale_order.exists():
            return {
                "result": False,
                "error": "Sales order not found"
            }
        
        products_with_price = {}

        for product in sale_order.order_line:
            products_with_price[product.product_id.name] = {
                'price': product.price_unit,
                'quantity': product.product_uom_qty
            }

        return {
            "result": True,
            "order_id": sale_order.id,
            "order_name": sale_order.name,
            "customer_name": sale_order.partner_id.name,
            "products": products_with_price,
            "amount_total": sale_order.amount_total,
        }

    @http.route("/api/get_dues", type='json', methods=['POST'], csrf=False, auth='public' )
    def get_dues(self, **data):
        customer_id = data.get('customer_id')   

        partner = request.env['res.partner'].sudo().browse(customer_id)

        if not partner:
            return {
                "result": False,
                "error": "partner not exists"
            }

        invoices = request.env['account.move'].sudo().search([
            ('partner_id', '=', partner.id),
            ('state','=','posted'),
            ('payment_state', '!=', 'paid'),
            ('move_type', '=', 'out_invoice')
            ])

        total_due = 0
        
        for inv in invoices:
            total_due += inv.amount_residual

        payments = request.env['account.move'].sudo().search([
            ('partner_id', '=', partner.id)
        ])

        dates = []
        for payment in payments:
            dates.append(payment.date)
            
        # print(total_due)

        return {
            "result": True,
            "customer": customer_id,
            "customer_name": partner.name,
            "customer_email": partner.email,
            "total due": total_due,
            "total_unpaid_invoices": len(invoices),
            "total payments": len(payments),
            "payments": payments,
            "dates": dates[0],
        }
        
    
    @http.route('/api/fetch_total_users', methods=['POST'], csrf=False, type='json', auth='public')
    def fetch_total_users(self):
        customers = request.env['res.users'].sudo().search([])
        users = []
        for customer in customers:
            users.append({
                'user': customer.id,
                'name': customer.name,
                'login': customer.login
            })
        return {
            'result': True,
            'users': users
        }

    @http.route('/api/', type='json', auth='public', csrf=False, methods=['POST'])
    def my_function(self, **data):
        pass




