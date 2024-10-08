import frappe
from frappe.utils import cint, flt, getdate
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_tds_amount,get_invoice_total_without_tcs
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import get_invoice_total_without_tcs

def get_tds_amount(ldc, parties, inv, tax_details, vouchers):
    tds_amount = 0
    invoice_filters = {"name": ("in", vouchers), "docstatus": 1, "apply_tds": 1}

    # Filters for TDS on advances
    payment_entry_filters = {
        "party_type": "Supplier",
        "party": ("in", parties),
        "docstatus": 1,
        "apply_tax_withholding_amount": 1,
        "unallocated_amount": (">", 0),
        "posting_date": ["between", (tax_details.from_date, tax_details.to_date)],
        "tax_withholding_category": tax_details.get("tax_withholding_category"),
    }

    field = "sum(tax_withholding_net_total)"

    if cint(tax_details.consider_party_ledger_amount):
        invoice_filters.pop("apply_tds", None)
        field = "sum(grand_total)"

        payment_entry_filters.pop("apply_tax_withholding_amount", None)
        payment_entry_filters.pop("tax_withholding_category", None)

    supp_credit_amt = frappe.db.get_value("Purchase Invoice", invoice_filters, field) or 0.0

    supp_jv_credit_amt = (
        frappe.db.get_value(
            "Journal Entry Account",
            {
                "parent": ("in", vouchers),
                "docstatus": 1,
                "party": ("in", parties),
                "reference_type": ("!=", "Purchase Invoice"),
            },
            "sum(credit_in_account_currency - debit_in_account_currency)",
        )
        or 0.0
    )

    payment_entry_amounts = frappe.db.get_all(
        "Payment Entry",
        filters=payment_entry_filters,
        fields=["sum(unallocated_amount) as amount", "payment_type"],
        group_by="payment_type",
    )
    # NoneType error solve by flt FinByz
    supp_credit_amt += flt(supp_jv_credit_amt)
    supp_credit_amt += flt(inv.tax_withholding_net_total)

    for entry in payment_entry_amounts:
        if entry.payment_type == "Pay":
            supp_credit_amt += entry.amount
        else:
            supp_credit_amt -= entry.amount

    threshold = tax_details.get("threshold", 0)
    cumulative_threshold = tax_details.get("cumulative_threshold", 0)

    if inv.doctype != "Payment Entry":
        tax_withholding_net_total = inv.base_tax_withholding_net_total
    else:
        tax_withholding_net_total = inv.tax_withholding_net_total
        # NoneType error solve by flt FinByz
    if (threshold and flt(tax_withholding_net_total) >= threshold) or (
        cumulative_threshold and supp_credit_amt >= cumulative_threshold
    ):
        if (cumulative_threshold and supp_credit_amt >= cumulative_threshold) and cint(
            tax_details.tax_on_excess_amount
        ):
            net_total = (
                frappe.db.get_value("Purchase Invoice", invoice_filters, "sum(tax_withholding_net_total)")
                or 0.0
            )
            net_total += inv.tax_withholding_net_total
            supp_credit_amt = net_total - cumulative_threshold

        if ldc and is_valid_certificate(ldc, inv.get("posting_date") or inv.get("transaction_date"), 0):
            tds_amount = get_lower_deduction_amount(
                supp_credit_amt, 0, ldc.certificate_limit, ldc.rate, tax_details
            )
        else:
            tds_amount = supp_credit_amt * tax_details.rate / 100 if supp_credit_amt > 0 else 0

    return tds_amount


def is_valid_certificate(ldc, posting_date, limit_consumed):
    available_amount = flt(ldc.certificate_limit) - flt(limit_consumed)
    return getdate(ldc.valid_from) <= getdate(posting_date) <= getdate(ldc.valid_upto) and available_amount > 0


def get_lower_deduction_amount(current_amount, limit_consumed, certificate_limit, rate, tax_details):
    if certificate_limit - flt(limit_consumed) - flt(current_amount) >= 0:
        return current_amount * rate / 100
    else:
        ltds_amount = certificate_limit - flt(limit_consumed)
        tds_amount = current_amount - ltds_amount

        return ltds_amount * rate / 100 + tds_amount * tax_details.rate / 100
    
def get_invoice_total_without_tcs(inv, tax_details):
    # inv.taxes None Handel by FinByz Start
	inv.taxes = inv.get("taxes") or []
    # FinByz End
	tcs_tax_row = [d for d in inv.taxes if d.account_head == tax_details.account_head]
	tcs_tax_row_amount = tcs_tax_row[0].base_tax_amount if tcs_tax_row else 0
    # NoneType error solve by flt FinByz Start
	return flt(inv.grand_total) - tcs_tax_row_amount
    # FinByz End
