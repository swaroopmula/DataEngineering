# Roman to Integer

def main():

    roman_num = {
    "I": 1,
    "V": 5,
    "X": 10,
    "C": 50,
    "L": 100,
    "D" : 500,
    "M" : 1000
    }

    roman_input = input("Enter a roman number: ")
    int_num = roman_to_int(roman_input.upper(), roman_num)

    print("The Equivalent integer number is", int_num)


def roman_to_int(roman, roman_dict):

    roman_list = list(roman)
    total = 0

    for i in range(len(roman_list)-1):

        if roman_dict.get(roman_list[i]) < roman_dict.get(roman_list[i+1]):
            total = total - roman_dict.get(roman_list[i])

        else: 
            total = total + roman_dict.get(roman_list[i])

    total = total + roman_dict.get(roman_list[i+1])
    return total


if __name__ == "__main__":
    main()




