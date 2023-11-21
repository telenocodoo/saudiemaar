from odoo import models, api, fields, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    letter_of_credit_id = fields.Many2one('letter.of.credit', string=_('LC'))
    