from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class Project(models.Model):
    _name = 'tb.project'

    name = fields.Char(required=1, string="Project Name")
    client_name = fields.Char(required=1, string="Client Name")
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
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


    def action_activate(self):
        """
        Draft → Active
        Rules:
        - Must have a freelancer assigned
        - Must have at least one task
        - Budget must be above zero
        """
        for rec in self:

            # guard: wrong stage
            if rec.stage != 'draft':
                raise UserError(
                    'Only a Draft project can be activated.'
                )

            # guard: no freelancer
            if not rec.freelancer_id:
                raise UserError(
                    'Please assign a freelancer before activating '
                    'the project.'
                )

            # guard: no tasks
            if not rec.task_ids:
                raise UserError(
                    'Please add at least one task before activating '
                    'the project.'
                )

            # guard: zero budget
            if rec.total_budget <= 0:
                raise UserError(
                    'Project budget must be greater than zero.'
                )

            # all checks passed — move to Active
            rec.stage = 'active'

    def action_complete(self):
        """
        Active → Completed
        Rules:
        - Project must be Active
        - All tasks must be marked as done
        """
        for rec in self:

            # guard: wrong stage
            if rec.stage != 'active':
                raise UserError(
                    'Only an Active project can be completed.'
                )

            # guard: unfinished tasks
            unfinished = rec.task_ids.filtered(
                lambda t: not t.is_done
            )
            if unfinished:
                raise UserError(
                    f'Cannot complete the project. '
                    f'{len(unfinished)} task(s) are not done yet:\n'
                    + '\n'.join(f'  • {t.name}' for t in unfinished)
                )

            # all checks passed — move to Completed
            rec.stage = 'completed'

    def action_cancel(self):
        """
        Active → Cancelled
        Rules:
        - Cannot cancel a Completed project
        """
        for rec in self:

            # guard: already completed
            if rec.stage == 'completed':
                raise UserError(
                    'A completed project cannot be cancelled.'
                )

            # guard: already cancelled
            if rec.stage == 'cancelled':
                raise UserError(
                    'This project is already cancelled.'
                )

            # move to Cancelled
            rec.stage = 'cancelled'

    def action_reset_to_draft(self):
        """
        Cancelled → Draft
        Allows restarting a cancelled project
        """
        for rec in self:

            if rec.stage != 'cancelled':
                raise UserError(
                    'Only a Cancelled project can be reset to Draft.'
                )

            rec.stage = 'draft'

    @api.constrains(total_budget)
    def _check_total_budget(self):
        if self.total_budget <= 0:
            raise ValidationError("Total Budget must be greater than 0")