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


	def validate_pincode(self):
		pin_code = self.pincode.strip()
		self.pincode = pin_code
		if len(self.pincode)>6 or len(self.pincode)<6:
			frappe.throw("Pincode has six digit So Please write six digit pincode")

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

	
	
