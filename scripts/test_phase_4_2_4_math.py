from decimal import Decimal, ROUND_HALF_UP

def r2(val):
    return val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Let's verify K factor
r_bank = Decimal('0.04')
r_fed = Decimal('0.16')
bank_factor = Decimal('1.00') + r_bank * (Decimal('1.00') + r_fed) # 1.0464
r_reserve = Decimal('0.05')

k_cash_atl = bank_factor * Decimal('1.0050') + r_reserve # 1.101632
k_cash_non = bank_factor * Decimal('1.0100') + r_reserve # 1.106864
k_econ_atl = bank_factor + r_reserve # 1.0964

print(f"K cash ATL: {k_cash_atl}")
print(f"K cash Non-ATL: {k_cash_non}")
print(f"K econ ATL: {k_econ_atl}")

# Check break-even at current catalog prices:
# Copilot: retail = 3800, usd = 10
avail_copilot = Decimal('3800') * Decimal('0.98') - Decimal('350') # 3724 - 350 = 3374
be_copilot_cash_atl = avail_copilot / (Decimal('10') * k_cash_atl)
be_copilot_econ_atl = avail_copilot / (Decimal('10') * k_econ_atl)
print(f"Copilot (Retail 3800) Break-Even FX (Cash ATL): {r2(be_copilot_cash_atl)}")
print(f"Copilot (Retail 3800) Break-Even FX (Econ ATL): {r2(be_copilot_econ_atl)}")

# Cursor / Claude: retail = 6800, usd = 20
avail_cursor = Decimal('6800') * Decimal('0.98') - Decimal('350') # 6664 - 350 = 6314
be_cursor_cash_atl = avail_cursor / (Decimal('20') * k_cash_atl)
be_cursor_econ_atl = avail_cursor / (Decimal('20') * k_econ_atl)
print(f"Cursor/Claude (Retail 6800) Break-Even FX (Cash ATL): {r2(be_cursor_cash_atl)}")
print(f"Cursor/Claude (Retail 6800) Break-Even FX (Econ ATL): {r2(be_cursor_econ_atl)}")

# Check break-even at NEW proposed prices:
# What if Copilot is priced at 3900?
avail_copilot_3900 = Decimal('3900') * Decimal('0.98') - Decimal('350') # 3822 - 350 = 3472
be_copilot_3900 = avail_copilot_3900 / (Decimal('10') * k_cash_atl)
print(f"Copilot (Retail 3900) Break-Even FX: {r2(be_copilot_3900)}")

# What if Cursor/Claude is priced at 7400?
avail_cursor_7400 = Decimal('7400') * Decimal('0.98') - Decimal('350') # 7252 - 350 = 6902
be_cursor_7400 = avail_cursor_7400 / (Decimal('20') * k_cash_atl)
print(f"Cursor/Claude (Retail 7400) Break-Even FX: {r2(be_cursor_7400)}")

# What if Cursor/Claude is priced at 7320 (10% margin at 276.76)?
avail_cursor_7320 = Decimal('7320') * Decimal('0.98') - Decimal('350')
be_cursor_7320 = avail_cursor_7320 / (Decimal('20') * k_cash_atl)
print(f"Cursor/Claude (Retail 7320) Break-Even FX: {r2(be_cursor_7320)}")
