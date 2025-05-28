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
    

class Students(models.Model):
    _name = "students.model"
    _description = "This is Stduents model"

    first_name = fields.Char("First Name", required=True)
    last_name = fields.Char("Last Name")
    phone_number = fields.Integer("Phone Number")
    department = fields.Char("Department")