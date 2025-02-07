# Program to calculate how many months it will take you save up enough money for a down payment (with salary raise)

def main():

    annual_salary = float(input("Enter your starting annual salary: "))
    portion_to_be_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream home: "))
    semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

    total_months = num_months_needed(total_cost, annual_salary, portion_to_be_saved, semi_annual_raise)
    print("Number of months needed:", total_months)


def num_months_needed(cost, a_salary, to_save, sal_raise):

    portion_down_payment = cost * 0.25

    month = 0
    portion_saved = 0
    current_savings = 0

    while current_savings < portion_down_payment:

        month += 1

        portion_saved = (a_salary/12) * to_save
        returns = current_savings * (0.04/12)

        current_savings += portion_saved + returns

        if month % 6 == 0:
            a_salary += a_salary * sal_raise

    return month


if __name__ == "__main__":
    main()