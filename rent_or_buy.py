# http://www.in2013dollars.com/us/inflation/2000?amount=1 2000-2019
ANNUAL_CURRENCY_INFLATION = 0.0213
# https://www.neighborhoodscout.com/ca/san-francisco/real-estate 2000-2019
ANNUAL_HOME_APPRECIATION = 0.0501
ANNUAL_HOME_MAINTENANCE_INITIAL = 15000
ANNUAL_NON_HOME_ROI = 0.075
# https://smartasset.com/taxes/california-property-tax-calculator
ANNUAL_PROPERTY_TAX_RATE = .00683
# https://www.deptofnumbers.com/rent/california/san-francisco/ 2005-2017
ANNUAL_RENT_APPRECIATION = 0.023
HOME_DOWN_PAYMENT = 304660
HOME_PRICE = 1520330
# https://www.investopedia.com/articles/mortgages-real-estate/11/calculate-the-mortgage-interest-math.asp
MAX_MORTAGE_DEDUCTION_LOAN_AMOUNT = 750000
MONTHLY_HOA = 500
MONTHLY_HOME_INSURANCE = 698
MONTHLY_MORTGAGE = 5764
MONTHLY_RENT = 5450
MORTGAGE_INTEREST_RATE = .04051
MORTGAGE_YEARS = 30
# https://www.nerdwallet.com/blog/taxes/standard-deduction/ - assumes married
STANDARD_FEDERAL_DEDUCTION = 24400
# https://www.investopedia.com/terms/m/marginaltaxrate.asp - assumes income $200k-$500k
TOP_MARGINAL_FEDERAL_TAX_RATE = 0.35

def deductible_mortgage_interest_by_year():
  result = []
  annual_deducted_interest, principal_remaining = 0, HOME_PRICE - HOME_DOWN_PAYMENT
  max_deductible_principal = deductible_loan_amount()
  for month in range(12 * MORTGAGE_YEARS):
    max_deductible_interest = min(max_deductible_principal, principal_remaining)
    deducted_interest = max_deductible_interest * (MORTGAGE_INTEREST_RATE / 12)
    actual_interest = principal_remaining * (MORTGAGE_INTEREST_RATE / 12)
    principal_remaining -= (MONTHLY_MORTGAGE - actual_interest)
    if (month + 1) % 12 == 0:
      result.append(annual_deducted_interest)
      annual_deducted_interest = 0
    else:
      annual_deducted_interest += deducted_interest

  return result

def standard_deduction(year): # Assume it appreciates in line with inflation
  return STANDARD_FEDERAL_DEDUCTION * ((1 + ANNUAL_CURRENCY_INFLATION) ** year)

def mortgage_deduction_tax_savings(year, deductible_interest_by_year):
  mortgage_deduction_advantage = TOP_MARGINAL_FEDERAL_TAX_RATE * \
    (deductible_interest_by_year[year] - standard_deduction(year))
  return max(mortgage_deduction_advantage, 0)

def deductible_loan_amount():
  return max(HOME_PRICE - HOME_DOWN_PAYMENT, MAX_MORTAGE_DEDUCTION_LOAN_AMOUNT)

def hoa_payment(year):
  return 12 * MONTHLY_HOA * ((1 + ANNUAL_CURRENCY_INFLATION) ** year)

def home_value(year):
  return HOME_PRICE * ((1 + ANNUAL_HOME_APPRECIATION) ** year)

def insurance_payment(year):
  return 12 * MONTHLY_HOME_INSURANCE * ((1 + ANNUAL_HOME_APPRECIATION) ** year)

def maintenance_payment(year):
  return ANNUAL_HOME_MAINTENANCE_INITIAL * ((1 + ANNUAL_CURRENCY_INFLATION) ** year)

def mortgage_payment(year):
  return 12 * MONTHLY_MORTGAGE

def property_tax_payment(year):
  return home_value(year) * ANNUAL_PROPERTY_TAX_RATE

def annual_home_payment(year):
  return mortgage_payment(year) + property_tax_payment(year) + \
    hoa_payment(year) + insurance_payment(year) + maintenance_payment(year)

def annual_rent_payment(year):
  return 12 * MONTHLY_RENT * ((1 + ANNUAL_RENT_APPRECIATION) ** year)

def compare_net_worths_including_opportunity_costs(print_mortage_deduction_benefit = False):
  buy_asset_surplus, rent_asset_surplus = 0, HOME_DOWN_PAYMENT
  deductible_interest_by_year = deductible_mortgage_interest_by_year()

  for year in range(MORTGAGE_YEARS):
    buy_asset_surplus *= (1 + ANNUAL_NON_HOME_ROI)
    rent_asset_surplus *= (1 + ANNUAL_NON_HOME_ROI)
    payment_diff = annual_home_payment(year) - annual_rent_payment(year)
    payment_diff -= mortgage_deduction_tax_savings(year, deductible_interest_by_year)

    if print_mortage_deduction_benefit:
      print('Mortage tax deduction savings in year {}:'.format(year + 1))
      print('${}'.format(mortgage_deduction_tax_savings(year, deductible_interest_by_year)))

    if payment_diff < 0:
      buy_asset_surplus += -payment_diff
    else:
      rent_asset_surplus += payment_diff

  final_home_value = HOME_PRICE * ((1 + ANNUAL_HOME_APPRECIATION) ** MORTGAGE_YEARS)

  print('Net worth in year {} after renting: ${}, and only investing money saved by renting each year' \
    .format(MORTGAGE_YEARS, rent_asset_surplus))
  print('Net worth in year {} after buying: ${}, and only investing money saved by owning each year' \
    .format(MORTGAGE_YEARS, final_home_value + buy_asset_surplus))

compare_net_worths_including_opportunity_costs()
