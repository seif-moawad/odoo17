from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Project(models.Model):
    _name = 'tb.project'

    name = fields.Char(required=1, string="Project Name")
    client_name = fields.Char(required=1, string="Client Name")
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Stage', default='draft',)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
        ('2', 'Critical'),
    ], string='Priority', default='0')
    start_date = fields.Date(string='Start Date', required=1)
    end_date = fields.Date(string='End Date', required=1)
    total_budget = fields.Float(string='Total Budget (USD)')

    freelancer_id = fields.Many2one(comodel_name='tb.freelancer')
    task_ids = fields.One2many(comodel_name='tb.task',inverse_name='project_id')

    @api.constrains(total_budget)
    def _check_total_budget(self):
        if self.total_budget <= 0:
            raise ValidationError("Total Budget must be greater than 0")