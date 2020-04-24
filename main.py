from core.ActionCollection import ListofActions
from core.Tracker import Tracker
from nlu.intent_classification import *
from nlu.named_entity import *
from dialog_manager.response_fetcher import *
from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home_view():
    return "<h2>Chatbot Prototype</h2>"


@app.route("/chatbot", methods=['GET', 'POST'])
def main():
    reference = {'share_report': 'report_sharing', 'greet': 'utter_greet', 'goodbye': 'utter_goodbye',
                 'mood_great': 'utter_mood_happy', 'mood_unhappy': 'action_jokes_response',
                 'bored': 'action_jokes_response', 'joke': 'action_jokes_response',
                 'bot_challenge': 'utter_bot_response', 'birthday': 'utter_birthday_response',
                 'voice': 'utter_voice_response', 'created': 'utter_created_response',
                 'gender': 'utter_gender_response', 'thank': 'utter_thank_response', 'weather': 'action_weather_res',
                 'create_event': 'create_event_response', 'wiki_what': 'action_wiki_questions',
                 'wiki_when': 'action_wiki_questions', 'currency_converter_with_amount': 'action_currency_converter',
                 'wiki_who': 'action_wiki_questions', 'wiki_which': 'action_wiki_questions',
                 'currency_value': 'action_currency_converter', 'check_currency_value': 'action_currency_converter',
                 'math': 'action_math_questions'}
    executor = ListofActions()
    list_of_actions = executor.get_the_subclasses()
    # print(list_of_actions, 'list of actions')
    tracker = Tracker()
    # print(tracker)
    tracker.dummy_tracker['user_id'] = 'usr1'
    # udf = simple_uv(dff)
    # udf_column = simple_uv(cdf)
    response = {"intent": "", "entity": [], "query": "", "response": ""}
    # while True:
    req = request.get_json(force=True)
    user_input = req['question']
    response["query"] = user_input
    print(user_input)
    # user_input = input("Hey : ")
    if user_input == 'stop':
        print("Thank you. Process terminated Successfully!!")
        response["response"] = "Thank you. Process terminated Successfully!!"
    else:
        intent, intent_dict_with_confidence = test_input(user_input)
        # print(intent)
        entities = entity_extraction_rules(intent, user_input)
        # print(entities)
        tracker.dummy_tracker['latest_message']['intent'] = intent
        tracker.dummy_tracker['latest_message']['entities'] = entities
        tracker.dummy_tracker['latest_message']['text'] = user_input

        # print(tracker.dummy_tracker, reference)
        # print(re)
        tracker.dummy_tracker['latest_action_name'] = intent_name(tracker, reference)
        action_to_be_called = tracker.dummy_tracker['latest_action_name']
        # print(action_to_be_called, '##############################################################')
        for k, v in list_of_actions.items():
            if action_to_be_called == k:
                # print(k)
                response["response"] = v(tracker)
                # return v(tracker)
        response["intent"] = intent
        response["entity"] = entities
    return response


# if __name__ == '__main__':
#     main()
# app.run(debug=True, port=5000)
if __name__ == "__main__":
    app.run(debug=True)
