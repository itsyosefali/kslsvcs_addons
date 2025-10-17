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
			"fieldname": "equipment_name",
			"label": _("Equipment Name"),
			"fieldtype": "Link",
			"options": "Customer Equipment",
			"width": 180
		},
		{
			"fieldname": "customer",
			"label": _("Customer"),
			"fieldtype": "Link",
			"options": "Customer",
			"width": 150
		},
		{
			"fieldname": "issue_name",
			"label": _("Issue/Work Order"),
			"fieldtype": "Link",
			"options": "Issue",
			"width": 150
		},
		{
			"fieldname": "subject",
			"label": _("Subject"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "priority",
			"label": _("Priority"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "opening_date",
			"label": _("Opening Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "resolution_date",
			"label": _("Resolution Date"),
			"fieldtype": "Date",
			"width": 120
		}
	]


def get_data(filters):
	conditions = []
	values = {}
	
	if filters.get("equipment"):
		conditions.append("ce.name = %(equipment)s")
		values["equipment"] = filters.get("equipment")
	
	if filters.get("customer"):
		conditions.append("ce.customer = %(customer)s")
		values["customer"] = filters.get("customer")
	
	where_clause = ""
	if conditions:
		where_clause = "AND " + " AND ".join(conditions)
	
	# Query issues linked to equipment
	query = f"""
		SELECT
			ce.name as equipment_name,
			ce.customer,
			i.name as issue_name,
			i.subject,
			i.status,
			i.priority,
			i.opening_date,
			i.resolution_date
		FROM
			`tabCustomer Equipment` ce
		LEFT JOIN
			`tabIssue` i ON i.equipment = ce.name
		WHERE
			i.name IS NOT NULL
			{where_clause}
		ORDER BY
			ce.name, i.opening_date DESC
	"""
	
	data = frappe.db.sql(query, values, as_dict=1)
	
	# If no issues found, return empty data
	if not data:
		# Try to get equipment info even if no issues
		if filters.get("equipment"):
			equipment = frappe.get_doc("Customer Equipment", filters.get("equipment"))
			return [{
				"equipment_name": equipment.name,
				"customer": equipment.customer,
				"issue_name": None,
				"subject": "No maintenance records found",
				"status": "-",
				"priority": "-",
				"opening_date": None,
				"resolution_date": None
			}]
	
	return data

