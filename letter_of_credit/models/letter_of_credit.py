from odoo import models, api, fields, _
from odoo.exceptions import UserError


class LetterOfCredit(models.Model):
    _name = 'letter.of.credit'
    _description = 'Letter of Credit'
    _inherit = _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    

    name = fields.Char(readonly=True, string='#', default=_('New'), tracking=True, copy=False)
    number = fields.Char(string=_('LC Number'), copy=False)
    date_issue = fields.Date(readonly=True, string=_('LC Date of Issue'), copy=False)
    date_expiry = fields.Date(string=_('Expiry Date'), copy=False)
    amount = fields.Float(string='Amount')
    remaining_amount = fields.Float(string='Remaining', compute='get_remaining_amount')
    partner_id = fields.Many2one('res.partner', string=_('Applicant of LC'), required=True, tracking=True)
    phone = fields.Char(string=_('Phone'), related='partner_id.phone')
    email = fields.Char(string=_('Email'), related='partner_id.email')
    work_email = fields.Char(string=_('Work Email'))
    notify_befoer_period = fields.Integer(string=_('Notify Before'))
    date_shipment = fields.Date(string=_('Last Date of Shipment'), copy=False)
    shipment_address = fields.Many2one('res.partner', string=_('Receipt or Dispach Address'), tracking=True)
    shipment_address_street = fields.Char(string=_('Stree'), readonly=True, related='shipment_address.street')
    shipment_address_phone = fields.Char(string=_('Phone'), readonly=True, related='shipment_address.phone')
    partial = fields.Boolean(string=_('Partial Shipment'))
    bank_charges = fields.Selection([
        ('customer', 'Customer'),
        ('beneficiary', 'Beneficiary')
    ], string='Bank Charges')
    sign_infos = fields.Html(string=_('Sign Infos'), copy=False)
    commercial_invoice_notes = fields.Html(string=_('Commercial Invoice Notes'), copy=False)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'), ('cancel', 'Canceled')], string=_('Status'), default='draft', copy=False)
    notification_mail_sent = fields.Boolean()

    company_id = fields.Many2one('res.company', string=_("Company"), default=lambda self: self.env.company)

    sale_order_ids = fields.One2many('sale.order', 'letter_of_credit_id', string=_('Sale Orders'), copy=False)
    sale_order_count = fields.Integer(compute='get_count')
    picking_ids = fields.One2many('stock.picking', 'letter_of_credit_id', string=_('Pickings'), copy=False)
    picking_count = fields.Integer(compute='get_count')

    @api.depends('sale_order_ids.state', 'amount')
    def get_remaining_amount(self):
        for rec in self:
            rec.remaining_amount = rec.amount - sum(rec.sale_order_ids.filtered(lambda order: order.state in ['sale', 'done']).mapped('amount_untaxed'))

    @api.depends('sale_order_ids')
    def get_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_ids)
            rec.picking_count = len(rec.picking_ids)

    @api.onchange('date_expiry', 'notify_befoer_period')
    def onchnage_date_expiry(self):
        self.notification_mail_sent = False
    

    def action_new_sale_order(self):
        action =  {
            'name': _('Sale Orders'),
            'res_model': 'sale.order',
            'type': 'ir.actions.act_window',
            'domain': [('letter_of_credit_id', '=', self.id)],
            'context': {'default_have_lc': True, 'default_letter_of_credit_id': self.id, 'default_partner_id': self.partner_id.id},
            'target': 'current',
            'view_mode': 'tree,form'
        }
        return action

    def action_view_picking(self):
        action =  {
            'name': _('Pickings'),
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window',
            'domain': [('letter_of_credit_id', '=', self.id)],
            'context': {'create': False},
            'target': 'current',
            'view_mode': 'tree,form'
        }
        return action
    
    def action_confirm(self):
        if self.name == _('New'):
            self.name = self.env['ir.sequence'].next_by_code('letter.of.credit.sequence')
        self.state = 'confirm'
        self.date_issue = fields.Date.today()

    def action_draft(self):
        if self.picking_ids or self.sale_order_ids:
            raise UserError(_("There are linked sale orders or pickings. Cancel them first."))
        self.state = 'draft'
        self.date_issue = False

    def action_cancel(self):
        # What will happen when we cancel an LC?
        pass


    def send_notification_email_for_expiry(self):
        for lc in self:

            if not lc.date_expiry or lc.notification_mail_sent:
                continue
            today = fields.Date.today()
            diff_days = (lc.date_expiry - (today)).days
            
            if diff_days < lc.notify_befoer_period:
                template_id = self.env.ref('letter_of_credit.lc_expiry_notification').id

                mail_id = self.env['mail.template'].browse(template_id).send_mail(lc.id)
                lc.notification_mail_sent = True


