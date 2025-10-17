# Customer Equipment DocType - Installation Guide

## ✅ What's Been Created

A complete **Customer Equipment** tracking system for passenger boarding bridges (PBB) and related assets has been added to the `kslsvcs_addons` app.

### 📦 Files Created: 23 files

- **1 DocType** (7 files): Customer Equipment
- **3 Reports** (9 files): Equipment by Customer, Warranty Expiry, Maintenance History  
- **Integration** (2 files): Custom fields for Issue, Sales Order, Project, etc.
- **Documentation** (4 files): Setup guides and references
- **Installation** (1 file): Automated installation script

---

## 🚀 Quick Installation

### Method 1: Using the Installation Script (Recommended)

```bash
# From the bench directory (/home/rust/erp15)
./apps/kslsvcs_addons/install_customer_equipment.sh kslsvcs.local
```

This script will:
- Check if the app is installed
- Run database migration
- Clear cache  
- Build assets
- Display success message

### Method 2: Manual Installation

```bash
# 1. Ensure bench services are running (in a separate terminal)
cd /home/rust/erp15
bench start

# 2. In another terminal, run migration
bench --site kslsvcs.local migrate

# 3. Clear cache
bench --site kslsvcs.local clear-cache

# 4. Build assets
bench build --app kslsvcs_addons
```

---

## 📍 Current Status

- ✅ All 23 files created successfully
- ✅ No linting errors
- ⚠️  **Migration pending** - Needs to be run to activate the doctype

**Note**: Your bench services had a port conflict (port 8000 in use by Laravel server). I've started bench on port 8001 in the background. You can access it at:
- **URL**: http://localhost:8001

---

## 🎯 Features Included

### 1. Customer Equipment DocType
- Track equipment name, customer, location
- Model number, serial number (unique)
- Installation & warranty dates with validation
- Status tracking (Active/In Service/Out of Service/Retired)
- Link to projects and contracts
- Notes and attachments

### 2. Automated Features
- ✅ Daily warranty expiry notifications (30-day warnings)
- ✅ Real-time warranty status indicators
- ✅ Quick action buttons (Create Issue, View History, Create Sales Order)

### 3. Reports
- **Equipment by Customer**: List all equipment per customer
- **Warranty Expiry Report**: Track expiring warranties with charts
- **Equipment Maintenance History**: Complete service history per equipment

### 4. Integrations
Custom "Equipment" field automatically added to:
- Issue (service tracking)
- Sales Order (sales linkage)
- Project (project management)
- Sales Invoice (billing)
- Delivery Note (installation tracking)

---

## 📚 Documentation

1. **CUSTOMER_EQUIPMENT_QUICK_START.txt** - Quick reference guide
2. **CUSTOMER_EQUIPMENT_SETUP.txt** - Detailed setup and features
3. **CUSTOMER_EQUIPMENT_STRUCTURE.txt** - Complete file structure and API reference
4. **README_INSTALLATION.md** - This file

---

## ✨ After Installation

### Access the DocType
```
Home > Kslsvcs Addons > Customer Equipment
```

### Create Your First Equipment
1. Click "New"
2. Fill in:
   - Equipment Name: e.g., "Jetway 4000 PBB"
   - Customer: Select from Customer master
   - Location: e.g., "Terminal 2, Gate A5"
   - Model & Serial Number
   - Installation Date
   - Warranty Expiry Date
   - Status: Active
3. Save

### Verify Integration
- Open **Issue** doctype → Check "Equipment" field exists
- Open **Sales Order** → Check "Equipment" field exists
- Open **Reports** > Kslsvcs Addons → See 3 new reports

---

## 🔧 Troubleshooting

### Issue: Doctype not appearing after migration
```bash
bench --site kslsvcs.local clear-cache
# Then hard refresh browser (Ctrl+Shift+R)
```

### Issue: Custom fields not showing
```bash
bench --site kslsvcs.local console

# In console:
from kslsvcs_addons.fixtures.custom_fields import create_equipment_custom_fields
create_equipment_custom_fields()
```

### Issue: Reports not showing
- Ensure at least one Customer Equipment record exists
- Check user permissions for the reports

### Issue: Bench services not starting
```bash
# Check what's using port 8000
lsof -i:8000

# Start on different port
bench start --port 8001
```

---

## 📞 Support

For issues or questions:
1. Check the detailed documentation in `CUSTOMER_EQUIPMENT_SETUP.txt`
2. Review the API reference in `CUSTOMER_EQUIPMENT_STRUCTURE.txt`
3. Check linter errors: No errors currently

---

## 🎉 Summary

All files are ready! Just run the installation script or manual migration to activate:

```bash
./apps/kslsvcs_addons/install_customer_equipment.sh kslsvcs.local
```

Then navigate to the DocType and start tracking your equipment!

---

**Created**: October 15, 2025  
**App**: kslsvcs_addons  
**ERPNext Version**: v15  
**Files**: 23 total (22 code + 1 script)

