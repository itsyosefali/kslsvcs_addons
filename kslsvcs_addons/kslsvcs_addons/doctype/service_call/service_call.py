# Copyright (c) 2025, itsyosefali and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, flt


class ServiceCall(Document):
	def validate(self):
		self.validate_dates()
		self.validate_customer_equipment()
		self.calculate_total_material_cost()
		self.update_status_based_on_completion()
	
	def validate_dates(self):
		"""Validate scheduled and completion dates"""
		if self.completion_date and self.scheduled_date:
			if self.completion_date < self.scheduled_date:
				frappe.throw("Completion date cannot be before scheduled date")
	
	def validate_customer_equipment(self):
		"""Validate that the equipment belongs to the selected customer"""
		if self.customer_equipment and self.customer:
			equipment = frappe.get_doc("Customer Equipment", self.customer_equipment)
			if equipment.customer != self.customer:
				frappe.throw(f"Equipment {self.customer_equipment} does not belong to customer {self.customer}")
	
	def calculate_total_material_cost(self):
		"""Calculate total cost of materials used"""
		total = 0
		for material in self.materials_used:
			# Calculate amount for each row
			material.amount = flt(material.qty) * flt(material.rate)
			total += material.amount
		
		self.total_material_cost = total
	
	def update_status_based_on_completion(self):
		"""Auto-update status when completion date is set"""
		if self.completion_date and self.status == "In Progress":
			self.status = "Completed"
	
	def on_submit(self):
		"""Actions to perform on submit"""
		# Auto-set completion date if not set
		if not self.completion_date and self.status == "Completed":
			self.completion_date = now_datetime()
		
		# Update last service date on equipment
		if self.customer_equipment:
			frappe.db.set_value("Customer Equipment", self.customer_equipment, 
				"last_service_date", self.completion_date or self.scheduled_date)
	
	def before_cancel(self):
		"""Prevent cancellation if already billed"""
		if self.sales_invoice:
			frappe.throw("Cannot cancel a service call that has been billed. Cancel the Sales Invoice first.")


@frappe.whitelist()
def make_sales_invoice(source_name, target_doc=None):
	"""Create Sales Invoice from Service Call"""
	from frappe.model.mapper import get_mapped_doc
	
	def set_missing_values(source, target):
		target.customer = source.customer
		target.posting_date = frappe.utils.today()
		target.due_date = frappe.utils.today()
		
		# Add service charge item if configured
		# You can customize this based on your requirements
		target.append("items", {
			"item_code": "SERVICE-CALL",  # You'll need to create this item
			"item_name": f"Service Call - {source.name}",
			"description": f"Service call for equipment {source.customer_equipment}",
			"qty": 1,
			"rate": source.total_material_cost or 0
		})
		
		# Add materials as separate line items
		for material in source.materials_used:
			target.append("items", {
				"item_code": material.item_code,
				"item_name": material.item_name,
				"description": material.description,
				"qty": material.qty,
				"uom": material.uom,
				"rate": material.rate,
				"amount": material.amount
			})
	
	def update_status(source, target, source_parent):
		target.service_call = source.name
		frappe.db.set_value("Service Call", source.name, "status", "Billed")
		frappe.db.set_value("Service Call", source.name, "sales_invoice", target.name)
	
	doclist = get_mapped_doc("Service Call", source_name, {
		"Service Call": {
			"doctype": "Sales Invoice",
			"validation": {
				"docstatus": ["=", 1]
			}
		}
	}, target_doc, set_missing_values, ignore_permissions=True)
	
	return doclist

