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

    custom_field_1 = fields.Boolean(string="Enable settings")
    custom_field_2 = fields.Char(string="custom_field_2")
    custom_field_3 = fields.Boolean(string="custom_field_3")

