from odoo import http
from odoo.http import request


class OnboardingController(http.Controller):
    @http.route('/co_omni/co_omni_message_onboarding_panel', auth='user', type='json')
    def sale_quotation_onboarding(self):
        return {
            "html": request.env.ref("co_omni.co_omni_message_onboarding_panel")._render({})
        }
