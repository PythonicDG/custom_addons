from typing import Required
from odoo import models, fields

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Simple Model'

    name = fields.Char(required=True)
    description = fields.Text() 

class Cart(models.Model):
    _name = "cart.model"
    _description = "This is Cart Model"

    name = fields.Char("Title", required=True)
    company_name = fields.Char("Company Name")
    price = fields.Char("Price")
    