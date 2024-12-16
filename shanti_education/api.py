import json
import os
from typing import TYPE_CHECKING

import frappe
import frappe.model
import frappe.utils
from frappe import _
from frappe.client import insert_doc

@frappe.whitelist(methods=["POST", "PUT"])
def create_product_bundle(**kwargs):
    product_bundle = kwargs
    if isinstance(product_bundle, str):
        product_bundle = json.loads(product_bundle)
        
    new_item_code = product_bundle.get("new_item_code")
    
    # Check if the bundle already exists
    if frappe.db.exists("Product Bundle", {"new_item_code": new_item_code}):
        doc_name = insert_sales_order(product_bundle)
        return {"Sales Order": doc_name}
    
    product_bundle_doc = frappe.get_doc({
        "doctype": "Product Bundle",
        "new_item_code": new_item_code,
    })    
    for item in product_bundle.get("items", []):
        product_bundle_doc.append("items", {
            "item_code": item.get("item_code"),
            "qty": item.get("quantity"),   
        })
    
    product_bundle_doc.insert()
    insert_sales_order(product_bundle)

@frappe.whitelist(methods=["POST", "PUT"])
def insert_sales_order(product_bundle):
    if isinstance(product_bundle, str):
        product_bundle = json.loads(product_bundle)
    
    new_item_code = product_bundle.get("new_item_code")
          
    sales_order_doc = frappe.get_doc({
        "doctype": "Sales Order",
        "customer": product_bundle.get("customer"),
        "items": [
            {
                "item_code": new_item_code,
                "qty": 1,
                "rate": product_bundle.get("rate"),
            }
        ],
        "cost_center": product_bundle.get("cost_center"),
        "company": product_bundle.get("company"),
        "customer": product_bundle.get("customer"),
        "transaction_date": product_bundle.get("transaction_date"),
        "delivery_date": product_bundle.get("delivery_date"),
        "branch": product_bundle.get("branch"),
        "customer_address": product_bundle.get("customer_address")
    })
    
    sales_order_doc.insert()
    return sales_order_doc.name

