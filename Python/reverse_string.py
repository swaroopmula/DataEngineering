# Reversing a String

def main():

    word = input("Enter a word: ").lower()
    reverse = reverse_string(word)

    print(f"Reverse of {word} is", reverse)

    if word == reverse:
        print(f"And, {word} is a palindrome!")


def reverse_string(word):

    new_word = ""
    
    for letter in word:
        new_word = letter + new_word
    return new_word


if __name__ == "__main__":
    main()


