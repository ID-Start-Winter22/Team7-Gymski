# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from datetime import datetime
import random
from sys import displayhook
from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import json


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

# class ActionGetWorkoutScheduleForSpecificDay(Action):

#      def name(self) -> Text:
#          return "action_get_workout_schedule_for_day"

#      def run(self, dispatcher, tracker, domain):
#         day = tracker.get_slot("day")
#         if not day :
#             attachment_monday = { "type":"video", "payload":{ "title": "Fun Full Body", "src": "https://www.youtube.com/embed/2-RGYM6ojJ4" } }
#             dispatcher.utter_message(text="Workout Freitag", attachment=attachment_monday)
#         elif ():
#             dispatcher.utter_message(" Beim Holen des Workoutplans ist ein Fehler aufgetreten.")
            
class ActionGetWorkoutScheduleForSpecificDay(Action):

    def name(self) -> Text:
          return "action_get_workout_schedule_for_day"
      
    def run(self, dispatcher, tracker, domain):
        dt = datetime.now()
        x = dt.weekday()
        if x == 0:
            text = f"Ich werde dir die Übungen für Montag geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_montag")
        elif x == 1:
            text = f"Ich werde dir die Übungen für Dienstag geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_dienstag")
        elif x == 2:
            text = f"Ich werde dir die Übungen für Mittwoch geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_mittwoch")
        elif x == 3:
            text = f"Ich werde dir die Übungen für Donnerstag geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_donnerstag")
        elif x == 4:
            text = f"Ich werde dir die Übungen für Freitag geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_freitag")
        elif x == 5:
            text = f"Ich werde dir die Übungen für Samstag geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_samstag")
        elif x == 6:
            text = f"Ich werde dir die Übungen für Sonntag geben!"
            dispatcher.utter_message(text)
            dispatcher.utter_message(response = "utter_get_workout_schedule_sonntag")
        



# class ActionChestWorkout(Action):

#     def name(self) -> Text:
#         return "action_get_chest_exercise"

#     def run(self, dispatcher, tracker,domain):
#         message = tracker.latest_message.get("Hier ist eine Brustübung für dich:")
#         keyword = "Brust", "Chest"
#         if keyword in message:
#             dispatcher.utter_template("utter_chest_exercise")

class ActionCalculateCalories(Action):
    def name(self) -> Text:
        return "action_calculate_calories"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        def user_info():
            age = tracker.get_slot("age")
            gender = tracker.get_slot("gender")
            weight = tracker.get_slot("weight")
            height = tracker.get_slot("height")
            activity_level = tracker.get_slot("activity")
            goals = tracker.get_slot("goal")
            
            bmr = 0

            if gender == "Mann":
                bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5
                
                if activity_level == '0':
                    bmr = bmr * 1.2 
                elif activity_level == '1-2':
                    bmr = 1.375 * bmr
                elif activity_level == '3-4':
                    bmr = 1.55 * bmr
                elif activity_level == '5-6':
                    bmr = 1.725 * bmr
                elif activity_level == '7>':
                    bmr = 1.9 * bmr
                       
            elif gender == "Frau":
                bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) - 161

                if activity_level == '0':
                    bmr = bmr * 1.2 
                elif activity_level == '1-2':
                    bmr = 1.375 * bmr
                elif activity_level == '3-4':
                    bmr = 1.55 * bmr
                elif activity_level == '5-6':
                    bmr = 1.725 * bmr
                elif activity_level == '7>':
                    bmr = 1.9 * bmr

            return(float(bmr))

        def gain_or_lose(bmr):
            goals = tracker.get_slot("goal")

            if goals == 'abzunehmen':
                calories = bmr - 500
                text = f"Um {goals} musst du {calories} Kalorien am Tag zu dir nehmen!"
                dispatcher.utter_message(text)

            elif goals == 'halten':
                calories = bmr
                text = f"Um dein Gewicht zu halten musst du {calories} Kalorien am Tag zu dir nehmen!"
                dispatcher.utter_message(text)

            elif goals == 'zuzunehmen':
                    calories = bmr + 500
                    text = f"Um {goals} musst du {calories} Kalorien am Tag zu dir nehmen!"
                    dispatcher.utter_message(text)


        gain_or_lose(user_info())

        return [SlotSet("gender", None), SlotSet("weight", None), SlotSet("height", None), SlotSet("age", None), SlotSet("goal", None),SlotSet("activity", None)]