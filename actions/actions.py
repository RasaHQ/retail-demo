# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction


class ActionProductSearch(Action):

    def name(self) -> Text:
        return "action_product_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template = "utter_product_stock_finish")
        reset_slots = ["number", "color"]
        return [SlotSet(slot, None) for slot in reset_slots]
        # return []

class SurveyStart(Action):

    def name(self) -> Text:
        return "action_survey_start"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot("survey_complete")==True:
            return[]
        else: 
            return [FollowupAction("survey_form")]

class SurveySubmit(Action):

    def name(self) -> Text:
        return "action_survey_submit"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template = "utter_open_feedback")
        dispatcher.utter_message(template = "utter_survey_end")
        return [SlotSet("survey_complete", True)]


