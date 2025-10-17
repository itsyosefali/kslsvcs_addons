# Copyright (c) 2025, itsyosefali and contributors
# For license information, please see license.txt

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_equipment_custom_fields():
	"""Create custom fields for Customer Equipment integration"""
	
	custom_fields = {
		"Issue": [
			{
				"fieldname": "equipment",
				"label": "Equipment",
				"fieldtype": "Link",
				"options": "Customer Equipment",
				"insert_after": "customer",
				"description": "Link to the customer equipment for tracking service history"
			}
		],
		"Sales Order": [
			{
				"fieldname": "equipment",
				"label": "Equipment",
				"fieldtype": "Link",
				"options": "Customer Equipment",
				"insert_after": "customer",
				"description": "Link equipment for project-based fabrication or installation"
			}
		],
		"Project": [
			{
				"fieldname": "equipment",
				"label": "Equipment",
				"fieldtype": "Link",
				"options": "Customer Equipment",
				"insert_after": "customer",
				"description": "Link equipment to project"
			}
		],
		"Sales Invoice": [
			{
				"fieldname": "equipment",
				"label": "Equipment",
				"fieldtype": "Link",
				"options": "Customer Equipment",
				"insert_after": "customer",
				"description": "Link equipment for tracking purposes"
			}
		],
		"Delivery Note": [
			{
				"fieldname": "equipment",
				"label": "Equipment",
				"fieldtype": "Link",
				"options": "Customer Equipment",
				"insert_after": "customer",
				"description": "Link equipment for installation tracking"
			}
		]
	}
	
	create_custom_fields(custom_fields, update=True)


def remove_equipment_custom_fields():
	"""Remove custom fields when app is uninstalled"""
	
	doctypes = ["Issue", "Sales Order", "Project", "Sales Invoice", "Delivery Note"]
	
	for doctype in doctypes:
		custom_field = frappe.db.exists("Custom Field", f"{doctype}-equipment")
		if custom_field:
			frappe.delete_doc("Custom Field", custom_field)

