import re

def main():

    email = input("Enter your email address:").strip()
    print(email_validation(email))



def email_validation(email):

    if re.search(r"^[a-z]\w*[a-z0-9]+@([\w]+\.)?\w+\.(edu|com)$", email, re.IGNORECASE):
        return "Valid Email"
    
    else:
        return "Invalid Email"


if __name__ == "__main__":
    main()
