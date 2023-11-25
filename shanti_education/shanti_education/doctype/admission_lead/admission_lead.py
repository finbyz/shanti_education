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

	def before_save(self):
		self.validate_email_counts()
		self.validate_contact_counts()

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

	def validate_email_counts(self):
		if self.fathers_email:
			count = frappe.db.count('Admission Lead', {'fathers_email': self.fathers_email, 'name': ('!=', self.name)})
			threshold = 3
			if count >= threshold:
				admission_lead_names = frappe.get_list('Admission Lead', {'fathers_email': self.fathers_email, 'name': ('!=', self.name)}, pluck='name', limit=threshold)
				admission_lead_names_str = ', '.join('<a href="/app/admission-lead/{0}">{0}</a>'.format(lead_name) for lead_name in admission_lead_names)
				frappe.throw('Email ID {} is already used in {} Admission Lead. Please use a different email. <br>Admission Lead Names: {}'.format(self.fathers_email, count, admission_lead_names_str))
	
	def validate_contact_counts(self):
		if self.fathers_mobile_no:
			count = frappe.db.count('Admission Lead', {'fathers_mobile_no': self.fathers_mobile_no, 'name': ('!=', self.name)})
			threshold = 3
			if count >= threshold:
				admission_lead_names = frappe.get_list('Admission Lead', {'fathers_mobile_no': self.fathers_mobile_no, 'name': ('!=', self.name)}, pluck='name', limit=threshold)
				admission_lead_names_str = ', '.join('<a href="/app/admission-lead/{0}">{0}</a>'.format(lead_name) for lead_name in admission_lead_names)
				frappe.throw("Father's Mobile No {} is already used in {} Admission Lead. Please use a different number. <br>Admission Lead Names: {}".format(self.fathers_mobile_no, count, admission_lead_names_str))
		
		if self.fathers_whatsapp_no:
			count = frappe.db.count('Admission Lead', {'fathers_whatsapp_no': self.fathers_whatsapp_no, 'name': ('!=', self.name)})
			threshold = 3
			if count >= threshold:
				admission_lead_names = frappe.get_list('Admission Lead', {'fathers_whatsapp_no': self.fathers_whatsapp_no, 'name': ('!=', self.name)}, pluck='name', limit=threshold)
				admission_lead_names_str = ', '.join('<a href="/app/admission-lead/{0}">{0}</a>'.format(lead_name) for lead_name in admission_lead_names)
				frappe.throw("Father's Whatsapp No {} is already used in {} Admission Lead. Please use a different number. <br>Admission Lead Names: {}".format(self.fathers_whatsapp_no, count, admission_lead_names_str))
		
		if self.mothers_moble_no:
			count = frappe.db.count('Admission Lead', {'mothers_moble_no': self.mothers_moble_no, 'name': ('!=', self.name)})
			threshold = 3
			if count >= threshold:
				admission_lead_names = frappe.get_list('Admission Lead', {'mothers_moble_no': self.mothers_moble_no, 'name': ('!=', self.name)}, pluck='name', limit=threshold)
				admission_lead_names_str = ', '.join('<a href="/app/admission-lead/{0}">{0}</a>'.format(lead_name) for lead_name in admission_lead_names)
				frappe.throw("Mother's Mobile No {} is already used in {} Admission Lead. Please use a different number. <br>Admission Lead Names: {}".format(self.mothers_moble_no, count, admission_lead_names_str))
		
		if self.mothers_whatsapp_no:
			count = frappe.db.count('Admission Lead', {'mothers_whatsapp_no': self.mothers_whatsapp_no, 'name': ('!=', self.name)})
			threshold = 3
			if count >= threshold:
				admission_lead_names = frappe.get_list('Admission Lead', {'mothers_whatsapp_no': self.mothers_whatsapp_no, 'name': ('!=', self.name)}, pluck='name', limit=threshold)
				admission_lead_names_str = ', '.join('<a href="/app/admission-lead/{0}">{0}</a>'.format(lead_name) for lead_name in admission_lead_names)
				frappe.throw("Mother's Whatsapp No {} is already used in {} Admission Lead. Please use a different number. <br>Admission Lead Names: {}".format(self.mothers_whatsapp_no, count, admission_lead_names_str))