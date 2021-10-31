# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import logging
from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime as dt
from api import getStats, fetchData

logger = logging.getLogger(__name__)


class ActionGetCases(Action):
    def name(self) -> Text:
        return "action_get_cases"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        states = tracker.get_slot("state")
        logger.info(states)
        dt_str = tracker.get_slot("time")
        from_date = None
        to_date = None
        user_message = tracker.latest_message["text"]
        altogether = True if 'altogether' in user_message.lower() else False 

        if type(dt_str) == str:  # if only one date is provided
            dt_str = dt.strptime(dt_str, "%Y-%m-%dT%H:%M:%S.%f%z")
            from_date = dt_str.strftime("%Y-%m-%d")

        if type(dt_str) == dict:  # if from & to date is provided
            from_date = dt.strptime(dt_str["from"], "%Y-%m-%dT%H:%M:%S.%f%z")
            from_date = from_date.strftime("%Y-%m-%d")
            to_date = dt.strptime(dt_str["to"], "%Y-%m-%dT%H:%M:%S.%f%z")
            to_date = to_date.strftime("%Y-%m-%d")

        if dt_str == None:  # if no dates are provided
            dt_str = dt.now()
            from_date = dt_str.strftime("%Y-%m-%d")

        data = fetchData()

        filtered_data = getStats(states, from_date, to_date, data, altogether)
        cases = filtered_data["cases"]
        state_cases = filtered_data["state_cases"]

        message = ""
        if not altogether:
            if states:
                for item in state_cases:
                    message = (
                        message + f'• State: {item["state"]}, Cases: {item["cases"]}\n'
                    )
                message = message if message != "" else "No data found"
            else:
                message = (
                    f"Total cases found: {cases}" if cases > 0 else "No cases found"
                )
        else:
            if states:
                for item in state_cases:
                    cases = cases + item["cases"]
                message = (
                    f"Total cases found: {cases}" if cases > 0 else "No cases found"
                )
            else:
                message = cases if cases > 0 else "No data found"
        dispatcher.utter_message(text=message)
        return [AllSlotsReset()]
