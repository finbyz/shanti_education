{% include "erpnext/public/js/controllers/accounts.js" %}
frappe.provide("erpnext.accounts.dimensions");

cur_frm.cscript.tax_table = "Advance Taxes and Charges";

frappe.ui.form.on("Payment Entry", {
    get_outstanding_invoices_or_orders: function(frm, get_outstanding_invoices, get_orders_to_be_billed) {
		const today = frappe.datetime.get_today();
		let fields = [
			{fieldtype:"Section Break", label: __("Posting Date")},
			{fieldtype:"Date", label: __("From Date"),
				fieldname:"from_posting_date", default:frappe.datetime.add_days(today, -30)},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_posting_date", default:today},
			{fieldtype:"Section Break", label: __("Due Date")},
			{fieldtype:"Date", label: __("From Date"), fieldname:"from_due_date"},
			{fieldtype:"Column Break"},
			{fieldtype:"Date", label: __("To Date"), fieldname:"to_due_date"},
			{fieldtype:"Section Break", label: __("Outstanding Amount")},
			{fieldtype:"Float", label: __("Greater Than Amount"),
				fieldname:"outstanding_amt_greater_than", default: 0},
			{fieldtype:"Column Break"},
			{fieldtype:"Float", label: __("Less Than Amount"), fieldname:"outstanding_amt_less_than"},
		];

		if (frm.dimension_filters) {
			let column_break_insertion_point = Math.ceil((frm.dimension_filters.length)/2);

			fields.push({fieldtype:"Section Break"});
			frm.dimension_filters.map((elem, idx)=>{
				fields.push({
					fieldtype: "Link",
					label: elem.document_type == "Cost Center" ? "Cost Center" : elem.label,
					options: elem.document_type,
					default: elem.fieldname == "cost_center" ? frm.doc.cost_center : null,
					fieldname: elem.fieldname || elem.document_type
				});
				if(idx+1 == column_break_insertion_point) {
					fields.push({fieldtype:"Column Break"});
				}
			});
		}

		fields = fields.concat([
			{fieldtype:"Section Break"},
			{fieldtype:"Check", label: __("Allocate Payment Amount"), fieldname:"allocate_payment_amount", default:1},
		]);

		let btn_text = "";

		if (get_outstanding_invoices) {
			btn_text = "Get Outstanding Invoices";
		}
		else if (get_orders_to_be_billed) {
			btn_text = "Get Outstanding Orders";
		}

		frappe.prompt(fields, function(filters){
			frappe.flags.allocate_payment_amount = true;
			frm.events.validate_filters_data(frm, filters);
			frm.doc.cost_center = filters.cost_center;
			frm.events.get_outstanding_documents(frm, filters, get_outstanding_invoices, get_orders_to_be_billed);
		}, __("Filters"), __(btn_text));
	},
})