weight = int(input('weight: '))
unit = input('(l)bs or (k)g: ')
if unit.upper() == "L":
    converted_weight = weight * 0.45359237
    print(f'Weight in kg: {converted_weight} kilograms')
else:
    converted_weight = weight / 0.45359237
    print(f'Your weight in lbs: {converted_weight} pounds')