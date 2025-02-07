# Removing duplicates from a list of string (without using set conversion)

def main():

    list_of_str = ['a', 'b', 'c', 'd', 'b', 'a']
    list_of_str = remove_dup(list_of_str)
   
    print(list_of_str)


def remove_dup(current_list):

    new_list = []

    for item in current_list:
        if item not in new_list:
            new_list.append(item)

    return new_list


if __name__ == "__main__":
    main()

