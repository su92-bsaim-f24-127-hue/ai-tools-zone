#!/usr/bin/env python3
"""
Automated Financial Reconciliation & Commercial Lock Test Suite
AI Tools Zone - Phase 3.1.4 Independent Quality Gate

Verifies the mathematical integrity, Decimal arithmetic precision,
statutory tax logic, and commercial authorization locks for all 12 Group A products.
"""

import sys
import csv
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

def r2(val: Decimal) -> Decimal:
    """Standardized commercial banking half-up rounding to 2 decimal places."""
    return val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def run_financial_reconciliation_tests() -> bool:
    repo_root = Path(__file__).resolve().parent.parent
    csv_path = repo_root / 'competitor-research' / 'phase-3.1.4' / '97_independently_recalculated_financial_model.csv'
    
    if not csv_path.exists():
        print(f"FAIL: Deliverable 97 CSV not found at {csv_path}")
        return False
        
    print(f"Loading financial model from: {csv_path}")
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Total products loaded: {len(rows)}")
    
    if len(rows) != 12:
        print(f"FAIL: Expected exactly 12 Group A products, found {len(rows)}")
        return False
        
    expected_ids = {
        'claude', 'cursor', 'office365', 'grammarly',
        'perplexity', 'copilot', 'quillbot', 'coursera-plus',
        'runway', 'deepseek', 'bolt-new', 'descript'
    }
    
    found_ids = {r['Product ID'] for r in rows}
    missing_ids = expected_ids - found_ids
    if missing_ids:
        print(f"FAIL: Missing expected Group A product IDs: {missing_ids}")
        return False
        
    print(f"PASS: All 12 Group A product IDs present.")
    
    tolerance = Decimal('0.01')
    errors = []
    
    for row in rows:
        pid = row['Product ID']
        name = row['Product Name']
        
        # Parse inputs
        usd = Decimal(row['USD Amount'])
        fx_rate = Decimal(row['SBP Base FX Rate (PKR/USD)'])
        price = Decimal(row['Proposed Customer Selling Price (PKR)'])
        
        # Reported values
        rep_base = Decimal(row['Base SBP Amount (PKR)'])
        rep_bank_spread = Decimal(row['Bank Spread Amount (PKR)'])
        rep_fed = Decimal(row['FED Amount (PKR)'])
        rep_bank_fee = Decimal(row['Total Bank Transaction Fee (PKR)'])
        rep_gross_remit = Decimal(row['Gross Remittance Outflow (PKR)'])
        rep_sec236y = Decimal(row['Section 236Y Advance Tax Cash Outlay (PKR)'])
        rep_cash_outlay = Decimal(row['Total Cash Outlay (PKR)'])
        rep_tax_credit = Decimal(row['Adjustable Tax Credit (PKR)'])
        rep_econ_cost = Decimal(row['Economic Landed Cost (PKR)'])
        rep_labor_onboarding = Decimal(row['Onboarding Labor Expense (PKR)'])
        rep_labor_support = Decimal(row['WhatsApp Support Labor Expense (PKR)'])
        rep_reserve = Decimal(row['Replacement Reserve (PKR)'])
        rep_other_opex = Decimal(row['Other Documented Operating Expenses (PKR)'])
        rep_opex = Decimal(row['Total Modeled Operating Cost (PKR)'])
        rep_gross_contrib_econ = Decimal(row['Gross Contribution - Economic Basis (PKR)'])
        rep_gross_margin_econ_pct = Decimal(row['Gross Contribution Margin - Economic Basis %'].replace('%', ''))
        rep_gross_contrib_cash = Decimal(row['Gross Contribution - Cash Outlay Basis (PKR)'])
        rep_gross_margin_cash_pct = Decimal(row['Gross Contribution Margin - Cash Outlay Basis %'].replace('%', ''))
        rep_net_contrib = Decimal(row['Net Contribution (PKR)'])
        rep_net_margin_pct = Decimal(row['Net Contribution Margin %'].replace('%', ''))
        status = row['Commercial Status and Authorization Restrictions']
        
        # Independent recalculation using Decimal
        calc_base = r2(usd * fx_rate)
        calc_bank_spread = r2(calc_base * Decimal('0.0400'))
        calc_fed = r2(calc_bank_spread * Decimal('0.1600'))
        calc_bank_fee = calc_bank_spread + calc_fed
        calc_gross_remit = calc_base + calc_bank_fee
        calc_sec236y = r2(calc_gross_remit * Decimal('0.0050'))
        calc_cash_outlay = calc_gross_remit + calc_sec236y
        calc_tax_credit = calc_sec236y
        calc_econ_cost = calc_gross_remit
        
        calc_labor_onboarding = Decimal('150.00')
        calc_labor_support = Decimal('200.00')
        calc_reserve = r2(calc_base * Decimal('0.05'))
        calc_other_opex = Decimal('0.00')
        calc_opex = calc_labor_onboarding + calc_labor_support + calc_reserve + calc_other_opex
        
        calc_gross_contrib_econ = price - calc_econ_cost
        calc_gross_margin_econ_pct = r2((calc_contrib := calc_gross_contrib_econ / price) * Decimal('100'))
        
        calc_gross_contrib_cash = price - calc_cash_outlay
        calc_gross_margin_cash_pct = r2((calc_gross_contrib_cash / price) * Decimal('100'))
        
        calc_net_contrib = calc_gross_contrib_econ - calc_opex
        calc_net_margin_pct = r2((calc_net_contrib / price) * Decimal('100'))
        
        # Assertions with tolerance check
        def check_diff(field_name, rep, calc):
            diff = abs(rep - calc)
            if diff > tolerance:
                errors.append(f"{pid} ({name}) - {field_name} discrepancy: reported {rep} vs calculated {calc} (diff {diff})")

        check_diff("Base SBP Amount", rep_base, calc_base)
        check_diff("Bank Spread", rep_bank_spread, calc_bank_spread)
        check_diff("FED on Bank Fee", rep_fed, calc_fed)
        check_diff("Total Bank Fee", rep_bank_fee, calc_bank_fee)
        check_diff("Gross Remittance", rep_gross_remit, calc_gross_remit)
        check_diff("Section 236Y Advance Tax", rep_sec236y, calc_sec236y)
        check_diff("Total Cash Outlay", rep_cash_outlay, calc_cash_outlay)
        check_diff("Adjustable Tax Credit", rep_tax_credit, calc_tax_credit)
        check_diff("Economic Landed Cost", rep_econ_cost, calc_econ_cost)
        check_diff("Replacement Reserve", rep_reserve, calc_reserve)
        check_diff("Total OPEX", rep_opex, calc_opex)
        check_diff("Gross Contribution (Economic)", rep_gross_contrib_econ, calc_gross_contrib_econ)
        check_diff("Gross Margin % (Economic)", rep_gross_margin_econ_pct, calc_gross_margin_econ_pct)
        check_diff("Gross Contribution (Cash Outlay)", rep_gross_contrib_cash, calc_gross_contrib_cash)
        check_diff("Gross Margin % (Cash Outlay)", rep_gross_margin_cash_pct, calc_gross_margin_cash_pct)
        check_diff("Net Contribution", rep_net_contrib, calc_net_contrib)
        check_diff("Net Margin %", rep_net_margin_pct, calc_net_margin_pct)
        
        # Verify commercial authorization lock enforcement
        if pid == 'claude':
            if 'PENDING LEGAL/TAX REVIEW' not in status and 'NOT AUTHORIZED' not in status:
                errors.append(f"claude missing required legal/tax commercial restriction in status: {status}")
        elif pid == 'cursor':
            if 'PENDING SUPPLIER VERIFICATION' not in status and 'NOT AUTHORIZED' not in status:
                errors.append(f"cursor missing required supplier verification restriction in status: {status}")
        elif pid == 'office365':
            if 'PENDING PROVIDER AUTHORIZATION' not in status and 'NOT AUTHORIZED' not in status:
                errors.append(f"office365 missing required provider authorization restriction in status: {status}")
        elif pid == 'grammarly':
            if 'UNVIABLE AT RETAIL' not in status and 'NOT AUTHORIZED' not in status:
                errors.append(f"grammarly missing required unviable commercial restriction in status: {status}")
            if rep_net_contrib >= 0:
                errors.append(f"grammarly net contribution must be negative (retail deficit), found: {rep_net_contrib}")

    if errors:
        print(f"FAIL: {len(errors)} financial reconciliation errors found:")
        for err in errors:
            print(f"  - {err}")
        return False

    print("PASS: All 12 Group A products independently recalculated and verified with 0 discrepancies (tolerance <= 0.01 PKR).")
    print("PASS: Section 236Y advance tax rate (0.50% ATL) and adjustable tax credit logic confirmed.")
    print("PASS: Commercial authorization locks strictly enforced on Claude Pro, Cursor AI Pro, Microsoft 365, and Grammarly.")
    return True

if __name__ == '__main__':
    success = run_financial_reconciliation_tests()
    sys.exit(0 if success else 1)
