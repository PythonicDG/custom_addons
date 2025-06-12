import re
from werkzeug import Response
from odoo import http
from odoo.http import request
import json

class SimpleAPI(http.Controller):
        @http.route('/api/my_model', type='json', auth='public', methods=['POST'], csrf=False)
        def create_record(self, **data):
            
            name = data.get("name")

            if not name:
                return {'error': 'name is required'}

            description = data.get('description')
            
            record = request.env['my.model'].sudo().create({
                'name': name,
                'description': description,
            })

            return {'message': 'data uploaded', 'records': record.id}

        @http.route('/api/my_model/read_data', type='json', auth='public', methods=['POST'], csrf=False)
        def read_data(self):
            records = request.env['my.model'].sudo().search([])

            data = []
            for record in records:
                data.append({
                    'id': record.id,
                    'name': record.name,
                    'description': record.description
                })

            return {
                'status': 200,
                'message': 'Data fetched successfully',
                'count': len(data),
                'data': data
            }


        @http.route('/api/my_model/<int:res_id>/update', type='json', auth='public', methods=['POST'], csrf=False)
        def update_record(self, res_id, **data):
            record = request.env['my.model'].sudo().browse(res_id)

            if not record.exists():
                return {'error': 'Record not found'}

            updated_fields = {}

            if 'name' in data:
                updated_fields['name'] = data['name']

            if 'description' in data:
                updated_fields['description'] = data['description']

            if not updated_fields:
                return {'error': 'No fields to update'}

            record.write(updated_fields)

            return {
                'message': 'Record updated successfully',
                'record': {
                    'id': record.id,
                    'name': record.name,
                    'description': record.description
                }
            }
        
        @http.route('/api/my_model/<int:res_id>/delete_record', type='json', methods=['POST'], auth='public', csrf=False)
        def delete_data(self, res_id):
            if not res_id:
                return {"Error":"Please provide res id"}

            record = request.env['my.model'].sudo().browse(res_id)

            if not record.exists():
                return {"Error":"Records not found for this res_id"}

            record.sudo().unlink() #deletes the records using superuser privilleges. 

            return {'message': f'Record {res_id} deleted successfully'}

        @http.route('/api/students/register', type='json', methods=['POST'], auth='public', csrf=False)
        def register_student(self, **data):
            first_name = data.get("first_name")
            last_name = data.get("last_name")
            phone_number = data.get("phone_number")
            department = data.get("department")
            email = data.get("email")

            if not email:
                return {'error': 'email is required'}


            record = request.env['students.model'].sudo().create({
                'first_name': first_name,
                'last_name': last_name,
                'phone_number': phone_number,
                'department': department,
                'email': email,
            })

            try:
                template = request.env.ref('my_first_module.email_template_student_welcome_basic')

                if not template:
                    return {
                        'error': 'email template not found',
                    }

                context = {
                    'message': "Consociate Solutions welcomes you to the Company's Portal."
                }
                
                if template and record.email:
                    template.with_context(context).sudo().send_mail(
                        record.id,
                        force_send=True
                    )
                return {
                    'message': 'Student registered successfully',
                    'record_id': record.id,
                    'email_sent': True
                }

            except Exception as e:
                return {
                    "error": "failed to send email",
                    "message": str(e)
                }

        @http.route('/api/fetch_students', type='json', methods=['POST'], auth='public', csrf=False)
        def fetch_students(self):
            records = request.env['students.model'].with_context(lang='hi_IN').search([])

            data = []
            for record in records:
                data.append({
                    'id': record.id,
                    'first_name': record.first_name,
                    'last_name': record.last_name,
                    'phone_number': record.phone_number,
                    'department': record.department,
                    'email': record.email
                })
            return {
                'status': 200,
                'data': data,
                'message': 'Students fetched successfully',
            }