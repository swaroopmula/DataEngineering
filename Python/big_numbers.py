def main():
    num1 = str(987654321234567)
    num2 = str(12345678987654345)

    total = sum_bignum(num1, num2)
    print(f"Sum of {num1} and {num2} is", total)

def sum_bignum(big1, big2):
    
    while len(big1) < len(big2):
        big1 = "0" + big1
    
    while len(big2) < len(big1):
        big2 = "0" + big2

    result = ""
    carry = 0

    for i in range(len(big1)-1, -1, -1):

        temp = int(big1[i]) + int(big2[i]) + carry
        carry = temp // 10

        result = str(temp % 10) + result

    if carry:
        result = str(carry) + result

    return result


if __name__ == "__main__":
    main()

    
