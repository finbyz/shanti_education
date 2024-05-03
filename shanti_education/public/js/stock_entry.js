frappe.ui.form.on("Stock Entry", {
    cost_center: function(frm) {
        var cost_center_doc = frm.doc.cost_center;
        frm.doc.items.forEach(function (d){
			d.cost_center = cost_center_doc
		})
    },
    update_qty_availability: function(frm) {
        var total_outgoing_qty = 0.0;
        var total_incoming_qty = 0.0;
        for (var i = 0; i < frm.doc.items.length; i++) {
            var item = frm.doc.items[i];
            if (item.is_finished_item == 0) {
                total_outgoing_qty += item.qty;
            }
            if (item.is_finished_item == 1) {
                total_incoming_qty += item.qty;
            }
        }
        frm.set_value('total_outgoing_qty', total_outgoing_qty);
        frm.set_value('total_incoming_qty', total_incoming_qty);
    }
});