import random
import string

WORDLIST_FILENAME = "/Users/swaroop/DataEngineering/Python/MIT-2/words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print()
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):

    return random.choice(wordlist)


wordlist = load_words()



def is_word_guessed(secret_word, letters_guessed):
    
    for letter in secret_word:
        if letter not in letters_guessed:
            return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    
    word = ""
   
    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += "_"
    
    return word
                


def get_available_letters(letters_guessed):
    
    alphabets = list(string.ascii_lowercase)
    available_letters = ""

    for letter in alphabets:
        if letter not in letters_guessed:
            available_letters += letter
    
    return available_letters



def hangman(secret_word):
    
    guess_count = 6
    no_of_letters = len(secret_word)
    letters_guessed = []

    print("\nWelcome to the game Hangman!")
    print(f"I am thinking of a word that is {no_of_letters} letters long.")
    print("_" * no_of_letters)
    print()
    print(f"You have {guess_count} guesses left")
    print(get_available_letters(letters_guessed))

    while guess_count > 0:
    
        input_letter = input("\nPlease guess a letter: ").lower()

        if input_letter in letters_guessed:
            print(f"You've already guessed the letter '{input_letter}'. Try again!")
            continue
        
        letters_guessed.append(input_letter)

        if is_word_guessed(secret_word, letters_guessed):
            print("Good guess:", get_guessed_word(secret_word, letters_guessed))
            print("Congratulations! You've won!")
            break

        else:
            if input_letter in secret_word:
                print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
            else:
                
                guess_count -= 1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
           
            print(f"\nYou have {guess_count} guesses left")
            print(get_available_letters(letters_guessed))

    if not is_word_guessed(secret_word, letters_guessed):
        print("Sorry, you ran out of guesses. The word was else.\n") 



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
