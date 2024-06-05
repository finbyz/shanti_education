import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import get_bank_cash_account
from hrms.hr.doctype.expense_claim.expense_claim import ExpenseClaim as _ExpenseClaim
class ExpenseClaim( _ExpenseClaim):
    def get_gl_entries(self):
            gl_entry = []
            self.validate_account_details()

            # payable entry
            if self.grand_total:
                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": self.payable_account,
                            "credit": self.grand_total,
                            "credit_in_account_currency": self.grand_total,
                            "against": ",".join([d.default_account for d in self.expenses]),
                            "party_type": "Employee",
                            "party": self.employee,
                            "against_voucher_type": self.doctype,
                            "against_voucher": self.name,
                            "cost_center": self.cost_center,
                            "project": self.project,
                        },
                        item=self,
                    )
                )

            # expense entries
            for data in self.expenses:
                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": data.default_account,
                            "debit": data.sanctioned_amount,
                            "debit_in_account_currency": data.sanctioned_amount,
                            "against": self.employee,
                            "cost_center": data.cost_center or self.cost_center,
                            "project": data.project or self.project,
                        },
                        item=data,
                    )
                )

            for data in self.advances:
                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": data.advance_account,
                            "credit": data.allocated_amount,
                            "credit_in_account_currency": data.allocated_amount,
                            "against": ",".join([d.default_account for d in self.expenses]),
                            "party_type": "Employee",
                            "party": self.employee,
                            "against_voucher_type": "Employee Advance",
                            "cost_center": self.cost_center, # finbyz change
                            "against_voucher": data.employee_advance,
                        }
                    )
                )

            self.add_tax_gl_entries(gl_entry)

            if self.is_paid and self.grand_total:
                # payment entry
                payment_account = get_bank_cash_account(self.mode_of_payment, self.company).get("account")
                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": payment_account,
                            "credit": self.grand_total,
                            "credit_in_account_currency": self.grand_total,
                            "against": self.employee,
                        },
                        item=self,
                    )
                )

                gl_entry.append(
                    self.get_gl_dict(
                        {
                            "account": self.payable_account,
                            "party_type": "Employee",
                            "party": self.employee,
                            "against": payment_account,
                            "debit": self.grand_total,
                            "debit_in_account_currency": self.grand_total,
                            "against_voucher": self.name,
                            "against_voucher_type": self.doctype,
                        },
                        item=self,
                    )
                )

            return gl_entry