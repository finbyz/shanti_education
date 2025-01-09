import frappe
from frappe import _,msgprint
# from erpnext.accounts.doctype.journal_entry.journal_entry import apply_tax_withholding
from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry as _JournalEntry
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import (
    get_party_tax_withholding_details,
)
from erpnext.accounts.report.general_ledger.general_ledger import get_account_type_map
from erpnext.accounts.party import get_party_account


class JournalEntry(_JournalEntry):
    def submit(self):
        # if len(self.accounts) > 100:
        #     msgprint(_("The task has been enqueued as a background job."), alert=True)
        #     self.queue_action("submit", timeout=4600)
        # else:
        return self._submit()

    def cancel(self):
        # if len(self.accounts) > 100:
        #     msgprint(_("The task has been enqueued as a background job."), alert=True)
        #     self.queue_action("cancel", timeout=4600)
        # else:
        return self._cancel()
