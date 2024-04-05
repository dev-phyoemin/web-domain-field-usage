from odoo import api, fields, models, _
import jsonclass AccountPayment(models.Model):
    _inherit = 'account.payment'

    user_id = fields.Many2one('res.users', string="User Id", default=lambda self: self.env.user)
    journal_id_domain = fields.Char(
        compute="_compute_journal_id_domain",
        readonly=True,
        store=False,
    )
    @api.depends('user_id.journal_ids')
    def _compute_journal_id_domain(self):
        print("............",self.user_id.id)
        for rec in self:
            if rec.user_id:
                rec.journal_id_domain = json.dumps(
                    [('journal_id', 'in', rec.user_id.journal_ids.ids)]
                )
                print("............", self.journal_id_domain)
            else:
                rec.journal_id_domain = False

    journal_id = fields.Many2one('account.journal', string='Journal', required=True, readonly=True, compute="_compute_journal_id_domain",
                                 states={'draft': [('readonly', False)]}, tracking=True
                                 )
