
import frappe
from frappe import _
from frappe.utils import now

# def after_workflow_action(self,method):
#     custom_workflow_state_change(self)

# def custom_workflow_state_change(self):
#     frappe.throw("hi")
#     previous_state = frappe.db.get_value(self.doctype,self,"workflow_state")
#     if previous_state != self.workflow_state:
#         user_name = frappe.session.user_fullname
#         current_time = now()

#         child_row = self.append('workflow_changes', {})
#         child_row.username = user_name
#         child_row.modification_time = current_time
#         child_row.workflow_status = self.workflow_state
    
# In your DocType's Python file or a custom app's hooks.py

def before_validate(self, method):
    previous_state = frappe.db.get_value(self.doctype,self.name,"workflow_state")

    if previous_state != self.workflow_state:
        workflow_state(self)

def workflow_state(self):
    user_name = frappe.db.get_value("User",frappe.session.user,"full_name")
    for row in self.workflow_changes:
        if row.workflow_status == self.workflow_state:
            self.workflow_changes = []
            user_name = row.username
    self.append('workflow_changes', {
        'username': user_name,
        'modification_time': now(),
        "workflow_status": self.workflow_state
    })

def before_insert(self, method):
    self.workflow_changes = []

