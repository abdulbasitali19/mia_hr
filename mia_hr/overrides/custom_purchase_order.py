import frappe
from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder

class Custompurchaseorder(PurchaseOrder):
    def onload(self):
        pass
    
    def validate(self):
        self.create_transition_table_for_workflow()
   
    @frappe.whitelist()
    def set_transitions_roles(self):
        email = frappe.db.get_value("User", frappe.session.user, 'email')
        cost_center_detail = frappe.get_doc("Cost Center", self.cost_center)
        transition_table = self.transition_table

        if cost_center_detail.get("store_keeper") == email and len(transition_table) == 0:
            self.approved_purchase_order_by_shop_keeper(email)
        

        elif email == cost_center_detail.get("project_admin")  and len(transition_table) == 1:
            self.approved_purchase_order_by_project_admin(email)
            

        elif cost_center_detail.get("management") == email  and len(transition_table) == 2:
            self.approved_purchase_order_by_management(email)
        
        
        elif cost_center_detail.get("pm_name") == email  and len(transition_table) == 3:
            self.approved_purchase_order_by_project_manager(email)

        else: 
            if len(self.transition_table) == 0 and frappe.session.user !="Administrator" : 
                frappe.throw("Document  Must be approved by Shopkeeper")
            elif len(self.transition_table) == 1 :
                frappe.throw("Document Must be approved by project Admin")
            elif len(self.transition_table) == 2:
                frappe.throw("Document Must be approved by Management")
            else:
                frappe.throw("Document Must be Submit by Project Manager")




    def approved_purchase_order_by_shop_keeper(self, email):
        if email:
            self.append("transition_table", {
                    "role": "Shop Keeper",
                    "approved": 1,
                    "user": email,
                    "transition_detail": "Purchase Order approved by Shop Keeper"
                })
            self.approval_stage = "Document Approved By Shopkeeper"
            self.docstatus = 0
        else:
            frappe.throw("Document Should Be Approved By Shopkeeper")


    def approved_purchase_order_by_project_admin(self, email):
        if email and len(self.transition_table) == 1:
            self.append("transition_table", {
                    "role": "Project Admin",
                    "approved": 1,
                    "user": email,
                    "transition_detail": "Purchase Order approved by Project Admin"
                })
            self.docstatus = 0 
            self.approval_stage = "Document Approved By Project Admin"
        else:
            frappe.throw("Project Should be approved by Shopkeeper")

    def approved_purchase_order_by_management(self, email):
        if email and len(self.transition_table) == 2:    
            self.append("transition_table", {
                    "role": "Management",
                    "approved": 1,
                    "user": email,
                    "transition_detail": "Purchase Order approved by Management"
                })
            self.docstatus = 0
            self.approval_stage = "Document Should Be Approved By management"  
        else:
            frappe.throw("Document Should Be Approved By managemu")


    def approved_purchase_order_by_project_manager(self, email):
        if email and len(self.transition_table) == 3:
            self.append("transition_table", {
                    "role": "Project Manager",
                    "approved": 1,
                    "user": email,
                    "transition_detail": "Purchase Order approved by Management"
                })
            self.docstatus = 1
            self.approval_stage = "Document Should Be Approved By Project Manager" 


    def create_transition_table_for_workflow(self):
        if self.cost_center:
            cost_center = frappe.get_doc("Cost Center", self.cost_center)
            role_transition_dict = {}
            role_transition_dict["pm_name"] = cost_center.pm_name
            
            for roles in role_transition_dict:
                self.append("transition_table",{
                    "role"

                })
        else:
            frappe.throw("Cost Center is not selected")
