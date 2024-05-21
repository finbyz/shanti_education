from frappe import _


def before_validate(self, method):
    update_cost_centre_in_items(self)

def update_cost_centre_in_items(self):
    for item in self.items:
        item.cost_center = self.cost_center
    for tax in self.taxes:
        tax.cost_center = self.cost_center