from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import BotUttered
from datetime import datetime

import sqlite3

# change this to the location of your SQLite file
path_to_db = "actions/example.db"

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
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get slots and save as tuple
        shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]

        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM inventory WHERE color=? AND size=?", shoe)
        
        # retrieve sqlite row
        data_row = cursor.fetchone()

        if data_row:
            # provide in stock message
            dispatcher.utter_message(template="utter_in_stock")
            connection.close()
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide out of stock
            dispatcher.utter_message(template="utter_no_stock")
            connection.close()
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

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
        return [SlotSet("survey_complete", True)]


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
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)
        if tracker.get_slot("email") == None:
            dispatcher.utter_message(text="Войдите в аккаунт, чтобы проверить заказы.")
            return []
        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE email=? AND status!='in cart'", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # convert tuple to list
            data_list = list(data_row)

            # respond with order status
            dispatcher.utter_message(template="utter_order_status", status=data_list[5])
            connection.close()
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
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
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("cancelled"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm cancellation
            dispatcher.utter_message(template="utter_order_cancel_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
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
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get email slot
        order_email = (tracker.get_slot("email"),)

        # retrieve row based on email
        cursor.execute("SELECT * FROM orders WHERE order_email=?", order_email)
        data_row = cursor.fetchone()

        if data_row:
            # change status of entry
            status = [("returning"), (tracker.get_slot("email"))]
            cursor.execute("UPDATE orders SET status=? WHERE order_email=?", status)
            connection.commit()
            connection.close()

            # confirm return
            dispatcher.utter_message(template="utter_return_finish")
            return []
        else:
            # db didn't have an entry with this email
            dispatcher.utter_message(template="utter_no_order")
            connection.close()
            return []

class GiveName(Action):
    def name(self) -> Text:
        return "action_give_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        evt = BotUttered(
            text = "my name is bot? idk", 
            metadata = {
                "nameGiven": "bot"
            }
        )

        return [evt]

class ReserveShoe(Action):
        def name(self) ->  Text:
            return "action_reserve_shoe"

        def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict[Text, Any]]:
            try:
                connection = sqlite3.connect(path_to_db)
                cursor = connection.cursor()
                shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]
                cursor.execute("SELECT * FROM inventory WHERE color=? AND size=? AND count <> 0", shoe)
                data_row = cursor.fetchone()
                if data_row:
                    #cursor.execute("SELECT email FROM users WHERE status == 1")
                    #email = cursor.fetchone()[0]
                    email = tracker.get_slot("email")
                    if email:
                        cursor.execute("INSERT into orders (order_date, email, color, size, status) values (?,?,?,?,?)", 
                                        (str(datetime.now().date()), email, data_row[1], data_row[0], "reserved"))
                        cursor.execute("UPDATE inventory SET count=count-1 WHERE color=? AND size=?", (data_row[1], data_row[0]))
                        connection.commit()
                        connection.close()
                        dispatcher.utter_message(template="utter_reservation_create_finish")
                        slots_to_reset = ["size", "color"]
                        return [SlotSet(slot, None) for slot in slots_to_reset]

                else:
                    # provide out of stock
                    dispatcher.utter_message(template="utter_no_stock")
                    connection.close()
                    slots_to_reset = ["size", "color"]
                    return [SlotSet(slot, None) for slot in slots_to_reset]
            except Exception as e:
                dispatcher.utter_message(template="utter_reservation_create_error")
                slots_to_reset = ["size", "color"]
                return [SlotSet(slot, None) for slot in slots_to_reset]

class AddToCart(Action):
    def name(self) -> Text:
        return "action_add_to_cart"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        order_date = datetime.now().strftime('%Y-%m-%d')
        color = str(tracker.get_slot("color"))
        size = float(tracker.get_slot("size"))
        status = "in_cart"
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()
        shoe = [(color), (size)]
        cursor.execute(
            "SELECT * FROM inventory WHERE color=? AND size=? AND count <> 0", shoe)
        data_row = cursor.fetchone()
        if data_row:
            #cursor.execute("SELECT email FROM users WHERE status == 1")
            #email = cursor.fetchone()[0]
            email = tracker.get_slot("email")
            if email:
                cursor.execute('INSERT INTO orders("order_date", "email", "color", "size", "status") VALUES (?,?,?,?,?)', (order_date, email, data_row[1], data_row[0], "in_cart"))
                connection.commit()
                connection.close()
                slots_to_reset = ["size", "color"]
                dispatcher.utter_message(template="utter_order_in_cart")
                return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            dispatcher.utter_message(template="utter_not_in_cart")
            connection.close()
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]

class Registration(Action):
    def name(self) -> Text:
        return "action_registration"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get slots and save as tuple
        reg_params = [(tracker.get_slot("email")), (tracker.get_slot("password"))]

        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM users WHERE email=?", [reg_params[0]])

        # retrieve sqlite row
        data_row = cursor.fetchone()

        if data_row:
            dispatcher.utter_message(text="Пользователь с таким email уже существует.")
            connection.close()
            #return [SlotSet("survey_complete", True)]
        else:
            # provide in stock message
            cursor.execute("INSERT INTO users (email, password, status) VALUES (?, ?, 0);", reg_params)
            connection.commit()
            dispatcher.utter_message(text="Вы успешно зарегистрированы!")
            connection.close()
        slots_to_reset = ["email", "password"]
        return [SlotSet(slot, None) for slot in slots_to_reset]

class SignIn(Action):
    def name(self) -> Text:
        return "action_sign_in"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # connect to DB
        connection = sqlite3.connect(path_to_db)
        cursor = connection.cursor()

        # get slots and save as tuple
        sign_in_params = [(tracker.get_slot("email")), (tracker.get_slot("password"))]

        # place cursor on correct row based on search criteria
        cursor.execute("SELECT * FROM users WHERE email=?", [sign_in_params[0]])

        # retrieve sqlite row
        data_row = cursor.fetchone()

        if not data_row:
            dispatcher.utter_message(text="Пользователя с таким email не существует:(")
            connection.close()
            slots_to_reset = ["email", "password"]
            return [SlotSet(slot, None) for slot in slots_to_reset]
        else:
            # provide in stock message
            cursor.execute("SELECT * FROM users WHERE email=? AND password=?", sign_in_params)

            data_row = cursor.fetchone()
            if data_row:
                connection.close()
                dispatcher.utter_message(text="Вы успешно вошли!")
                return []
            else:
                connection.close()
                dispatcher.utter_message(text="Неправильный email или пароль!")
                slots_to_reset = ["email", "password"]
                return [SlotSet(slot, None) for slot in slots_to_reset]