from odoo import conf, http
from odoo.http import request

class ManufacturingApi(http.Controller):

    @http.route('/api/fetch_bom/<int:product_id>', type='json', csrf=False, methods=['POST'], auth='public')
    def fetch_bom(self, product_id):
        product = request.env['product.template'].sudo().browse(product_id)
        bom_list = product.bom_ids.sudo()

        components = []
        ready_to_produce_candidates = []

        for bom in bom_list:
            bom_lines = bom.bom_line_ids.sudo()

            for line in bom_lines:
                component = line.product_id
                required_qty = line.product_qty
                available_qty = component.qty_available

                components.append({
                    'component': component.name,
                    'component_id': component.id,
                    'required_qty': required_qty,
                    'available_qty': available_qty
                })

                if required_qty > 0:
                    ready_to_produce_candidates.append(available_qty / required_qty)

        # Calculate minimum of asssll component ratios
        ready_to_produce = int(min(ready_to_produce_candidates)) if ready_to_produce_candidates else 0
        
        return {
            "result": True,
            "product name": product.name,
            "components": components,
            "ready_to_produce": ready_to_produce
        }

