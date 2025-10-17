#!/bin/bash

# Customer Equipment Installation Script
# This script will install the Customer Equipment doctype and all related features

echo "======================================================================"
echo "Customer Equipment - Installation Script"
echo "======================================================================"
echo ""

# Check if we're in the bench directory
if [ ! -f "sites/common_site_config.json" ]; then
    echo "Error: This script must be run from the bench directory (erp15)"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Get the site name
if [ -z "$1" ]; then
    echo "Usage: ./apps/kslsvcs_addons/install_customer_equipment.sh [site-name]"
    echo ""
    echo "Available sites:"
    ls -d sites/*/ | grep -v "assets" | grep -v "common_site_config" | sed 's|sites/||g' | sed 's|/||g'
    echo ""
    echo "Example: ./apps/kslsvcs_addons/install_customer_equipment.sh kslsvcs.local"
    exit 1
fi

SITE_NAME=$1

echo "Installing Customer Equipment on site: $SITE_NAME"
echo ""

# Step 1: Check if kslsvcs_addons is installed
echo "Step 1: Checking if kslsvcs_addons is installed..."
if ! bench --site $SITE_NAME list-apps | grep -q "kslsvcs_addons"; then
    echo "  → kslsvcs_addons not found on this site. Installing..."
    bench --site $SITE_NAME install-app kslsvcs_addons
else
    echo "  ✓ kslsvcs_addons is already installed"
fi
echo ""

# Step 2: Run migration
echo "Step 2: Running database migration..."
bench --site $SITE_NAME migrate
echo ""

# Step 3: Clear cache
echo "Step 3: Clearing cache..."
bench --site $SITE_NAME clear-cache
echo ""

# Step 4: Build assets (if needed)
echo "Step 4: Building assets..."
bench build --app kslsvcs_addons
echo ""

echo "======================================================================"
echo "Installation Complete!"
echo "======================================================================"
echo ""
echo "✓ Customer Equipment doctype installed"
echo "✓ 3 reports added (Equipment by Customer, Warranty Expiry, Maintenance History)"
echo "✓ Custom fields added to Issue, Sales Order, Project, Sales Invoice, Delivery Note"
echo "✓ Automated warranty notifications enabled"
echo ""
echo "Next steps:"
echo "1. Login to http://localhost:8001 (or your site URL)"
echo "2. Navigate to: Home > Kslsvcs Addons > Customer Equipment"
echo "3. Create your first equipment record"
echo ""
echo "Documentation:"
echo "- Quick Start: apps/kslsvcs_addons/CUSTOMER_EQUIPMENT_QUICK_START.txt"
echo "- Full Setup: apps/kslsvcs_addons/CUSTOMER_EQUIPMENT_SETUP.txt"
echo "- File Structure: apps/kslsvcs_addons/CUSTOMER_EQUIPMENT_STRUCTURE.txt"
echo ""
echo "======================================================================"

