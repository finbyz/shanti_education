// Copyright (c) 2023, FINBYZ TECH PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Admission Lead', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			if(!frm.doc.lead_owner)
				frm.set_value('lead_owner',frappe.session.user)
		}
	}
});
