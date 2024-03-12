from odoo import fields, models, api
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


def convert_timestamp_to_datetime(timestamp):
    try:
        # Chuyển đổi timestamp thành đối tượng datetime
        dt_object = datetime.utcfromtimestamp(timestamp)
        return dt_object
    except Exception as e:
        # Xử lý ngoại lệ nếu có lỗi
        print("Lỗi khi chuyển đổi timestamp:", str(e))
        return None


class OmniMessage(models.Model):
    _name = "co_omni.message"
    _description = 'Omni Message'
    _order = "timestamp DESC, id DESC"
    _rec_name = "channel_id"

    channel_id = fields.Many2one(
        comodel_name="co_omni.channel",
        string="Channel"
    )

    channel_code = fields.Char(
        "Channel ID",
        related="channel_id.external_id"
    )

    contact_id = fields.Many2one(
        comodel_name="co_omni.contact",
        related="channel_id.contact_id",
        string="Partner"
    )

    content = fields.Char(string="Content")

    timestamp = fields.Datetime(
        string="Timestamp",
        default=fields.Datetime.now()
    )

    sender_name = fields.Char(string="Sender")
    sender_id = fields.Char(string='Sender ID')
    receiver_name = fields.Char(string="Receiver")
    receiver_id = fields.Char(string='Receiver ID')

    user_id = fields.Many2one(
        comodel_name="res.users",
        default=lambda self: self.env.user,
        string="Responsible"
    )

    type = fields.Selection([
        ("send", "Send"),
        ("receive", "Receive")
    ], string="Type")

    account_id = fields.Many2one(
        comodel_name="co_omni.account",
        related="channel_id.account_id",
        string="Account"
    )

    def save_message(self, body):
        _logger.warning("Api server pancake response: " + str(body))

        try:
            channel_id = self._get_channel_id(body)


            vals = {
                'channel_id': channel_id.id,
                'content': body.get('content'),
                'timestamp': datetime.now(),
                'type': body.get('type'),
                'sender_name': body.get('sender'),
                'receiver_name': body.get('recipient'),
                'sender_id': body.get('sender_id'),
                'receiver_id': body.get('recipient_id'),
            }

            self.sudo().create(vals)

        except Exception as e:
            _logger.error("Save message error: " + str(e))

    def _get_channel_id(self, body):
        channel_id = self.env['co_omni.channel'].sudo().search([('external_id', '=', body.get('channel_id'))])
        pan_page_id = self._get_pan_page_id(body)
        source_id = self._get_source_id(body)
        contact_id = self._get_contact_id(body)

        if contact_id:
            self._update_partner_phone(contact_id)

        if not channel_id:
            channel_id = self.env['co_omni.channel'].sudo().create({
                'name': body.get('channel'),
                'external_id': body.get('channel_id'),
                'account_id': pan_page_id.id,
                'utm_source_id': source_id.id,
                'contact_id': contact_id.id
            })

        return channel_id

    def _get_pan_page_id(self, body):
        pan_page_id = self.env['co_omni.account'].sudo().search([('name', '=', body.get('fan_page'))])
        source_id = self._get_source_id(body)

        if not pan_page_id:
            pan_page_id = self.env['co_omni.account'].sudo().create({
                'name': body.get('fan_page'),
                'external_id': body.get('account_id'),
                'utm_source_id': source_id.id
            })

        return pan_page_id

    def _get_source_id(self, body):
        source_id = self.env['utm.source'].sudo().search([('name', '=', body.get('fan_page'))])

        if not source_id:
            source_id = self.env['utm.source'].sudo().create({
                'name': body.get('fan_page'),
            })

        return source_id

    def _get_contact_id(self, body):
        contact_id = self.env['co_omni.contact'].sudo().search([('external_id', '=', body.get('contact_id'))])

        if not contact_id:
            contact_id = self.env['co_omni.contact'].sudo().create({
                'name': body.get('channel'),
                'external_id': body.get('contact_id'),
            })

        return contact_id

    def _update_partner_phone(self, contact_id):
        partner = self.env['res.partner'].sudo().search([('zalo_id', '=', contact_id.external_id)])

        if partner:
            vals = {
                'phone': partner.phone
            }
            contact_id.write(vals)

