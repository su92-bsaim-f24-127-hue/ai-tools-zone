from decimal import Decimal, ROUND_HALF_UP

def r2(val):
    return val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Let's compare Copilot at 276.76
usd = Decimal('10.00')
fx = Decimal('276.76')
base = r2(usd * fx) # 2767.60

# Interpretation 1: Statutory Tax Base (Principal Only)
bank_fee = r2(base * Decimal('0.0400')) # 110.70
fed = r2(bank_fee * Decimal('0.1600')) # 17.71
total_bank = bank_fee + fed # 128.41
gross_remit = base + total_bank # 2896.01

sec236y_stat = r2(base * Decimal('0.0050')) # 13.84
landed_stat = gross_remit + sec236y_stat # 2909.85

# Interpretation 2: Disputed Gross Base (Gross Remittance)
sec236y_gross = r2(gross_remit * Decimal('0.0050')) # 14.48
landed_gross = gross_remit + sec236y_gross # 2910.49 (or 2910.50)

print(f"Base Principal: {base}")
print(f"Bank Fee + FED: {total_bank}")
print(f"Gross Remittance: {gross_remit}")
print(f"Statutory 236Y (Principal only): {sec236y_stat} -> Landed Cash: {landed_stat}")
print(f"Disputed 236Y (Gross Remittance): {sec236y_gross} -> Landed Cash: {landed_gross}")
print(f"Delta: {landed_gross - landed_stat} PKR")
