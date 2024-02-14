import frappe
import json
import psutil
from frappe import _
from frappe.utils import now
from frappe.custom.doctype.property_setter.property_setter import make_property_setter


def setting_first_approver(doc, method=None):
    if doc.cost_center and not doc.approval_stage:
        approver = getting_transition_data(doc.cost_center)
        doc.approval_stage = approver.get("approver_1")


def updated_only_by_owner(doc, method=None):
    if frappe.session.user == doc.owner and doc.rejected == 1:
        doc.remarks_for_rejection = ""
        doc.rejected = 0
        doc.workflow_state = "Draft"


@frappe.whitelist()
def purchase_order_approved(doc):
    doc = frappe.get_doc("Purchase Order", doc)
    document_approval_workflow = frappe.get_doc(
        "Documents Approval Workflow", {"document": "Purchase Order"}
    )
    transition_state = getting_transition_data(doc.cost_center)
    if not doc.approval_stage:
        doc.approval_stage = transition_state.get("approver_1")

    if (
        frappe.session.user == doc.approval_stage
        and frappe.session.user == transition_state.get("approver_1")
    ):
        if transition_state.get("approver_2") is not "":
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_1,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_1")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = transition_state.get("approver_2")
            doc.docstatus = 0
            doc.workflow_state = "Draft"
            doc.save()
            return True
        else:
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_1,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_1")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = ""
            doc.workflow_state = "Approved"
            doc.submit()
            return True

    elif (
        frappe.session.user == doc.approval_stage
        and frappe.session.user == transition_state.get("approver_2")
    ):
        if transition_state.get("approver_3") is not "":
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_2,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_2")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = transition_state.get("approver_3")
            doc.docstatus = 0
            doc.workflow_state = "Draft"
            doc.save()
            return True
        else:
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_2,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_2")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = ""
            doc.workflow_state = "Approved"
            doc.submit()
            return True

    elif (
        frappe.session.user == doc.approval_stage
        and frappe.session.user == transition_state.get("approver_3")
    ):
        if transition_state.get("approver_4") is not "":
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_3,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_3")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = transition_state.get("approver_4")
            doc.docstatus = 0
            doc.workflow_state = "Draft"
            doc.save()
            return True
        else:
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_3,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_3")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = ""
            doc.workflow_state = "Approved"
            doc.submit()
            return True

    elif (
        frappe.session.user == doc.approval_stage
        and frappe.session.user == transition_state.get("approver_4")
    ):
        if transition_state.get("approver_5") is not "":
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_4,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_4")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = transition_state.get("approver_5")
            doc.docstatus = 0
            doc.workflow_state = "Draft"
            doc.save()
            return True
        else:
            doc.append(
                "transition_table",
                {
                    "role": document_approval_workflow.approver_4,
                    "approved": 1,
                    "approving_date": now(),
                    "user": frappe.session.user,
                    "transition_detail": "Purchase approved by {0}".format(
                        transition_state.get("approver_4")
                    ),
                },
            )
            doc.documnet_currently_update_by = frappe.session.user
            doc.approval_stage = ""
            doc.workflow_state = "Approved"
            doc.submit()
            return True
    else:
        frappe.throw("Document  Must be approved by {0}".format(doc.approval_stage))


@frappe.whitelist()
def purchase_order_reject(doc):
    doc = frappe.get_doc("Purchase Order", doc)
    if (
        frappe.session.user == doc.approval_stage
        or frappe.session.user == "Administrator"
    ):
        return True
    else:
        throw("Document Should Be Rejected By {0}".format(doc.approval_stage))


def getting_transition_data(cost_center):
    transition_dict = {}
    role_base_dict = {}
    cost_center_role_dict = {}
    document_approval_workflow = frappe.get_doc(
        "Documents Approval Workflow", {"document": "Purchase Order"}
    )
    cost_center = frappe.get_doc("Cost Center", cost_center)

    if cost_center:
        cost_center_role_dict = {
            "Project Admin": cost_center.project_admin,
            "PM": cost_center.pm_name,
            "Management": cost_center.management,
            "Store Keeper": cost_center.store_keeper,
        }

    if document_approval_workflow:
        role_base_dict = {
            f"approver_{i}": getattr(document_approval_workflow, f"approver_{i}", None)
            for i in range(1, 6)
        }

    for key, value in role_base_dict.items():
        transition_dict[key] = cost_center_role_dict.get(value, value)

    return transition_dict
