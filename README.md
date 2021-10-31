# SWE Task

Create a rasa chatbot that extracts data from this [url](https://api.rootnet.in/covid19-in/stats/history) and is able to do the following. 

Can answer basic queries such as :
- Hey, what's the current confirmed cases in Delhi, Maharashtra etc?
- Hey, what’s the total count of confirmed cases in Delhi, Maharashtra altogether?
- What’s the confirmed case count from 1st Oct 2020 to 12th Oct 2020?
- Bonus Task : You can increase the complexity of this task by adding
    support for basic NLP.

Also demonstrate the following abilities for the chatbot
- Entity Extraction : For example Timestamps and states etc mentioned in the above tasks should be extracted and stored in the Slots.
- Custom Actions : Implement Custom Actions to demonstrate usage of api in them.
- BONUS TASKS :
    - Dockerization of the chatbot itself, just to show POC
    - Deployment of rasa server on place of your choosing, just to show POC.

# Approach
So basically the above task involves fetching covid cases for different states of India using some date filters.

So I have developed this bot using Rasa v.2.8.12, I have used [lookup table](https://rasa.com/docs/rasa/nlu-training-data#lookup-tables) for extracting the state names and [Duckling](https://rasa.com/docs/rasa/components#ducklingentityextractor) for date extraction

In my training data I have labelled the data for state names since lookup table requires atleast 2 examples in training

In my custom actions, I am extracting the state & date values from slot and then checking if date is present else it will take the current date,and then I call the above mentioned api for fetching the covid data and then search for the data based on the state & date parameters

to run the chatbot, please run the below command & makre sure you have docker & docker-compose setup on ur machines

> docker-compose up --build