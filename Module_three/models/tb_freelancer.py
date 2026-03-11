from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TBFreelancer(models.Model):
    _name = 'tb.freelancer'

    name = fields.Char(required=1, string="Name")
    email = fields.Char(required=1, string="Email Address")
    phone = fields.Char(required=1, string="Phone Number")
    status = fields.Selection([
        ('available',   'Available'),
        ('busy',        'Busy'),
        ('unavailable', 'Unavailable'),
    ], string="Status", default='available')
    daily_rate = fields.Float(string="Daily Rate")

    skill_ids = fields.Many2many(comodel_name='tb.skill')

    @api.constrains('daily_rate')
    def _check_daily_rate(self):
        if self.daily_rate <= 0:
            raise ValidationError("Daily Rate must be greater than 0")
