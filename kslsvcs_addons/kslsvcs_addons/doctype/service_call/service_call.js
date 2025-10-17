// Copyright (c) 2025, itsyosefali and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Call', {
	refresh: function(frm) {
		// Add custom buttons
		if (!frm.is_new()) {
			// Button to complete service call
			if (frm.doc.status !== 'Completed' && frm.doc.status !== 'Billed') {
				frm.add_custom_button(__('Mark as Completed'), function() {
					frappe.call({
						method: 'frappe.client.set_value',
						args: {
							doctype: 'Service Call',
							name: frm.doc.name,
							fieldname: {
								'status': 'Completed',
								'completion_date': frappe.datetime.now_datetime()
							}
						},
						callback: function(r) {
							frm.reload_doc();
						}
					});
				});
			}
			
			// Button to create sales invoice
			if (frm.doc.status === 'Completed' && !frm.doc.sales_invoice && frm.doc.is_billable) {
				frm.add_custom_button(__('Create Sales Invoice'), function() {
					frappe.model.open_mapped_doc({
						method: 'kslsvcs_addons.kslsvcs_addons.doctype.service_call.service_call.make_sales_invoice',
						frm: frm
					});
				}, __('Create'));
			}
			
			// Button to view customer equipment
			if (frm.doc.customer_equipment) {
				frm.add_custom_button(__('View Equipment'), function() {
					frappe.set_route('Form', 'Customer Equipment', frm.doc.customer_equipment);
				});
			}
			
			// Add status indicator
			frm.page.set_indicator(__('Status: {0}', [frm.doc.status]), 
				frm.doc.status === 'Completed' ? 'green' : 
				frm.doc.status === 'In Progress' ? 'orange' : 
				frm.doc.status === 'Billed' ? 'blue' : 'red');
		}
		
		// Set default scheduled date to now if new
		if (frm.is_new() && !frm.doc.scheduled_date) {
			frm.set_value('scheduled_date', frappe.datetime.now_datetime());
		}
		
		// Set primary technician to current user if new
		if (frm.is_new() && !frm.doc.primary_technician) {
			frm.set_value('primary_technician', frappe.session.user);
		}
	},
	
	customer: function(frm) {
		// Filter customer equipment based on selected customer
		if (frm.doc.customer) {
			frm.set_query('customer_equipment', function() {
				return {
					filters: {
						'customer': frm.doc.customer
					}
				};
			});
			
			// Clear equipment if customer changes
			if (frm.doc.customer_equipment) {
				frappe.db.get_value('Customer Equipment', frm.doc.customer_equipment, 'customer', function(r) {
					if (r && r.customer !== frm.doc.customer) {
						frm.set_value('customer_equipment', '');
					}
				});
			}
		}
	},
	
	customer_equipment: function(frm) {
		// Load default checklist from equipment type if available
		if (frm.doc.customer_equipment && frm.is_new()) {
			// You can customize this to load a standard checklist based on equipment type
			frappe.msgprint(__('Add checklist items for this service call'));
		}
	},
	
	status: function(frm) {
		// Auto-set completion date when status changes to Completed
		if (frm.doc.status === 'Completed' && !frm.doc.completion_date) {
			frm.set_value('completion_date', frappe.datetime.now_datetime());
		}
	},
	
	scheduled_date: function(frm) {
		// Validate scheduled date
		if (frm.doc.scheduled_date && frm.doc.completion_date) {
			if (frm.doc.completion_date < frm.doc.scheduled_date) {
				frappe.msgprint(__('Completion date cannot be before scheduled date'));
				frm.set_value('completion_date', '');
			}
		}
	},
	
	completion_date: function(frm) {
		// Validate completion date
		if (frm.doc.completion_date && frm.doc.scheduled_date) {
			if (frm.doc.completion_date < frm.doc.scheduled_date) {
				frappe.msgprint(__('Completion date cannot be before scheduled date'));
				frm.set_value('completion_date', '');
			}
		}
	}
});

// Child table: Service Call Checklist
frappe.ui.form.on('Service Call Checklist', {
	is_completed: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		
		// Auto-fill completed by and date when checkbox is checked
		if (row.is_completed) {
			frappe.model.set_value(cdt, cdn, 'completed_by', frappe.session.user);
			frappe.model.set_value(cdt, cdn, 'completed_date', frappe.datetime.now_datetime());
		}
	}
});

// Child table: Service Call Material
frappe.ui.form.on('Service Call Material', {
	item_code: function(frm, cdt, cdn) {
		let row = locals[cdt][cdn];
		
		// Fetch item rate
		if (row.item_code) {
			frappe.call({
				method: 'frappe.client.get_value',
				args: {
					doctype: 'Item',
					filters: { name: row.item_code },
					fieldname: ['standard_rate', 'item_name', 'description']
				},
				callback: function(r) {
					if (r.message) {
						frappe.model.set_value(cdt, cdn, 'rate', r.message.standard_rate);
					}
				}
			});
		}
	},
	
	qty: function(frm, cdt, cdn) {
		calculate_material_amount(frm, cdt, cdn);
	},
	
	rate: function(frm, cdt, cdn) {
		calculate_material_amount(frm, cdt, cdn);
	},
	
	materials_used_remove: function(frm) {
		calculate_total_material_cost(frm);
	}
});

function calculate_material_amount(frm, cdt, cdn) {
	let row = locals[cdt][cdn];
	let amount = (row.qty || 0) * (row.rate || 0);
	frappe.model.set_value(cdt, cdn, 'amount', amount);
	calculate_total_material_cost(frm);
}

function calculate_total_material_cost(frm) {
	let total = 0;
	
	if (frm.doc.materials_used) {
		frm.doc.materials_used.forEach(function(material) {
			total += (material.amount || 0);
		});
	}
	
	frm.set_value('total_material_cost', total);
}

