from odoo import fields, models, api


class OmniAccount(models.Model):
    _name = "co_omni.account"
    _inherit = ["image.mixin"]
    _description = "Omni Account"

    name = fields.Char(
        string="Name",
        required=True
    )

    new_message_count = fields.Integer(
        string="New Message Count",
        compute="compute_new_message_count"
    )

    new_channel_count = fields.Integer(string="New Channel Count")

    external_id = fields.Char(
        string="Account ID",
        required=True
    )

    utm_source_id = fields.Many2one(
        comodel_name="utm.source",
        string="Source"
    )

    new_message = fields.Char(
        string="New Message",
        readonly=True
    )

    unread_message = fields.Char(
        string="Unread Message",
        compute="compute_new_message",
        readonly=True
    )

    unanswered_message = fields.Char(
        string="Unanswered Message",
        readonly=True
    )

    latest_message = fields.Datetime(string="Latest Message")

    channel_ids = fields.One2many(
        comodel_name="co_omni.channel",
        inverse_name="account_id",
        string="Channel"
    )

    _sql_constraints = [
        ("external_id_uniq", 'UNIQUE (external_id)', "The Account ID must be unique!"),
    ]

    def action_redirect_to_channel(self):
        return {
            "type": "ir.actions.act_window",
            "name": f"Channel of {self.name}",
            "res_model": "co_omni.channel",
            "view_mode": "tree",
            "target": "current",
            "domain": [("id", "in", self.channel_ids.ids)],
            "view_id": self.env.ref("co_omni.co_omni_channel_tree_view").id,
        }

    @api.depends("channel_ids")
    def compute_new_message_count(self):
        for record in self:
            new_message_count = len(record.channel_ids.filtered(
                lambda c: c.status == "unread")
            ) or 0

            record.new_message_count = new_message_count

    @api.depends("channel_ids")
    def compute_new_message(self):
        for record in self:
            message_count_text = f"{record.new_message_count}/{len(record.channel_ids)}"
            unread_message = message_count_text if len(record.channel_ids) > 0 else "0/0"
            record.unread_message = unread_message
