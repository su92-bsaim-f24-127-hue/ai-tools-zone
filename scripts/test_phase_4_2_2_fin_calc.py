from decimal import Decimal, ROUND_HALF_UP

def r2(val):
    return val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

products = [
    {'id': 'copilot', 'name': 'GitHub Copilot', 'usd': Decimal('10.00'), 'retail': Decimal('3800.00')},
    {'id': 'cursor', 'name': 'Cursor AI Pro', 'usd': Decimal('20.00'), 'retail': Decimal('6800.00')},
    {'id': 'claude', 'name': 'Claude Pro', 'usd': Decimal('20.00'), 'retail': Decimal('6800.00')}
]

scenarios = [
    Decimal('276.76'),
    Decimal('285.00'),
    Decimal('294.12'),
    Decimal('300.00'),
    Decimal('315.00')
]

bank_spread_pct = Decimal('0.0400') # 4.0%
fed_pct = Decimal('0.1600') # 16% on bank spread = 0.64% of base
total_bank_fee_pct = bank_spread_pct * (Decimal('1.00') + fed_pct) # 4.64%

atl_236y_pct = Decimal('0.0050') # 0.5% (TY2027)
non_atl_236y_pct = Decimal('0.0100') # 1.0% (TY2027)

labor_onboarding = Decimal('150.00')
labor_support = Decimal('200.00')
gateway_pct = Decimal('0.0200') # 2.0% domestic gateway fee

print("--- BASELINE SBP 276.76 ATL CALCULATIONS ---")
for p in products:
    usd = p['usd']
    retail = p['retail']
    fx = Decimal('276.76')
    base_pkr = r2(usd * fx)
    bank_fee = r2(base_pkr * total_bank_fee_pct)
    gross_remit = base_pkr + bank_fee
    sec236y_atl = r2(gross_remit * atl_236y_pct)
    total_cash_outlay_atl = gross_remit + sec236y_atl
    
    reserve = r2(base_pkr * Decimal('0.05')) # 5% replacement provision
    gateway = r2(retail * gateway_pct)
    opex = labor_onboarding + labor_support + reserve + gateway
    
    # Cash basis
    cash_collected = retail
    net_cash_contrib = cash_collected - total_cash_outlay_atl - opex
    net_cash_margin = r2((net_cash_contrib / cash_collected) * Decimal('100'))
    
    # Economic basis (advance tax is adjustable credit)
    econ_landed = gross_remit
    net_econ_contrib = cash_collected - econ_landed - opex
    net_econ_margin = r2((net_econ_contrib / cash_collected) * Decimal('100'))
    
    print(f"{p['id']}: Base={base_pkr}, BankFee={bank_fee}, GrossRemit={gross_remit}, Sec236Y={sec236y_atl}, Outlay={total_cash_outlay_atl}")
    print(f"   Opex={opex} (Reserve={reserve}, GW={gateway}, Labor={labor_onboarding+labor_support})")
    print(f"   Net Cash Contrib={net_cash_contrib} ({net_cash_margin}%), Net Econ Contrib={net_econ_contrib} ({net_econ_margin}%)")

print("\n--- SENSITIVITY TABLE ACROSS SCENARIOS ---")
for p in products:
    usd = p['usd']
    retail = p['retail']
    print(f"\nProduct: {p['name']} (Retail: PKR {retail}, USD: ${usd})")
    print(f"{'FX Rate':<10} | {'Status':<8} | {'Gross Remit':<12} | {'Sec 236Y':<10} | {'Cash Outlay':<12} | {'Net Cash (PKR)':<15} | {'Cash Margin':<12} | {'Net Econ (PKR)':<15} | {'Econ Margin':<12}")
    print("-" * 115)
    for fx in scenarios:
        base_pkr = r2(usd * fx)
        bank_fee = r2(base_pkr * total_bank_fee_pct)
        gross_remit = base_pkr + bank_fee
        reserve = r2(base_pkr * Decimal('0.05'))
        gateway = r2(retail * gateway_pct)
        opex = labor_onboarding + labor_support + reserve + gateway
        
        # ATL
        sec236y_atl = r2(gross_remit * atl_236y_pct)
        outlay_atl = gross_remit + sec236y_atl
        net_cash_atl = retail - outlay_atl - opex
        cash_margin_atl = r2((net_cash_atl / retail) * Decimal('100'))
        net_econ_atl = retail - gross_remit - opex
        econ_margin_atl = r2((net_econ_atl / retail) * Decimal('100'))
        print(f"{fx:<10} | {'ATL':<8} | {gross_remit:<12} | {sec236y_atl:<10} | {outlay_atl:<12} | {net_cash_atl:<15} | {cash_margin_atl}%{'':<6} | {net_econ_atl:<15} | {econ_margin_atl}%")
        
        # Non-ATL
        sec236y_non = r2(gross_remit * non_atl_236y_pct)
        outlay_non = gross_remit + sec236y_non
        net_cash_non = retail - outlay_non - opex
        cash_margin_non = r2((net_cash_non / retail) * Decimal('100'))
        # For non-filer who cannot adjust advance tax, economic cost includes the unrecoverable tax
        net_econ_non = retail - outlay_non - opex
        econ_margin_non = r2((net_econ_non / retail) * Decimal('100'))
        print(f"{fx:<10} | {'Non-ATL':<8} | {gross_remit:<12} | {sec236y_non:<10} | {outlay_non:<12} | {net_cash_non:<15} | {cash_margin_non}%{'':<6} | {net_econ_non:<15} | {econ_margin_non}%")

print("\n--- BREAK-EVEN EXCHANGE RATES ---")
for p in products:
    usd = p['usd']
    retail = p['retail']
    # Break-even when Net Cash Contrib = 0 or Net Econ Contrib = 0
    # Net Econ = retail - gross_remit - opex = 0
    # retail - (usd*fx*(1 + bank_fee_pct)) - (labor + reserve + gateway) = 0
    # reserve = usd*fx * 0.05
    # retail - labor - gateway = usd*fx * (1 + bank_fee_pct + 0.05)
    # fx = (retail - labor - gateway) / (usd * (1 + bank_fee_pct + 0.05))
    gateway = r2(retail * gateway_pct)
    labor = labor_onboarding + labor_support
    available_for_procurement = retail - labor - gateway
    cost_factor_econ = (Decimal('1.00') + total_bank_fee_pct + Decimal('0.05'))
    be_fx_econ = r2(available_for_procurement / (usd * cost_factor_econ))
    
    # Cash basis ATL
    # retail - labor - gateway = usd*fx * [ (1 + bank_fee_pct)*(1 + atl_236y) + 0.05 ]
    cost_factor_cash_atl = (Decimal('1.00') + total_bank_fee_pct) * (Decimal('1.00') + atl_236y_pct) + Decimal('0.05')
    be_fx_cash_atl = r2(available_for_procurement / (usd * cost_factor_cash_atl))

    # Cash basis Non-ATL
    cost_factor_cash_non = (Decimal('1.00') + total_bank_fee_pct) * (Decimal('1.00') + non_atl_236y_pct) + Decimal('0.05')
    be_fx_cash_non = r2(available_for_procurement / (usd * cost_factor_cash_non))

    print(f"{p['name']}:")
    print(f"   Break-even FX (Economic Basis): PKR {be_fx_econ} / USD")
    print(f"   Break-even FX (Cash Basis ATL 0.5%): PKR {be_fx_cash_atl} / USD")
    print(f"   Break-even FX (Cash Basis Non-ATL 1.0%): PKR {be_fx_cash_non} / USD")
