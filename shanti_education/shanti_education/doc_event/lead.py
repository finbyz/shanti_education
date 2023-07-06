from dateutil import relativedelta
import datetime
from frappe.utils import today

import frappe
def validate(self, method):
    if self.birth_date:
        set_age_as_on(self)

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