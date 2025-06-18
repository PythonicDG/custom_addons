from odoo import conf, http
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

    







