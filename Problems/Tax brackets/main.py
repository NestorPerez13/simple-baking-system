income = int(input())
tax = 0
if 15_527 < income <= 42_707:
    tax = 0.15
elif 42_707 < income <= 132_406:
    tax = 0.25
elif income >= 132_407:
    tax = 0.28
calculated_tax = round(income * tax)
print(f"The tax for {income} is {int(tax * 100)}%. That is {calculated_tax} dollars!")
