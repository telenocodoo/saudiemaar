from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    arabic_name = fields.Char(string='Name in Arabic')
    street_arabic = fields.Char(string='Street in Arabic')
    street2_arabic = fields.Char(string='Neighbourhood in Arabic')
    city_arabic = fields.Char(string='City in Arabic')
    