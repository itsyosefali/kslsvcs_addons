# Copyright (c) 2025, itsyosefali and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import getdate, add_days, today


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	chart = get_chart_data(data)
	return columns, data, None, chart


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
			"fieldname": "location",
			"label": _("Location"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "warranty_expiry",
			"label": _("Warranty Expiry"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "days_remaining",
			"label": _("Days Remaining"),
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": _("Status"),
			"fieldtype": "Data",
			"width": 100
		}
	]


def get_data(filters):
	conditions = []
	values = {}
	
	# Default: Show equipment with warranties expiring in next 90 days
	days_ahead = filters.get("days_ahead") or 90
	
	values["today"] = today()
	values["future_date"] = add_days(today(), days_ahead)
	
	if filters.get("customer"):
		conditions.append("customer = %(customer)s")
		values["customer"] = filters.get("customer")
	
	# Only show Active and In Service equipment
	conditions.append("status IN ('Active', 'In Service')")
	
	# Only show equipment with warranty expiry date
	conditions.append("warranty_expiry IS NOT NULL")
	
	# Show warranties expiring within the specified period
	conditions.append("warranty_expiry BETWEEN %(today)s AND %(future_date)s")
	
	where_clause = "WHERE " + " AND ".join(conditions)
	
	query = f"""
		SELECT
			name as equipment_name,
			customer,
			location,
			warranty_expiry,
			DATEDIFF(warranty_expiry, CURDATE()) as days_remaining,
			status
		FROM
			`tabCustomer Equipment`
		{where_clause}
		ORDER BY
			warranty_expiry ASC
	"""
	
	return frappe.db.sql(query, values, as_dict=1)


def get_chart_data(data):
	if not data:
		return None
	
	# Group data by month
	labels = []
	values = []
	
	# Count equipment expiring per month
	month_counts = {}
	for row in data:
		month = frappe.utils.formatdate(row.warranty_expiry, "MMM YYYY")
		month_counts[month] = month_counts.get(month, 0) + 1
	
	labels = list(month_counts.keys())
	values = list(month_counts.values())
	
	return {
		"data": {
			"labels": labels,
			"datasets": [
				{
					"name": "Warranties Expiring",
					"values": values
				}
			]
		},
		"type": "bar",
		"colors": ["#fc4f51"]
	}

