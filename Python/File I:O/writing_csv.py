import csv
import os

def main():
    
    if not os.path.exists("details.csv") or os.stat("details.csv").st_size == 0:

        col1 = input("Enter Column1 name: ")
        col2 = input("Enter Column2 name: ")
        column_names(col1,col2)

    else:
        with open("details.csv") as file:
            reader = csv.reader(file)
            col1, col2 = next(reader)

    name = input("Enter person name: ")
    place = input("Enter person place: ")
    people_details(name, place, col1, col2)



def column_names(col1,col2):

    with open("details.csv", "w") as file:

        writer = csv.writer(file)
        writer.writerow([col1,col2])



def people_details(name, place, col1, col2):

    with open("details.csv", "a") as file:

        writer = csv.DictWriter(file, fieldnames=[col1, col2])
        writer.writerow({col1: name, col2: place})



if __name__ == "__main__":
    main()






