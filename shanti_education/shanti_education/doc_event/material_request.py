# Edited By Meghwin
from frappe import _


def before_validate(self, method):
	update_cost_centre_in_items(self)

def update_cost_centre_in_items(self):
	for item in self.items:
		item.cost_center = self.cost_center
