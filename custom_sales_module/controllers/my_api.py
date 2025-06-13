from odoo import http
from odoo.http import request

class MyApi(http.Controller):

    def get_employee_hyerarchy(self, employee):
        heirarchy = {
            'name': employee.name,
            'work_email': employee.work_email,
            'Company': employee.company_id.name,
            'job_title': employee.job_id.name,
            'subordinates': [self.get_employee_hyerarchy(child) for child in employee.child_ids]
        }

        return heirarchy

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
        
        hierarchy = self.get_employee_hyerarchy(employee)

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



