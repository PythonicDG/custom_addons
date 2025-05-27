from typing import Required
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Simple Model'

    name = fields.Char(required=True)
    description = fields.Text() 