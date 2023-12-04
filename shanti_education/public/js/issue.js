frappe.ui.form.on('Issue', {
	refresh: function(frm) {
	    if (frappe.user.has_role('Timeline Disable') == 1) {
		    $('.form-footer').hide();
	    }
	}
});