frappe.ui.form.on('Expense Claim', {
	refresh: function(frm) {
	    if (frm.doc.__islocal) {
            frm.set_value('is_paid', 0);
	    }
    }
});