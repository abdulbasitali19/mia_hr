import frappe
from frappe.permissions import add_user_permission


def add_user_permissions(doc, handler=None):
    add_user_permission(doc.doctype, doc.name, doc.pm_name,True)
    add_user_permission(doc.doctype, doc.name, doc.project_admin,True)
    add_user_permission(doc.doctype, doc.name, doc.management,True)
    add_user_permission(doc.doctype, doc.name, doc.store_keeper,True)

def remove_user_permissions(doc, handler=None):
    remove_user_permission(doc.doctype, doc.name, frappe.db.get_value(doc.doctype, doc.name, 'pm_name'))
    remove_user_permission(doc.doctype, doc.name,frappe.db.get_value(doc.doctype, doc.name, 'project_admin'))
    remove_user_permission(doc.doctype, doc.name,frappe.db.get_value(doc.doctype, doc.name, 'management'))
    remove_user_permission(doc.doctype, doc.name,frappe.db.get_value(doc.doctype, doc.name, 'store_keeper'))


def remove_user_permission(doctype, name, user):
	user_permission_name = frappe.db.get_value(
		"User Permission", dict(user=user, allow=doctype, for_value=name)
	)
	frappe.delete_doc( doctype = "User Permission", name = user_permission_name, ignore_permissions=True)