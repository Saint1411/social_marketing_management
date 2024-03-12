from odoo import fields, models, api


class OmniContact(models.Model):
    _name = "co_omni.contact"
    _inherit = ["image.mixin"]
    _description = "Omni contact"

    name = fields.Char(
        string="Name",
        required=True
    )

    external_id = fields.Char(
        string="User ID",
        required=True
    )

    gender = fields.Selection([
        ("male", "Male"),
        ("female", "Female")
    ])

    phone = fields.Char(string="Phone Number")

    channel_ids = fields.One2many(
        comodel_name="co_omni.channel",
        inverse_name="contact_id",
        string="Channels"
    )

    def go_to_channel_by_contact(self):
        action = self.env.ref("co_omni.co_omni_channel_view_act_window").read()[0]

        action.update({


        })

        return {
            "type": "ir.actions.act_window",
            "name": f"Channel of {self.name}",
            "res_model": "co_omni.channel",
            "view_mode": "kanban,tree,form",
            "views": [
                [self.env.ref("co_omni.co_omni_channel_kanban_view").id, "kanban"],
                [self.env.ref("co_omni.co_omni_channel_form_view").id, "form"],
                [self.env.ref("co_omni.co_omni_channel_tree_view").id, "tree"],
            ],
            "domain": [("contact_id", "=", self.id)],
            "context": dict(self._context)
        }
