# Copyright (c) 2025, itsyosefali and contributors
# For license information, please see license.txt

from frappe import _


def get_data():
	return {
		"fieldname": "customer_equipment",
		"non_standard_fieldnames": {},
		"transactions": [
			{
				"label": _("Service & Maintenance"),
				"items": ["Service Call"]
			}
		]
	}

