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
    def apply_tax_withholding(self):
        if not self.apply_tds or self.voucher_type not in ("Debit Note", "Credit Note"):
            return
        parties = [d.party for d in self.get("accounts") if d.party]
        parties = list(set(parties))

        if len(parties) > 1:
            frappe.throw(_("Cannot apply TDS against multiple parties in one entry"))

        account_type_map = get_account_type_map(self.company)
        party_type = "supplier" if self.voucher_type == "Credit Note" else "customer"
        doctype = "Purchase Invoice" if self.voucher_type == "Credit Note" else "Sales Invoice"
        debit_or_credit = (
            "debit_in_account_currency"
            if self.voucher_type == "Credit Note"
            else "credit_in_account_currency"
        )
        rev_debit_or_credit = (
            "credit_in_account_currency"
            if debit_or_credit == "debit_in_account_currency"
            else "debit_in_account_currency"
        )

        party_account = get_party_account(party_type.title(), parties[0], self.company)

        net_total = sum(
            d.get(debit_or_credit)
            for d in self.get("accounts")
            if account_type_map.get(d.account) not in ("Tax", "Chargeable")
        )

        party_amount = sum(
            d.get(rev_debit_or_credit) for d in self.get("accounts") if d.account == party_account
        )

        inv = frappe._dict(
            {
                party_type: parties[0],
                "doctype": doctype,
                "company": self.company,
                "posting_date": self.posting_date,
                "net_total": net_total,
            }
        )
        # finbyz changes Extra argument Remove (advance_taxes, voucher_wise_amount) Start
        tax_withholding_details = get_party_tax_withholding_details(
            inv, self.tax_withholding_category
        )
        # finbyz changes Extra argument Remove (advance_taxes, voucher_wise_amount) End
        if not tax_withholding_details:
            return
        accounts = []
        for d in self.get("accounts"):
            if d.get("account") == tax_withholding_details.get("account_head"):
                d.update(
                    {
                        "account": tax_withholding_details.get("account_head"),
                        debit_or_credit: tax_withholding_details.get("tax_amount"),
                    }
                )

            accounts.append(d.get("account"))

            if d.get("account") == party_account:
                d.update({rev_debit_or_credit: party_amount - tax_withholding_details.get("tax_amount")})

        if not accounts or tax_withholding_details.get("account_head") not in accounts:
            self.append(
                "accounts",
                {
                    "account": tax_withholding_details.get("account_head"),
                    rev_debit_or_credit: tax_withholding_details.get("tax_amount"),
                    "against_account": parties[0],
                },
            )

        to_remove = [
            d
            for d in self.get("accounts")
            if not d.get(rev_debit_or_credit) and d.account == tax_withholding_details.get("account_head")
        ]

        for d in to_remove:
            self.remove(d)