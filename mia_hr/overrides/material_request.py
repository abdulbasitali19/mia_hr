import frappe
import json
from frappe.utils import today
from frappe import _


def check(doc, method=None):
    if frappe.session.user == doc.owner and doc.rejected == 1:
        doc.remarks_for_rejection = " "
        doc.rejected = 0
        doc.workflow_state = "Draft"


@frappe.whitelist()
def Accepting_from_custom_approver_material_request(material_request):
    if material_request:
        doc = frappe.get_doc("Material Request",material_request)
        approver_1 = frappe.db.get_value("Documents Approval Workflow", {'document': doc.get("doctype")},"approver_1")
        
        if approver_1 == "PM":
            pm_name = frappe.db.get_value("Cost Center", doc.get("cost_center"), "pm_name")
                
            if pm_name and frappe.session.user == pm_name:
                doc.approver_transition_detail = []
                doc.append('approver_transition_detail',{
                    "role": "Project Manager",
                    "user": pm_name,
                    "approving_date": today(),
                    "approver_mac_address": "",
                    "transition_detail": f"Approved By Project Manager {pm_name}",
                    "approved": 1
                })
                doc.workflow_state = "Approved"
                doc.rejected = 0
                doc.document_currently_updated_by = frappe.session.user
                doc.approval_stage = ""
                doc.submit()
                return True
            else:
                frappe.throw(_("Document must be approved by {0}").format(pm_name))
                doc.status = "Draft"
                return False
        else:
            frappe.throw(_("Approver is not Project Manager {0}").format(pm_name))
    else:
        raise Exception(_("{0} is missing").format('Material Request'))



@frappe.whitelist()
def Rejecting_from_custom_approver_material_request(material_request):
    if material_request:
        doc = frappe.get_doc("Material Request",material_request)
        approver_1 = frappe.db.get_value("Documents Approval Workflow", {'document': doc.get("doctype")},"approver_1")
        
        if approver_1 == "PM":
            pm_name = frappe.db.get_value("Cost Center", doc.get("cost_center"), "pm_name")
            
            if pm_name and frappe.session.user == pm_name:
                doc.approver_transition_detail = []
                doc.append("approver_transition_detail", {
                    "role": "Project Manager",
                    "user": pm_name,
                    "approving_date": today(),
                    "approver_mac_address": "",
                    "transition_detail": f"Rejected By Project Manager {pm_name}",
                    "approved": 0
                })
                if not doc.remarks_for_rejection:
                    # doc.approval_stage = doc.document_created_by
                    return False
                doc.workflow_state = "Rejected"
                doc.docstatus = 0
                doc.save()
                return True
            else:
                frappe.throw(_("Document must be Rejected by {0}").format(pm_name))
                doc.status = "Draft"
                return False
        else:
            frappe.throw(_("Approver is not Project Manager {0}").format(pm_name))
    else:
        raise Exception(_("{0} is missing").format('Material Request'))

