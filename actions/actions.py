# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


# NOTE(Michael): We could use this action to store the name in
#                the TrackerStore (in memory database) or a persitent DB
#                such as MySQL. But we need to store a key-value pair 
#                to identify the user by id eg. (user_id, slotvalue)
class ActionStoreUserName(Action):

     def name(self) -> Text:
         return "action_store_name"
         
     def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot("username")
        print("Sender ID: ", tracker.sender_id)

        return []


class ActionUserName(Action):

     def name(self) -> Text:
         return "action_get_name"

     def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot("username")
        if not username :
            dispatcher.utter_message(" Du hast mir Deinen Namen nicht gesagt.")
        else:
            dispatcher.utter_message(' Du bist {}'.format(username))


class ActionGetWorkoutScheduleForSpecificDay(Action):

     def name(self) -> Text:
         return "action_get_workout_schedule_for_day"

     def run(self, dispatcher, tracker, domain):
        day = tracker.get_slot("day")
        if not day :
            dispatcher.utter_message(" Beim Holen des Workoutplans ist ein Fehler aufgetreten.")
        elif (day == "montag"):
            # attachment objekt geht irgendwie nicht
            attachment_monday = { "type":"video", "payload":{ "title": "Fun Full Body", "src": "https://www.youtube.com/embeded/=2-RGYM6ojJ4" } }
            dispatcher.utter_message(text="Workout Monday", attachment=attachment_monday)