import csv

def main():

    read_people_deets()



def read_people_deets():
    
    people = []

    with open("details.csv") as file:

        reader = csv.DictReader(file)

        for row in reader: 
            people.append(row)

    for person in people:
        print(f"{person['name']} lives in {person['place']}")



if __name__ == "__main__":
    main()