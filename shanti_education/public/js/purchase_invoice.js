frappe.ui.form.on("Purchase Invoice", {
    onload: function(frm) {
        // Ignore cancellation for all linked documents of respective DocTypes.
        frm.ignore_doctypes_on_cancel_all = ["Payment Ledger Entry"];
    }
});