import frappe
import json
from frappe.utils import today
from frappe import _


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
                doc.status = "Pending"
                # frappe.db.set_value("Material Request",doc.name,'workflow_state',"Approved By PM{}".format(pm_name))
                doc.docstatus = 1
                return True
            else:
                frappe.throw(_("Document must be approved by {0}").format(pm_name))
                doc.status = "Pending"
                return False



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
                doc.status = "Pending"
                # doc.save()
                return True
            else:
                frappe.throw(_("Document must be approved by {0}").format(pm_name))
                doc.status = "Pending"
                return False






def accept():
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
                doc.approved_by_project_manager = pm_name
                doc.workflow_state = "Approved"
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
                    # doc.approved_by_project_manager = doc.document_created_by
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

def Validating_approver(doc, method=None):
    email = frappe.db.get_value("User",frappe.session.user,'email' )
    if email == doc.approved_by_project_manager:
        doc.approver_role = 'Project Manager'
        doc.approver_address = frappe.db.get_value("Contact", email, 'address' )
        doc.date_and_time = today()
        doc.docstatus = 1
    else:
        doc.docstatus = 0
        frappe.msgprint("For Submit the Document Approval Required By {0}".format(doc.approved_by_project_manager))