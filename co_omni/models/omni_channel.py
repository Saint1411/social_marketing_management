# -*- coding: utf-8 -*-
from odoo import models, fields, api


class OmniChannel(models.Model):
    _name = "co_omni.channel"
    _description = "Omni Channel"
    _order = "id DESC, name ASC"

    name = fields.Char(
        string="Name",
        required=True
    )

    external_id = fields.Char(string="Channel ID")

    account_id = fields.Many2one(
        comodel_name="co_omni.account",
        string="Account"
    )

    utm_source_id = fields.Many2one(
        comodel_name="utm.source",
        string="Source",
        related="account_id.utm_source_id"
    )

    contact_id = fields.Many2one(
        comodel_name="co_omni.contact",
        string="Contact"
    )

    kanban_state = fields.Selection([
        ("normal", "Read"),
        ("done", "Unread")], string="Kanban State",
        default="done")

    status = fields.Selection([
        ("unread", "Unread"),
        ("read", "Read"),
    ],
        string="Status",
        compute="compute_status"
    )

    message_ids = fields.One2many(
        comodel_name="co_omni.message",
        inverse_name="channel_id",
        string="Messenger ID"
    )

    last_message_id = fields.Many2one(
        comodel_name="co_omni.message",
        compute="compute_last_messenger_id",
        string="Last Messenger ID"
    )

    content = fields.Char(
        string="Content",
        related="last_message_id.content"
    )

    timestamp = fields.Datetime(
        string="Updated At",
        related="last_message_id.timestamp"
    )

    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Response By",
        related="last_message_id.user_id"
    )

    last_messenger_id_of_response = fields.Many2one(
        comodel_name="co_omni.message",
        compute="compute_last_messenger_id_of_response",
        string="Last Messenger ID Of Response"
    )

    response_at = fields.Datetime(
        string="Response At",
        related="last_messenger_id_of_response.timestamp"
    )

    def action_redirect_to_message(self):
        self.kanban_state = "normal"

        context = dict(
                self._context,
                message_ids=self.message_ids.read(
                    ["receiver_id", "receiver_name", "sender_name", "sender_id"]
                ),
                channel_id=self.id,
                name=f"Messenger of {self.name}"
            )

        return {
            "type": "ir.actions.act_window",
            "name": f"Messenger of {self.name}",
            "res_model": "co_omni.message",
            "view_mode": "list,form",
            "target": "current",
            "domain": [("id", "in", self.message_ids.ids)],
            "views": [
                (self.env.ref("co_omni.view_co_omni_message_tree_with_onboarding").id, "list"),
                (False, "form")
            ],
            "context": context
        }

    @api.depends("kanban_state")
    def compute_status(self):
        for record in self:
            record.status = "read" if record.kanban_state == "normal" else "unread"

    @api.depends("message_ids")
    def compute_last_messenger_id(self):
        for record in self:
            if record.message_ids:
                record.last_message_id = record.message_ids[0]
            else:
                record.last_message_id = False

    def compute_last_messenger_id_of_response(self):
        for record in self:
            messenger_ids_of_response = record.message_ids.filtered(lambda m: m.user_id == record.user_id)
            if messenger_ids_of_response:
                record.last_messenger_id_of_response = messenger_ids_of_response[0]
            else:
                record.last_messenger_id_of_response = False
