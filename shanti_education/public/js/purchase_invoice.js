frappe.ui.form.on("Purchase Invoice", {
    onload: function(frm) {
        // Ignore cancellation for all linked documents of respective DocTypes.
        frm.ignore_doctypes_on_cancel_all = ["Payment Ledger Entry"];
    },
    cost_center: function(frm) {
        for (let row of frm.doc.taxes) {
            frappe.model.set_value(row.doctype, row.name, "cost_center", frm.doc.cost_center);
        }
        for (let row of frm.doc.items) {
            frappe.model.set_value(row.doctype, row.name, "cost_center", frm.doc.cost_center);
        }
    },
});