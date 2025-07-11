from typing import Required
from odoo import models, fields, api

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
    _description = "Students Model"

    


    first_name = fields.Char(string='Name', translate=True, required=True)
    last_name = fields.Char("Last Name", translate=True)
    phone_number = fields.Char("Phone Number")
    department = fields.Char("Department", translate=True)
    email = fields.Char("Email--", required=True)

    # def create(self, vals_list):
    #    record = super(Students, self).create(vals_list)

    #    if record.email:
    #        subject = "Welcome to the students portal"
    #        body = "This is a test email body."

    #        mail_values = {
    #            'subject': subject,
    #            'body_html': body, 
    #            'email_to': record.email,
    #            'email_from': 'dipakgaikwadms@gmail.com'
    #        }
    #        self.env['mail.mail'].create(mail_values).send()

    #    return record

   
    
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

    module_students_custom_feature = fields.Boolean(
        string="Enable Student Feature"
    )