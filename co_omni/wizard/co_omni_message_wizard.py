from odoo import fields, models, _


class CoOmniMessengerWizard(models.TransientModel):
    _name = "co_omni.message.wizard"
    _description = "Co Omni Messenger Wizard"

    channel_id = fields.Many2one(
        comodel_name="co_omni.channel",
        string="Channel",
        required=True
    )

    channel_code = fields.Char(
        "Channel ID",
        related="channel_id.external_id"
    )

    content = fields.Char(string="Content", required=True)

    sender_id = fields.Char(string="Sender ID", required=True)
    receiver_id = fields.Char(string="Receiver ID", required=True)

    def create_omni_messenger(self):
        omni_messenger = self.env["co_omni.message"].sudo()

        res = omni_messenger.create({
            "channel_id": self.channel_id.id,
            "content": self.content,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
        })
        print(self.env.ref("co_omni.view_co_omni_message_tree_with_onboarding").id)

        if res:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Successfully"),
                    "type": "success",
                    "message": "A messenger was created!",
                    "sticky": False,
                    "next": {
                        "name": _("Omni Messenger"),
                        "view_mode": "list,form",
                        "res_model": "co_omni.message",
                        "views": [
                            (self.env.ref("co_omni.view_co_omni_message_tree_with_onboarding").id, "list"),
                            (False, "form")
                        ],
                        'type': 'ir.actions.act_window',
                        "context": {'search_default_group_by_channel_id': 1},
                        "target": "current"
                    },
                }
            }

        else:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": _("Warning"),
                    "type": "error",
                    "message": "You cannot create messenger now!",
                    "sticky": False,
                }
            }
