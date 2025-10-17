// Copyright (c) 2025, itsyosefali and contributors
// For license information, please see license.txt

frappe.listview_settings['Service Call'] = {
	get_indicator: function(doc) {
		const status_colors = {
			'Open': 'red',
			'In Progress': 'orange',
			'Completed': 'green',
			'Billed': 'blue',
			'Cancelled': 'gray'
		};
		
		return [__(doc.status), status_colors[doc.status] || 'gray', 'status,=,' + doc.status];
	},
	
	onload: function(listview) {
		// Add custom button to create new service call
		listview.page.add_inner_button(__('Schedule Service Call'), function() {
			frappe.new_doc('Service Call');
		});
	}
};

