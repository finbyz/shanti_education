from frappe import _
import frappe

def on_update(self, method):
	out_and_in_qty(self)
     
@frappe.whitelist()
def out_and_in_qty(self):
    # ongoing qty total
    total_outgoing_qty = 0.0
    total_incoming_qty = 0.0
    for item in self.items:
        if  item.is_finished_item == 0:
            total_outgoing_qty += item.qty
    self.total_outgoing_qty = total_outgoing_qty
    # incoming qty total
    for item in self.items:
        if  item.is_finished_item == 1:
            total_incoming_qty += item.qty
    self.total_incoming_qty = total_incoming_qty