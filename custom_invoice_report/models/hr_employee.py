from odoo import models, api, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    arabic_name = fields.Char(string='Arabic Name')