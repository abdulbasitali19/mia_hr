frappe.ui.form.on('Material Request', {
    validate:function(frm){
        frm.set_value("document_currently_updated_by",frappe.session.user)
    },
    onload: function (frm) {
        if (!frm.is_new() && frappe.session.user != "Administrator" && frappe.session.user != frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
            $(".inner-group-button[data-label='Actions'] > button").hide();

        }

        if (frm.doc.rejected == 1 &&  !frm.is_new() && frappe.session.user != "Administrator" && frappe.session.user == frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
            $(".inner-group-button[data-label='Actions'] > button").hide();

        }


        if (frm.doc.rejected == 0 && frappe.session.user != "Administrator" && frappe.session.user == frm.doc.approval_stage) {
            $("button[data-label='Submit']").hide();
            $('.primary-action').prop('disabled', true);
            // $(".inner-group-button[data-label='Actions'] > button").hide();

        }


        if (frm.doc.workflow_state) {
            if (frm.doc.workflow_state == "Rejected" && frm.doc.rejected == 1) {
                frm.set_intro(`Rejected By ${frm.doc.approval_stage}`, 'red')
            }

            if (frm.doc.workflow_state == "Approved") {
                frm.set_intro(`Approved By ${frm.doc.document_currently_updated_by}`, 'green')
                      
             }
        }
        
    },

    refresh: function (frm) {
        frm.add_custom_button(__('Approved'), function () {
            frappe.call({
                method: "mia_hr.overrides.material_request.Accepting_from_custom_approver_material_request",
                args: {
                    material_request: frm.doc.name
                },
                callback: function (r) {
                    r = r.message
                    if (r == true) {
                        frm.reload_doc();
                        frappe.set_route('app/material-request')
                    }
                }
            });
        }, __("Actions"));


        frm.add_custom_button(__('Reject'), function () {
            frappe.call({
                method: "mia_hr.overrides.material_request.Rejecting_from_custom_approver_material_request",
                args: {
                    material_request: frm.doc.name
                },
                callback: function (r) {
                    r = r.message
                    if (r == true) {
                        frm.reload_doc();
                        frappe.set_route('app/material-request')    
                    }
                    else {
                        frappe.prompt({
                            title :'Remarks',
                            label: 'Provide Valid reason for rejection',
                            fieldname: 'reject_remark',
                            fieldtype: 'Small Text'
                        }, (values) => {
                            frm.set_value("remarks_for_rejection",values.reject_remark )
                            frm.set_value("workflow_state","rejected" )
                            frm.set_value("rejected",1)
                            frm.set_value("approval_stage", "")
                            frm.set_value("document_currently_updated_by", frappe.session.user)
                            frm.save();
                            frappe.set_route('app/material-request')
                        })
                    }
                }
            });

        }, __("Actions"));
    }




},

)
