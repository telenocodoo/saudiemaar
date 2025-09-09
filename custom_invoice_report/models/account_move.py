from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def to_indian_numerals(self, num):
        if not num:
            return ''
        western_to_indian = {
            '0': '٠',
            '1': '١',
            '2': '٢',
            '3': '٣',
            '4': '٤',
            '5': '٥',
            '6': '٦',
            '7': '٧',
            '8': '٨',
            '9': '٩'
        }
        return ''.join(western_to_indian.get(d, d) for d in str(num)) or ''
    