# Program to calculate how many months it will take you to save up enough money for a down payment

def main():

    annual_salary = float(input("Enter your annual salary: "))
    portion_to_be_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream home: "))

    total_months = num_months_needed(total_cost, annual_salary, portion_to_be_saved)
    print("Number of months needed:", total_months)


def num_months_needed(cost, a_salary, to_save):

    portion_down_payment = cost * 0.25

    month = 0
    portion_saved = 0
    current_savings = 0

    while current_savings < portion_down_payment:

        portion_saved = (a_salary/12) * to_save
        returns = current_savings * (0.04/12)

        current_savings += portion_saved + returns

        month += 1

    return month


if __name__ == "__main__":
    main()