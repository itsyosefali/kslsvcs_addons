// Copyright (c) 2025, itsyosefali and contributors
// For license information, please see license.txt

frappe.ui.form.on('Customer Equipment', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			// Button to view service calls
			frm.add_custom_button(__('View Service Calls'), function() {
				frappe.set_route('List', 'Service Call', {
					customer_equipment: frm.doc.name
				});
			});
			
			// Button to create new service call
			frm.add_custom_button(__('New Service Call'), function() {
				frappe.new_doc('Service Call', {
					customer: frm.doc.customer,
					customer_equipment: frm.doc.name
				});
			}, __('Create'));
			
			// Button to view maintenance history (if report exists)
			// frm.add_custom_button(__('View Maintenance History'), function() {
			// 	frappe.set_route('query-report', 'Equipment Maintenance History', {
			// 		equipment: frm.doc.name
			// 	});
			// });
		}
		
		// Show warranty status indicator
		if (frm.doc.warranty_expiry) {
			let days_remaining = frappe.datetime.get_day_diff(frm.doc.warranty_expiry, frappe.datetime.nowdate());
			
			if (days_remaining < 0) {
				frm.dashboard.add_indicator(__('Warranty Expired'), 'red');
			} else if (days_remaining <= 30) {
				frm.dashboard.add_indicator(__('Warranty Expiring Soon ({0} days)', [days_remaining]), 'orange');
			} else {
				frm.dashboard.add_indicator(__('Warranty Valid ({0} days)', [days_remaining]), 'green');
			}
		}
	},
	
	customer: function(frm) {
		// Auto-fetch customer details if needed
		if (frm.doc.customer) {
			frappe.db.get_value('Customer', frm.doc.customer, 'territory', function(r) {
				if (r && r.territory) {
					// You can set default location based on territory if needed
				}
			});
		}
	},
	
	installation_date: function(frm) {
		// Validate installation date
		if (frm.doc.installation_date) {
			let install_date = frappe.datetime.str_to_obj(frm.doc.installation_date);
			let today = frappe.datetime.now_date(true);
			
			if (install_date > today) {
				frappe.msgprint(__('Installation date cannot be in the future'));
				frm.set_value('installation_date', '');
			}
		}
	},
	
	warranty_expiry: function(frm) {
		// Validate warranty expiry
		if (frm.doc.warranty_expiry && frm.doc.installation_date) {
			let warranty_date = frappe.datetime.str_to_obj(frm.doc.warranty_expiry);
			let install_date = frappe.datetime.str_to_obj(frm.doc.installation_date);
			
			if (warranty_date < install_date) {
				frappe.msgprint(__('Warranty expiry date cannot be before installation date'));
				frm.set_value('warranty_expiry', '');
			}
		}
	}
});

