# -*- coding: utf-8 -*-
{
    'name': "Omni",
    'summary': "Omni",
    'description': "Omni",
    'author': "CloudMedia LLC",
    'website': "https://www.cloudmedia.vn",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ["base", "utm", 'crm'],
    "data": [
        "security/ir.model.access.csv",
        "views/omi_account_view.xml",
        "views/omi_channel_view.xml",
        "templates/footer_omni_message_view.xml",
        "views/omi_message_view.xml",
        "views/omi_contact_view.xml",
        "views/omi_sources.xml",
        "templates/assets.xml",
        "wizard/co_omni_message_wizard_view.xml",
        "views/menu.xml",
    ],
    "qweb": [
        "static/src/xml/create_message_button.xml",
        "static/src/xml/expand_buttons.xml",
    ],
    'installable': True,
    'application': True,
}
