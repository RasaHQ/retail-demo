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
import sqlite3


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        conn = sqlite3.connect("example.db")
        c = conn.cursor()

        # get slots
        shoe = [(tracker.get_slot("color")), (tracker.get_slot("number"))]

        # retrieve row based on search criteria
        c.execute("SELECT * FROM inventory WHERE color=? AND size=?", shoe)
        rw = c.fetchone()

        if rw:
            # provide in stock message
            dispatcher.utter_message(template="utter_in_stock")
            conn.close()
            reset_slots = ["number", "color"]
            return [SlotSet(slot, None) for slot in reset_slots]
        else:
            # provide out of stock
            dispatcher.utter_message(template="utter_no_stock")
            conn.close()
            reset_slots = ["number", "color"]
            return [SlotSet(slot, None) for slot in reset_slots]


class SurveyStart(Action):
    def name(self) -> Text:
        return "action_survey_start"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        if tracker.get_slot("survey_complete") == True:
            return []
        else:
            return [FollowupAction("survey_form"), SlotSet("number", None)]


class SurveySubmit(Action):
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(template="utter_open_feedback")
        dispatcher.utter_message(template="utter_survey_end")
        return [SlotSet("survey_complete", True), SlotSet("number", None)]


class OrderStatus(Action):
    def name(self) -> Text:
        return "action_order_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        conn = sqlite3.connect("example.db")
        c = conn.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        c.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        rw = c.fetchone()

        if rw:
            rw_lst = list(rw)

            # respond with order status
            dispatcher.utter_message(template="utter_order_status", status=rw_lst[5])
            conn.close()
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            conn.close()
            return []


class CancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        conn = sqlite3.connect("example.db")
        c = conn.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        c.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        rw = c.fetchone()

        if rw:
            # change status of entry
            status = [("cancelled"), (tracker.get_slot("email"))]
            c.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            conn.commit()
            conn.close()

            # confirm cancellation
            dispatcher.utter_message(template="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            conn.close()
            return []


class ReturnOrder(Action):
    def name(self) -> Text:
        return "action_return"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # connect to DB
        conn = sqlite3.connect("example.db")
        c = conn.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        c.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        rw = c.fetchone()

        if rw:
            # change status of entry
            status = [("returning"), (tracker.get_slot("email"))]
            c.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            conn.commit()
            conn.close()

            # confirm return
            dispatcher.utter_message(template="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            conn.close()
            return []
