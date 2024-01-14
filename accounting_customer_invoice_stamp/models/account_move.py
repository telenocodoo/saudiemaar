from odoo import api, fields, models, tools, http, release, registry

class AccountMove(models.Model):
    _inherit = ['account.move']

    image_stamp = fields.Image(string="Stamp Image", max_width=80, max_height=80)


