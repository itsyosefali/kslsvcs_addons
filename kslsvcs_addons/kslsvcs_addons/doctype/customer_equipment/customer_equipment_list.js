// Copyright (c) 2025, itsyosefali and contributors
// For license information, please see license.txt

frappe.listview_settings['Customer Equipment'] = {
	add_fields: ['status', 'warranty_expiry', 'customer'],
	
	get_indicator: function(doc) {
		// Status-based indicators
		if (doc.status === 'Active') {
			return [__('Active'), 'green', 'status,=,Active'];
		} else if (doc.status === 'In Service') {
			return [__('In Service'), 'blue', 'status,=,In Service'];
		} else if (doc.status === 'Out of Service') {
			return [__('Out of Service'), 'orange', 'status,=,Out of Service'];
		} else if (doc.status === 'Retired') {
			return [__('Retired'), 'red', 'status,=,Retired'];
		}
	},
	
	onload: function(listview) {
		// Add custom button to view warranty expiry report
		listview.page.add_inner_button(__('Warranty Expiry Report'), function() {
			frappe.set_route('query-report', 'Warranty Expiry Report');
		});
		
		// Add custom button to view equipment by customer
		listview.page.add_inner_button(__('Equipment by Customer'), function() {
			frappe.set_route('query-report', 'Equipment by Customer');
		});
	},
	
	// Custom filters
	filters: [
		['status', '=', 'Active']
	]
};

