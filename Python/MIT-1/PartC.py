# Program to calculate the best savings rate, and steps in bisection search

def main():

    annual_salary = float(input("Enter your starting annual salary: "))

    rate, steps = savings_rate(annual_salary)

    if rate == None:
        print("It is not possible to pay the down payment in three years.")
    else:
        print("Best savings rate:", rate)
        print("Steps in bisection search:", steps)


def savings_rate(a_salary):

    portion_down_payment = 1000000 * 0.25
    target_months = 36
    sal_raise = 0.07

    current_savings = 0
    returns = 0

    low = 0
    high = 10000
    best_rate = (high + low)//2
    steps = 0

    if a_salary/12 < portion_down_payment/target_months:
        return None, None
    
    while True:

        current_savings = 0
        salary = a_salary

        for month in range(1, target_months+1):

            portion_saved = (salary/12) * (best_rate/10000)
            returns = current_savings * (0.04/12)

            current_savings += portion_saved + returns

            if month % 6 == 0:
                salary += salary * sal_raise

        steps += 1

        if abs(current_savings - portion_down_payment) <= 100:
            break
        elif current_savings < portion_down_payment:
            low = best_rate
        else: 
            high = best_rate

        best_rate = (low+high)//2

    return best_rate / 10000, steps
    

if __name__ == "__main__":
    main()