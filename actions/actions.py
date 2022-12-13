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
class CalorieCalculator(Action):
    
    def name(self) -> Text:
        return "action_calorie_calculator"
    
    def run(self, dispatcher, tracker, domain):

        def user_info():
            weight = tracker.get_slot("user_weight") * 2.205
            height = tracker.get_slot("user_height") / 2.54
            age = tracker.get_slot("user_age")
            gender = tracker.get_slot("user_gender")
            

            if gender == 'männlich':
                c1 = 66
                hm = 6.2 * height
                wm = 12.7 * weight
                am = 6.76 * age
            elif gender == 'weiblich':
                c1 = 655.1
                hm = 4.35 * height
                wm = 4.7 * weight
                am = 4.7 * age

                #BMR = 665 + (9.6 X 69) + (1.8 x 178) – (4.7 x 27)
                bmr_result = c1 + hm + wm - am
                return(int(bmr_result))

        def calculate_activity(bmr_result): 
                

                if activity_level == 'wenig':
                    activity_level = 1.2 * bmr_result
                elif activity_level == 'moderat':
                    activity_level = 1.55 * bmr_result
                elif activity_level == 'viel':
                    activity_level = 1.725 * bmr_result

                return(int(activity_level))

        def gain_or_lose(activity_level):
                goals = tracker.get_slot("user_goal")
                activity_level = tracker.get_slot("user_activity")

                if goals == 'abnehmen':
                    calories = activity_level - 500
                elif goals == 'halten':
                    calories = activity_level
                elif goals == 'zunehmen':
                    calories = activity_level + 500

                dispatcher.utter_message("Um {} musst du am Tag {} essen!".format(goals, calories))

        gain_or_lose(calculate_activity(user_info()))
        
        return []