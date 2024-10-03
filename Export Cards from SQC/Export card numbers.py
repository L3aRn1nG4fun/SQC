#this script to to export card/pin from SafeQ cloud
#it will export  card/pin for users based on the csv
#CSV should contain at least one column "Username" with data
#During exporting, by default up to 4 card numbers will be exported and addition columns will be created in csv, specified as card1,2,3,4 , you can change this configuration in def export_all_cards():
#the API call needs to specify the user authentication provider id, change that in def export_card()
#the update csv with card numbers will be happened at the end of process, make sure you do not interrupt it until it stopped normally.

#configuration 
#define csv_file_path
#define api_key 
#define base_url2 
#define url_path_for_card for providerid

import csv
import requests
import urllib3

urllib3.disable_warnings()

# Define the CSV file path
csv_file_path = "C:/Path/userlist.csv"

# Define your API key
api_key = "your API key here"

# Define the base URL
base_url = "https://your_SQL_URL:7300/api/v1/users/"
base_url2 = "https://your_SQL_URL:7300/api/v1/users?username="


def export_card(username):
    url_path_for_card = base_url2 + username + "&providerid=1184"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url_path_for_card, headers=headers, verify=False)

    print("==============================================================")

    if response.status_code == 200:
        if not response.text:
            print(f"No data returned for {username}.")
            return []  # Return an empty list if there's no content
        
        try:

            data = response.json()
            card_numbers = data.get("cards",[])
            return card_numbers
        except ValueError as e:
            print(f"Error decoding JSON for {username}: {e}")
            return []  # Return an empty list if JSON decoding fails
    else:
        print (f"Error fetching cards for {username}: {response.status_code} {response.text}")
        return []


def export_all_cards():
    updated_rows =[]

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row["Username"]
            #print (username)
            card_numbers = export_card(username)
            if username:  # If username is not blank, start look up card for the username
                export_card(username)
                for i in range(4):  # Assuming you want to handle up to 4 cards
                    if i < len(card_numbers):
                        row[f"card{i + 1}"] = card_numbers[i]  # card1, card2, ...
                    else:
                        row[f"card{i + 1}"] = None  # Fill empty if no card number

                updated_rows.append(row)
               
            else:
                print("No Card number specified in cloud for " + username)
                print("==============================================================")

    # Write all updated rows back to the CSV file at the end
    with open(csv_file_path, mode='w', newline='') as file:
        fieldnames = reader.fieldnames + [f"card{i + 1}" for i in range(4)]  # Add new card columns
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # Write header
        writer.writerows(updated_rows)  # Write all updated rows



# Main program
export_all_cards()

