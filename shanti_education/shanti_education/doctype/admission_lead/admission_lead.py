# Copyright (c) 2023, FINBYZ TECH PVT LTD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from dateutil import relativedelta
import datetime
from frappe.utils import today

class AdmissionLead(Document):
	def validate(self):
		if self.birth_date:
			self.set_age_as_on()
		self.validate_pincode()
		self.validate_contact()


	def validate_pincode(self):
		pin_code = self.pincode.strip()
		self.pincode = pin_code
		if len(self.pincode)>6 or len(self.pincode)<6:
			frappe.throw("Pincode has six digit So Please write six digit pincode")
	
	def validate_contact(self):
		fmn = self.fathers_mobile_no.strip()
		self.fathers_mobile_no = fmn
		if len(self.fathers_mobile_no)>10 or len(self.fathers_mobile_no)<10:
			frappe.throw("Please write 10 digit number. So please update your <b>Father's Mobile No</b>.")
		
		fwn = self.fathers_whatsapp_no.strip()
		self.fathers_whatsapp_no = fwn
		if len(self.fathers_whatsapp_no)>10 or len(self.fathers_whatsapp_no)<10:
			frappe.throw("Please write 10 digit number. So please update your <b>Father's WhatsApp No</b>.")
		
		mmn = self.mothers_moble_no.strip()
		self.mothers_moble_no = mmn
		if len(self.mothers_moble_no)>10 or len(self.mothers_moble_no)<10:
			frappe.throw("Please write 10 digit number. So please update your <b>Mother's Mobile No</b>.")
		
		mwn = self.mothers_whatsapp_no.strip()
		self.mothers_whatsapp_no = mwn
		if len(self.mothers_whatsapp_no)>10 or len(self.mothers_whatsapp_no)<10:
			frappe.throw("Please write 10 digit number. So please update your <b>Mother's WhatsApp No</b>.")

	def set_age_as_on(self):
		birth_date = self.birth_date
		birth_date_date =datetime.datetime.strptime(str(birth_date), "%Y-%m-%d").date()
		today_date = datetime.datetime.strptime(str(today()), "%Y-%m-%d").date()
		delta = relativedelta.relativedelta(today_date, birth_date_date)
		years = ''
		if delta.years:
			years = f"{delta.years} Year"
		month = ''
		if delta.months:
			month= f"{delta.months} Month"
		self.age_as_on = f"{years} {month} "

	
	
