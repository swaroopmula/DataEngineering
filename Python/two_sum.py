# Two Sum

def main():

    num_list = [1, 2, 3, 4, 5, 6, 7]
    target_sum = int(input("Enter a number for which you want to do the Two Sum: "))

    print(twosum(target_sum, num_list))


def twosum(target, num_list):
    new_list = []
    for i in range(len(num_list)):
        for j in range(i + 1, len(num_list)): 
            if num_list[i] + num_list[j] == target:
                new_list.append([num_list[i], num_list[j]])

    return new_list
                
            
if __name__ == "__main__":
    main()




