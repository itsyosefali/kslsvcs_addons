# Copyright (c) 2025, itsyosefali and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"fieldname": "equipment_name",
			"label": _("Equipment Name"),
			"fieldtype": "Link",
			"options": "Customer Equipment",
			"width": 180
		},
		{
			"fieldname": "location",
			"label": _("Location"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "model_number",
			"label": _("Model Number"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "serial_number",
			"label": _("Serial Number"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "installation_date",
			"label": _("Installation Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "warranty_expiry",
			"label": _("Warranty Expiry"),
			"fieldtype": "Date",
			"width": 120
		}
	]


def get_data(filters):
	conditions = []
	values = {}
	
	if filters.get("customer"):
		conditions.append("customer = %(customer)s")
		values["customer"] = filters.get("customer")
	
	if filters.get("status"):
		conditions.append("status = %(status)s")
		values["status"] = filters.get("status")
	
	where_clause = ""
	if conditions:
		where_clause = "WHERE " + " AND ".join(conditions)
	
	query = f"""
		SELECT
			customer,
			name as equipment_name,
			location,
			model_number,
			serial_number,
			status,
			installation_date,
			warranty_expiry
		FROM
			`tabCustomer Equipment`
		{where_clause}
		ORDER BY
			customer, equipment_name
	"""
	
	return frappe.db.sql(query, values, as_dict=1)

