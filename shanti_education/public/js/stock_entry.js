frappe.ui.form.on("Stock Entry", {
    cost_center: function(frm) {
        var cost_center_doc = frm.doc.cost_center;
        frm.doc.items.forEach(function (d){
			d.cost_center = cost_center_doc
		})
    }
});