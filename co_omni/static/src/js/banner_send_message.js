odoo.define("co_omni.banner_send_message", function (require) {
    "use strict";

    const ListController = require('web.ListController');
    const ListView = require('web.ListView');
    const viewRegistry = require('web.view_registry');
    const core = require("web.core");
    const _t = core._t;

    const TreeCreateMessengerButton = ListController.extend({
        buttons_template: "button_co_omni_message.buttons",
        events: _.extend({}, ListController.prototype.events, {
            "click .open_wizard_create_message": "_openWizardCreateMessage",
            "click #btn_create_message": "_createMessage",
        }),

        _openWizardCreateMessage: function () {
            this.do_action({
                type: "ir.actions.act_window",
                res_model: "co_omni.message.wizard",
                name: "Create Message",
                view_mode: "form",
                view_type: "form",
                views: [[false, "form"]],
                target: "new",
                res_id: false,
            });
        },

        _makeAlert: function (type, title, message) {
            const alertResult = $("#alert_result");
            alertResult.html(`<div class="alert alert-${type} alert-dismissible fade show  mb-0 h-100  d-flex align-items-center" role="alert">
                <p class="mb-0"><strong>${title}!</strong> ${message}</p>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <i class="fa fa-close"/>
                </button>
            </div>`);
        },

        _getViewsList: async function () {
            try {
                const response = await this._rpc({
                    model: "ir.model.data",
                    method: "xmlid_to_res_model_res_id",
                    args: ['co_omni.view_co_omni_message_tree_with_onboarding'],
                });

                return response[1] || false;

            } catch (error) {
                console.error(error);
                return false;
            }
        },

        _createMessage: async function () {
            const self = this;
            const content = $("textarea#message_content").val();
            const context = this.model.get(this.handle).getContext();
            const messages = context["message_ids"] || [];

            if (!content) {
                self._makeAlert(
                    "danger",
                    "Excuse me",
                    "Please typing something to send..."
                );
            } else {
                const messageIDS = messages.map(message => message.id);

                try {
                    await this._rpc({
                        model: "co_omni.message",
                        method: "create",
                        args: [{
                            channel_id: context["channel_id"],
                            content: content,
                            sender_name: messages[0]["receiver_name"],
                            receiver_name: messages[0]["sender_name"],
                            receiver_id: messages[0]["sender_id"],
                            sender_id: messages[0]["receiver_id"],
                            type: "send"
                        }],
                    }).then(async (result) => {
                        const new_massages = [result, ...messageIDS];
                        await this.do_action({
                            type: "ir.actions.act_window",
                            res_model: "co_omni.message",
                            name: context["name"],
                            view_mode: "list,form",
                            view_type: "tree",
                            views: [
                                [await this._getViewsList(), "list"],
                                [false, "form"]
                            ],
                            target: "current",
                            domain: [["id", "in", new_massages]]
                        }).then(() => {
                            this.trigger_up("show_effect", {
                                message: "Send message successfully!",
                                type: "rainbow_man",
                            });
                            self._makeAlert(
                                "success",
                                "Congratulations",
                                "The message has been sent successfully!"
                            );
                        });
                    }).catch((error) => {
                        console.error("Error while creating records:", error);
                    });
                } catch (error) {
                    console.error("Error while creating records:", error);
                }
            }
        },

    });

    const OmniMessenger = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: TreeCreateMessengerButton,
        }),

    });

    viewRegistry.add("btn_wizard_create_message", OmniMessenger);

});