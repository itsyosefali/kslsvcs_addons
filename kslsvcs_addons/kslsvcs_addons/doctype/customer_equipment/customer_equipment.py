# Copyright (c) 2025, itsyosefali and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class CustomerEquipment(Document):
	def validate(self):
		"""Validate the Customer Equipment document"""
		self.validate_warranty_date()
		self.check_duplicate_serial_number()
	
	def validate_warranty_date(self):
		"""Ensure warranty expiry is after installation date"""
		if self.installation_date and self.warranty_expiry:
			if self.warranty_expiry < self.installation_date:
				frappe.throw(
					frappe._("Warranty Expiry Date cannot be before Installation Date")
				)
	
	def check_duplicate_serial_number(self):
		"""Check for duplicate serial numbers"""
		if self.serial_number:
			existing = frappe.db.exists(
				"Customer Equipment",
				{
					"serial_number": self.serial_number,
					"name": ["!=", self.name]
				}
			)
			if existing:
				frappe.throw(
					frappe._("Serial Number {0} already exists in {1}").format(
						frappe.bold(self.serial_number),
						frappe.bold(existing)
					)
				)


@frappe.whitelist()
def get_equipment_maintenance_history(equipment):
	"""Get maintenance history for a specific equipment"""
	# This function will be useful for reports and dashboards
	return frappe.get_all(
		"Issue",  # or your Work Order/Job Card doctype
		filters={"equipment": equipment},
		fields=["name", "subject", "status", "creation", "modified"],
		order_by="creation desc"
	)


@frappe.whitelist()
def get_warranty_expiring_soon(days=30):
	"""Get list of equipment with warranties expiring soon"""
	from frappe.utils import add_days, today
	
	expiry_date = add_days(today(), days)
	
	return frappe.get_all(
		"Customer Equipment",
		filters={
			"warranty_expiry": ["between", [today(), expiry_date]],
			"status": ["in", ["Active", "In Service"]]
		},
		fields=["name", "equipment_name", "customer", "warranty_expiry", "location"],
		order_by="warranty_expiry asc"
	)


def send_warranty_expiry_notifications():
	"""Send daily notifications for warranties expiring soon (30 days)"""
	from frappe.utils import add_days, today, formatdate
	
	expiry_date = add_days(today(), 30)
	
	equipment_list = frappe.get_all(
		"Customer Equipment",
		filters={
			"warranty_expiry": ["between", [today(), expiry_date]],
			"status": ["in", ["Active", "In Service"]]
		},
		fields=["name", "equipment_name", "customer", "warranty_expiry", "location", "owner"]
	)
	
	if not equipment_list:
		return
	
	# Group by owner for notification
	owner_equipment = {}
	for equipment in equipment_list:
		owner = equipment.get("owner")
		if owner not in owner_equipment:
			owner_equipment[owner] = []
		owner_equipment[owner].append(equipment)
	
	# Send notifications
	for owner, equipments in owner_equipment.items():
		message = "<h3>Equipment Warranties Expiring Soon</h3><ul>"
		for eq in equipments:
			message += f"<li><b>{eq.equipment_name}</b> (Customer: {eq.customer}) - Expires: {formatdate(eq.warranty_expiry)}</li>"
		message += "</ul>"
		
		frappe.get_doc({
			"doctype": "Notification Log",
			"subject": f"Warranty Expiry Alert - {len(equipments)} Equipment(s)",
			"for_user": owner,
			"type": "Alert",
			"document_type": "Customer Equipment",
			"email_content": message
		}).insert(ignore_permissions=True)

