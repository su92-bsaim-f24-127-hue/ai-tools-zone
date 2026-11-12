import csv
from decimal import Decimal, ROUND_HALF_UP

def r2(val):
    return val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

products = [
    {
        'id': 'claude',
        'name': 'Claude Pro',
        'slug': 'claude-pro',
        'retail_str': '$20.00',
        'usd': Decimal('20.00'),
        'period': '1 Month',
        'price': Decimal('6800.00'),
        'status': 'NOT AUTHORIZED (PENDING LEGAL/TAX REVIEW)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Concierge Virtual Card Facilitation'
    },
    {
        'id': 'cursor',
        'name': 'Cursor AI Pro',
        'slug': 'cursor-ai-pro',
        'retail_str': '$20.00',
        'usd': Decimal('20.00'),
        'period': '1 Month',
        'price': Decimal('6800.00'),
        'status': 'NOT AUTHORIZED (PENDING SUPPLIER VERIFICATION)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Developer Workspace Concierge Facilitation'
    },
    {
        'id': 'office365',
        'name': 'Microsoft Office 365 (1TB)',
        'slug': 'microsoft-office-365',
        'retail_str': '$16.66',
        'usd': Decimal('16.665'),
        'period': '1 Year (Per User Share of $99.99)',
        'price': Decimal('5500.00'),
        'status': 'NOT AUTHORIZED (PENDING PROVIDER AUTHORIZATION)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Family Tenant Share (1/6 of $99.99); Resale Prohibited under EULA'
    },
    {
        'id': 'grammarly',
        'name': 'Grammarly Premium',
        'slug': 'grammarly-premium',
        'retail_str': '$30.00',
        'usd': Decimal('30.00'),
        'period': '1 Month',
        'price': Decimal('7500.00'),
        'status': 'NOT AUTHORIZED (UNVIABLE AT RETAIL)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Monthly Benchmark; Wholesale Corporate Seat Required'
    },
    {
        'id': 'perplexity',
        'name': 'Perplexity Pro',
        'slug': 'perplexity-pro',
        'retail_str': '$20.00',
        'usd': Decimal('20.00'),
        'period': '1 Month',
        'price': Decimal('6800.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Concierge Card Facilitation'
    },
    {
        'id': 'copilot',
        'name': 'GitHub Copilot',
        'slug': 'github-copilot',
        'retail_str': '$10.00',
        'usd': Decimal('10.00'),
        'period': '1 Month',
        'price': Decimal('3800.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Individual Benchmark'
    },
    {
        'id': 'quillbot',
        'name': 'QuillBot Premium',
        'slug': 'quillbot-premium',
        'retail_str': '$9.95',
        'usd': Decimal('9.95'),
        'period': '1 Month',
        'price': Decimal('3800.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Monthly Benchmark'
    },
    {
        'id': 'coursera-plus',
        'name': 'Coursera Plus',
        'slug': 'coursera-plus-premium',
        'retail_str': '$59.00',
        'usd': Decimal('59.00'),
        'period': '1 Month',
        'price': Decimal('19500.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Monthly Benchmark'
    },
    {
        'id': 'runway',
        'name': 'Runway ML Gen-3',
        'slug': 'runway-ml-gen-3',
        'retail_str': '$15.00',
        'usd': Decimal('15.00'),
        'period': '1 Month',
        'price': Decimal('5500.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Standard Plan'
    },
    {
        'id': 'deepseek',
        'name': 'DeepSeek Unlimited',
        'slug': 'deepseek-unlimited',
        'retail_str': '$15.00',
        'usd': Decimal('15.00'),
        'period': '1 Month',
        'price': Decimal('5500.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Dedicated Developer API / Web Workspace Benchmark ($15.00/mo)'
    },
    {
        'id': 'bolt-new',
        'name': 'Bolt.new Pro',
        'slug': 'bolt-new-pro',
        'retail_str': '$20.00',
        'usd': Decimal('20.00'),
        'period': '1 Month',
        'price': Decimal('6800.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Monthly Benchmark'
    },
    {
        'id': 'descript',
        'name': 'Descript Creator',
        'slug': 'descript-creator',
        'retail_str': '$15.00',
        'usd': Decimal('15.00'),
        'period': '1 Month',
        'price': Decimal('5500.00'),
        'status': 'VIABLE AT PROPOSED RETAIL (Pending Supplier Verification)',
        'sources': 'SBP Rate (PKR 276.76, Nov 2026); FBR Sec 236Y TY2027 (0.5% ATL); Meezan/HBL FX Spread (4.0% + 16% FED = 4.64%); Direct Retail Monthly Benchmark'
    }
]

fx_rate = Decimal('276.76')
bank_spread_pct = Decimal('0.0400')
fed_pct = Decimal('0.1600')
sec236y_pct = Decimal('0.0050')

out_path = 'competitor-research/phase-3.1.4/97_independently_recalculated_financial_model.csv'

fieldnames = [
    'Product ID',
    'Product Name',
    'Canonical Slug',
    'Official Retail (USD)',
    'Subscription Billing Period',
    'USD Amount',
    'FX Benchmark and Source Date',
    'SBP Base FX Rate (PKR/USD)',
    'Base SBP Amount (PKR)',
    'Bank FX Spread %',
    'Bank Spread Amount (PKR)',
    'FED on Bank Fee %',
    'FED Amount (PKR)',
    'Total Bank Transaction Fee (PKR)',
    'Gross Remittance Outflow (PKR)',
    'Section 236Y Statutory Rate % (ATL)',
    'Section 236Y Advance Tax Cash Outlay (PKR)',
    'Total Cash Outlay (PKR)',
    'Adjustable Tax Credit (PKR)',
    'Economic Landed Cost (PKR)',
    'Onboarding Labor Expense (PKR)',
    'WhatsApp Support Labor Expense (PKR)',
    'Replacement Reserve (PKR)',
    'Other Documented Operating Expenses (PKR)',
    'Total Modeled Operating Cost (PKR)',
    'Proposed Customer Selling Price (PKR)',
    'Gross Contribution - Economic Basis (PKR)',
    'Gross Contribution Margin - Economic Basis %',
    'Gross Contribution - Cash Outlay Basis (PKR)',
    'Gross Contribution Margin - Cash Outlay Basis %',
    'Net Contribution (PKR)',
    'Net Contribution Margin %',
    'Commercial Status and Authorization Restrictions',
    'Evidence Date & Regulatory Sources'
]

rows = []
for p in products:
    usd = p['usd']
    base_pkr = r2(usd * fx_rate)
    bank_spread = r2(base_pkr * bank_spread_pct)
    fed = r2(bank_spread * fed_pct)
    total_bank_fee = bank_spread + fed
    gross_remittance = base_pkr + total_bank_fee
    sec236y = r2(gross_remittance * sec236y_pct)
    total_cash_outlay = gross_remittance + sec236y
    tax_credit = sec236y
    economic_cost = gross_remittance
    
    labor_onboarding = Decimal('150.00')
    labor_support = Decimal('200.00')
    reserve = r2(base_pkr * Decimal('0.05'))
    other_opex = Decimal('0.00')
    opex = labor_onboarding + labor_support + reserve + other_opex
    
    price = p['price']
    gross_contrib_econ = price - economic_cost
    gross_margin_econ_pct = r2((gross_contrib_econ / price) * Decimal('100'))
    
    gross_contrib_cash = price - total_cash_outlay
    gross_margin_cash_pct = r2((gross_contrib_cash / price) * Decimal('100'))
    
    net_contrib = gross_contrib_econ - opex
    net_margin_pct = r2((net_contrib / price) * Decimal('100'))
    
    row = {
        'Product ID': p['id'],
        'Product Name': p['name'],
        'Canonical Slug': p['slug'],
        'Official Retail (USD)': p['retail_str'],
        'Subscription Billing Period': p['period'],
        'USD Amount': f'{usd:.3f}' if usd == Decimal('16.665') else f'{usd:.2f}',
        'FX Benchmark and Source Date': 'SBP Customer Selling Rate (Nov 2026)',
        'SBP Base FX Rate (PKR/USD)': f'{fx_rate:.2f}',
        'Base SBP Amount (PKR)': f'{base_pkr:.2f}',
        'Bank FX Spread %': '4.00%',
        'Bank Spread Amount (PKR)': f'{bank_spread:.2f}',
        'FED on Bank Fee %': '16.00%',
        'FED Amount (PKR)': f'{fed:.2f}',
        'Total Bank Transaction Fee (PKR)': f'{total_bank_fee:.2f}',
        'Gross Remittance Outflow (PKR)': f'{gross_remittance:.2f}',
        'Section 236Y Statutory Rate % (ATL)': '0.50%',
        'Section 236Y Advance Tax Cash Outlay (PKR)': f'{sec236y:.2f}',
        'Total Cash Outlay (PKR)': f'{total_cash_outlay:.2f}',
        'Adjustable Tax Credit (PKR)': f'{tax_credit:.2f}',
        'Economic Landed Cost (PKR)': f'{economic_cost:.2f}',
        'Onboarding Labor Expense (PKR)': f'{labor_onboarding:.2f}',
        'WhatsApp Support Labor Expense (PKR)': f'{labor_support:.2f}',
        'Replacement Reserve (PKR)': f'{reserve:.2f}',
        'Other Documented Operating Expenses (PKR)': f'{other_opex:.2f}',
        'Total Modeled Operating Cost (PKR)': f'{opex:.2f}',
        'Proposed Customer Selling Price (PKR)': f'{price:.2f}',
        'Gross Contribution - Economic Basis (PKR)': f'{gross_contrib_econ:.2f}',
        'Gross Contribution Margin - Economic Basis %': f'{gross_margin_econ_pct:.2f}%',
        'Gross Contribution - Cash Outlay Basis (PKR)': f'{gross_contrib_cash:.2f}',
        'Gross Contribution Margin - Cash Outlay Basis %': f'{gross_margin_cash_pct:.2f}%',
        'Net Contribution (PKR)': f'{net_contrib:.2f}',
        'Net Contribution Margin %': f'{net_margin_pct:.2f}%',
        'Commercial Status and Authorization Restrictions': p['status'],
        'Evidence Date & Regulatory Sources': p['sources']
    }
    rows.append(row)

with open(out_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Successfully wrote {len(rows)} products to {out_path}')
