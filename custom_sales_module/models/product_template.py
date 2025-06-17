from odoo import models, fields, api
import re


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    slug = fields.Char(
        string="Slug",
        compute="_compute_slug",
        store=True,
        readonly=True,
        index=True
    )
    
    def convert_slug(self, text):

        if not isinstance(text, str):
            text = str(text)

        text = text.lower().strip()

        slug = re.sub(r'[^a-z0-9]+', '-', text)

        slug = re.sub(r'-{2,}', '-', slug)

        slug = slug.strip('-')

        return slug 


    @api.depends('name')
    def _compute_slug(self):
        for record in self:
            if record.name:
                record.slug = self.convert_slug(record.name)
            else:
                record.slug = ''

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    custom_field_1 = fields.Boolean(
        string="Enable Setting",
        config_parameter='custom_sales_module.custom_field_1'
    )
    
    custom_field_2 = fields.Char(
        string="Custom Field 2",
        config_parameter='custom_sales_module.custom_field_2'
    )
    
    custom_field_3 = fields.Boolean(
        string="Custom Field 3",
        config_parameter='custom_sales_module.custom_field_3'
    )



    # def set_values(self):
    #     super().set_values()
    #     self.env['ir.config_parameter'].sudo().set_param('custom_sales_module.custom_field_1', self.custom_field_1)
    #     self.env['ir.config_parameter'].sudo().set_param('custom_sales_module.custom_field_2', self.custom_field_2)
    #     self.env['ir.config_parameter'].sudo().set_param('custom_sales_module.custom_field_3', self.custom_field_3)

    # @api.model
    # def get_values(self):
    #     res = super().get_values()
    #     config = self.env['ir.config_parameter'].sudo()

    #     res.update(
    #         custom_field_1=config.get_param('custom_sales_module.custom_field_1') == 'True',
    #         custom_field_2=config.get_param('custom_sales_module.custom_field_2', default=''),
    #         custom_field_3=config.get_param('custom_sales_module.custom_field_3') == 'True',
    #     )
    #     return res






