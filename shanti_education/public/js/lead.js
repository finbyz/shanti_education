frappe.ui.form.on('Lead', {
    birth_date: function(frm) {
        frappe.call({
            method: "shanti_education.shanti_education.doctype.admission_lead.date_diff.",
            args: {
                'self':frm.doc
            },
            callback: function (r) {
               console.log('aa')
            }
        });
        
    }
});
