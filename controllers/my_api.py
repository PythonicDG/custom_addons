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

            return {'message': 'data uploaed', 'records': record.id}    


        @http.route('/api/my_model/read_data', type='json', auth='public', methods=['POST'], csrf=False)
        def read_data(self):
            
            records = request.env['my.model'].sudo().search([])

            record_names = [record.name for record in records]
            

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
