# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Lead(models.Model):
    _inherit = "crm.lead"

    def create_lead_crm(self, recipient, record):
        """
        Create a lead in the CRM system based on the given record.
        This function takes 'record' as a parameter and does not return anything.
        """
        if not record.event_name.startswith("user"):
            return
        source = recipient
        utm_source = self.env['utm.source'].sudo()
        data = utm_source.search([('name', '=', source)])
        if not data:
            data = utm_source.create({'name': source})
        name = f"{record.sender}/{record.sender_id}_{data.name}"
        zalo_id = record.sender_id
        crm_rs = self.env["crm.lead"].sudo()

        unique_id = f"{record.sender_id}_zalo"
        if not crm_rs.search([("contact_name", "ilike", unique_id)]).ids:
            vals = dict(contact_name=name,
                        name=name,
                        zalo_id=zalo_id,
                        source_id=int(data),
                        type="lead")
            crm_rs.create(vals)
        else:
            for lead in crm_rs.search([("contact_name", "ilike", unique_id)]):
                lead.write(dict(contact_name=name))
