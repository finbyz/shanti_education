// Copyright (c) 2023, FINBYZ TECH PVT LTD and contributors
// For license information, please see license.txt

frappe.ui.form.on('Admission Lead', {
	refresh: function(frm) {
		if(frm.doc.__islocal){
			if(!frm.doc.lead_owner)
				frm.set_value('lead_owner',frappe.session.user)
		}
	},
	copy_whatsapp_father:function(frm){
		if(frm.doc.fathers_mobile_no){
			if(!frm.doc.fathers_whatsapp_no || frm.doc.fathers_whatsapp_no!=frm.doc.fathers_mobile_no){
				frm.set_value('fathers_whatsapp_no',frm.doc.fathers_mobile_no)
			}
		}
	},
	copy_whatsapp_mother:function(frm){
		if(frm.doc.mothers_moble_no){
			if(!frm.doc.mothers_whatsapp_no || frm.doc.mothers_whatsapp_no!=frm.doc.mothers_moble_no){
				frm.set_value('mothers_whatsapp_no',frm.doc.mothers_moble_no)
			}
		}
	},
	birth_date: function(frm) {
        // Trigger the age calculation when the date of birth field changes
        calculateAge(frm);
    }
});


function calculateAge(frm) {
    // Get the selected date of birth from the custom field
    var birthDate = frm.doc.birth_date;

    if (birthDate) {
        // Split the date strings into year, month, and day components
        var birthDateParts = birthDate.split('-');
        var currentDate = frappe.datetime.now_date().split('-');
        
        var birthYear = parseInt(birthDateParts[0]);
        var birthMonth = parseInt(birthDateParts[1]);
        var currentYear = parseInt(currentDate[0]);
        var currentMonth = parseInt(currentDate[1]);

        // Calculate the age in years and months
        var ageYears = currentYear - birthYear;
        var ageMonths = currentMonth - birthMonth;

        // Adjust for negative month difference
        if (ageMonths < 0) {
            ageYears--;
            ageMonths += 12;
        }

        // Display the calculated age in a custom field
        frm.set_value('age_as_on', ageYears + ' Year ' + ageMonths + ' Month');
    }
}