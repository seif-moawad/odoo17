from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TBFreelancer(models.Model):
    _name = 'tb.freelancer'

    _inherit = ['mail.thread', 'mail.activity.mixin']
    #            ↑                ↑
    #            messages          activity buttons
    #            & followers       (schedule call etc.)

    name = fields.Char(string='Name', required=True,
                       tracking=True)  # ← tracking logs changes
    #   in the chatter

    email = fields.Char(string='Email', required=True,
                        tracking=True)

    phone = fields.Char(string='Phone', required=True)

    daily_rate = fields.Float(string='Daily Rate',
                              required=True,
                              tracking=True)

    status = fields.Selection([
        ('available',   'Available'),
        ('busy',        'Busy'),
        ('unavailable', 'Unavailable'),
    ], string="Status", default='available')

    skill_ids = fields.Many2many(comodel_name='tb.skill')

    @api.constrains('daily_rate')
    def _check_daily_rate(self):
        if self.daily_rate <= 0:
            raise ValidationError("Daily Rate must be greater than 0")
