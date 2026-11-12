from decimal import Decimal, ROUND_HALF_UP

def r2(val):
    return val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

products = [
    {'id': 'github-copilot', 'name': 'GitHub Copilot', 'usd': Decimal('10.00'), 'retail': Decimal('3800.00')},
    {'id': 'cursor-ai-pro', 'name': 'Cursor AI Pro', 'usd': Decimal('20.00'), 'retail': Decimal('6800.00')},
    {'id': 'claude-pro', 'name': 'Claude Pro', 'usd': Decimal('20.00'), 'retail': Decimal('6800.00')}
]

scenarios = [
    Decimal('276.76'),
    Decimal('285.00'),
    Decimal('294.12'),
    Decimal('300.00'),
    Decimal('315.00')
]

# Bank fee: 4.0% cross-border fee
r_bank = Decimal('0.0400')
# FED on bank fee: 16.0% (applied strictly to the bank fee)
r_fed = Decimal('0.1600')
# Bank spread: 0.00% if bank converts at Visa/Mastercard reference rate and charges 4% all-inclusive fee
# Or Bank fee breakdown:
# Base PKR = USD * FX
# Bank conversion fee = Base PKR * 0.04
# FED = Bank conversion fee * 0.16
# Gross Remittance = Base PKR + Bank conversion fee + FED
# Section 236Y:
# ATL: 0.5% of Gross Remittance
# Non-ATL: 1.0% of Gross Remittance

labor_onboarding = Decimal('150.00')
labor_support = Decimal('200.00')
labor_total = labor_onboarding + labor_support
r_gateway = Decimal('0.0200') # 2.0% domestic gateway
r_reserve = Decimal('0.0500') # 5.0% warranty reserve on base PKR

# Let's verify for Copilot at 276.76 ATL
usd = Decimal('10.00')
fx = Decimal('276.76')
retail = Decimal('3800.00')

base_pkr = r2(usd * fx) # 2767.60
bank_fee = r2(base_pkr * r_bank) # 110.70
fed = r2(bank_fee * r_fed) # 17.71
total_bank = bank_fee + fed # 128.41
gross_remit = base_pkr + total_bank # 2896.01
sec236y_atl = r2(gross_remit * Decimal('0.0050')) # 14.48
landed_cash = gross_remit + sec236y_atl # 2910.49 or 2910.50

gateway_amt = r2(retail * r_gateway) # 76.00
reserve_amt = r2(base_pkr * r_reserve) # 138.38
chargeback_amt = Decimal('0.00')
total_cash_outlay = landed_cash + gateway_amt + labor_total + reserve_amt + chargeback_amt
net_cash = retail - total_cash_outlay
cash_margin = r2((net_cash / retail) * Decimal('100'))

# Target prices:
k_atl = (Decimal('1.00') + r_bank * (Decimal('1.00') + r_fed)) * Decimal('1.0050') + r_reserve
p_min_10 = r2((usd * fx * k_atl + labor_total) / Decimal('0.88'))
p_min_12 = r2((usd * fx * k_atl + labor_total) / Decimal('0.86'))
p_min_15 = r2((usd * fx * k_atl + labor_total) / Decimal('0.83'))

print(f"Copilot 276.76 ATL:")
print(f"  Base={base_pkr}, BankFee={bank_fee}, FED={fed}, GrossRemit={gross_remit}, Sec236Y={sec236y_atl}, LandedCash={landed_cash}")
print(f"  Total Cash Outlay={total_cash_outlay}, Net Cash={net_cash} ({cash_margin}%)")
print(f"  Min Price 10%: {p_min_10}, 12%: {p_min_12}, 15%: {p_min_15}")
