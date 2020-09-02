import requests
import json
import re
from dotenv import load_dotenv
import os
import datetime
import time

class FAQGenerator:

    # Constructor
    def __init__(self):

        # Dot env
        load_dotenv()

        self.CHANNEL_ID = os.getenv("CHANNEL_ID")
        self.OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")


    # Process the String
    def __process_string(self, text):
        # text.replace("[<@]+[a-zA-Z0-9>]", "")
        text = re.sub("([<@]+[a-zA-Z0-9>])", "", text)

        return text;

    # get the filter input from user
    def __get_filters(self):


        print("""

            🔥 Welcome to FAQ Extractor 🔥

        """)
        print("Please enter the bellow details to get your FAQs as JSON file \n");

        filters = {
            "time_limit" : None,
            "speaker_id": None,
        }
        print("When was the session started?(Unix timestamp)")

        # Get the date time input
        date = int(input("Date = "))
        month = int(input("Month = "))
        year = int(input("Year = "))
        hours = int(input("Hour = "))
        minutes = int(input("Minute = "))

        # Convert the date time to Unix timestamp
        dt = datetime.datetime(year, month, date, hours, minutes)
        time_stamp = time.mktime(dt.timetuple())
        filter["time_limit"] = time_stamp;
         
        # Get the speaker ID
        filters['speaker_id'] = input("\nWhat is the speaker's user id? ");

        # Return the filters
        return {"time_limit": "1598764092", "speaker_id":"U019TPK0GP6"}


    # Get the FAQ Dictionary
    def __get_faq(self, filters):

        faqs = []

        # Get the conversation history of the defined channel
        conversation = requests.get("https://slack.com/api/conversations.history?token=" + self.OAUTH_TOKEN +"&channel=" + self.CHANNEL_ID + "&oldest="+ filters["time_limit"] + "&pretty=1").json()

        # Get the thread replies
        for i in conversation['messages']:

            # extract the question 
            faq = {
                "question":self.__process_string(i['text']),
                "answer": ""
            }


            thread = requests.get("https://slack.com/api/conversations.replies?token=" + self.OAUTH_TOKEN + "&channel=" + self.CHANNEL_ID + "&ts=" + i['thread_ts'] + "&pretty=1").json();

            for j in thread['messages']:
                if (j['user'] == filters["speaker_id"]):
                    faq["answer"] += " " + self.__process_string(j['text'])
            

            faqs.append(faq)

        return faqs

    # Convert the dictionary to JSON file
    def __convert_to_json(self, faqs):
        with open("faqs.json", "w") as outfile:  
            json.dump(faqs, outfile)

        print("""
            Hurray!🥳 JSON file created and data extracted!
            """)
    
    # Start the FAQ Generation
    def generate_FAQs(self):
         # Get the filter from user
        filters = self.__get_filters()

        # Extract the FAQs from the channel
        faqs = self.__get_faq(filters)

        # Convert it to JSON file
        self.__convert_to_json(faqs)


if __name__=="__main__":
    task = FAQGenerator()
    task.generate_FAQs()