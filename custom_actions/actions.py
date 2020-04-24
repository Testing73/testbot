from core.Tracker import Action, FormAction

from api.weather import weather


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import wolframalpha
from forex_python.converter import CurrencyRates
from word2number import w2n
import re
import inflect
import json
import random


class SendReportAction(Action):
    def name(self):
        return "report_sharing"

    def run(self, tracker):
        det = ['livewitharun.12@gmail.com', 'Rainaprakash.12']
        email_user = det[0]
        email_password = det[1]
        if len(tracker.dummy_tracker['latest_message']['entities']) == 0:
            print("Sorry, I can't find any recipients to send :(")
        else:
            for each_entity in range(len(tracker.dummy_tracker['latest_message']['entities'])):
                if 'recepients' in list(tracker.dummy_tracker['latest_message']['entities'][each_entity].keys()):
                    recipients = tracker.dummy_tracker['latest_message']['entities'][each_entity]['recepients']
            # print(recipients, '%^&*()')
            senders = ','.join(recipients)
            print("Sending mail to "+senders)
            email_send = senders
            subject = 'Report'
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            # msg['CC'] = cc
            msg['Subject'] = subject
            body = 'Hi team, checkout this report'
            msg.attach(MIMEText(body, 'plain'))
            filename = '/home/pooja/Desktop/svm_original_data.png'
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, email_send, text)
            server.quit()
            print("Successfully Sent:)")


class UtterGreet(Action):
    def name(self):
        return "utter_greet"

    def run(self, tracker):
        return "Hey! How are you?"


class MoodHappyResponse(Action):
    def name(self):
        return "utter_mood_happy"

    def run(self, tracker):
        return "Great, carry on!"


class UtterGoodbye(Action):
    def name(self):
        return "utter_goodbye"

    def run(self, tracker):
        return "Bye."


class ActionJokesResponse(Action):
    def name(self):
        return "action_jokes_response"

    def run(self, tracker):
        with open("/home/pooja/Desktop/ChatBot/Open_domain/apis/jokes.json", "r") as f:
            CACHE = tuple(json.loads(f.read()).values())
            joke = random.choice(CACHE)
            # print(joke)
            return joke


class UtterBotChallenge(Action):
    def name(self):
        return "utter_bot_response"

    def run(self, tracker):
        return "I am a AI bot called as Scira, created by Teknuance Team."


class UtterVoiceResponse(Action):
    def name(self):
        return "utter_voice_response"

    def run(self, tracker):
        return "I am a female, I have got only one voice for now."


class UtterGenderResponse(Action):
    def name(self):
        return "utter_gender_response"

    def run(self, tracker):
        return "I am an AI bot."


class UtterCreatedResponse(Action):
    def name(self):
        return "utter_created_response"

    def run(self, tracker):
        return "I am created by Teknuance Team."


class UtterBirthdayResponse(Action):
    def name(self):
        return "utter_birthday_response"

    def run(self, tracker):
        return "Scira celebrates it birthday on September 23rd, I think it’s a good day to celebrate."


class UtterThankResponse(Action):
    def name(self):
        return "utter_thank_response"

    def run(self, tracker):
        return "My Pleasure."


class DidNotUnderstandResponse(Action):
    def name(self):
        return "utter_did_not_understand_response"

    def run(self, tracker):
        return "Sorry, I didn't understand you."


class ActionWeatherResponse(Action):
    def name(self):
        return "action_weather_res"

    def run(self, tracker):
        # print(tracker.dummy_tracker)
        loc_entity = None
        date_entity = None
        intent = tracker.dummy_tracker["latest_message"]["intent"]
        for each_entity in range(len(tracker.dummy_tracker['latest_message']['entities'])):
            if 'location' in list(tracker.dummy_tracker['latest_message']['entities'][each_entity].keys()):
                loc_entity = tracker.dummy_tracker['latest_message']['entities'][each_entity]['location'][0]
            if 'day_time' in list(tracker.dummy_tracker['latest_message']['entities'][each_entity].keys()):
                print(tracker.dummy_tracker['latest_message']['entities'][each_entity]['day_time'][0])
                date_entity = tracker.dummy_tracker['latest_message']['entities'][each_entity]['day_time'][0]
        # print(intent)
        print(loc_entity, date_entity, "Entity From question")
        if intent == 'weather':
            # print('yes')
            if loc_entity is not None:
                # print('yes2')
                if date_entity is not None:
                    date_entity = date_entity.rstrip(" ").lstrip(" ")
                    res = weather(loc_entity, date_entity)
                else:
                    res = weather(loc_entity, "today")
                # dispatcher.utter_message("The weather at " + name_entity + " is " + res)
                # print(res)
                return res
            else:
                if date_entity is not None:
                    date_entity = date_entity.rstrip(" ").lstrip(" ")
                    res = weather("chennai", date_entity)
                else:
                    res = weather("chennai", "today")
                # dispatcher.utter_message
                print("Showing for Chennai")
                # dispatcher.utter_message("The weather at " + name_entity + " is " + res)
                # dispatcher.utter_custom_json(res)
                # print(res)
                return res


# class ActionWeatherRes(Action):
#     def name(self):
#         return "action_weather_res"
#
#     def run(self, tracker):
#         print(tracker.dummy_tracker, '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
#         # intent = tracker.dummy_tracker["latest_message"]["intent"]
#         # loc_entity = next(tracker.get_latest_entity_values("location"), None)
#         # date_entity = next(tracker.get_latest_entity_values("day_time"), None)
#         # print(intent)
#         # print(loc_entity, date_entity, "Entity From question")
#
#         if intent == 'weather':
#             print('yes')
#             if loc_entity is not None:
#                 print('yes2')
#                 if date_entity is not None:
#                     date_entity = date_entity.rstrip(" ").lstrip(" ")
#                     res = weather(loc_entity, date_entity)
#                 else:
#                     res = weather(loc_entity, "today")
#                 # dispatcher.utter_message("The weather at " + name_entity + " is " + res)
#                 return res
#             else:
#                 if date_entity is not None:
#                     date_entity = date_entity.rstrip(" ").lstrip(" ")
#                     res = weather("chennai", date_entity)
#                 else:
#                     res = weather("chennai", "today")
#                 # dispatcher.utter_message
#                 print("Showing for Chennai")
#                 # dispatcher.utter_message("The weather at " + name_entity + " is " + res)
#                 # dispatcher.utter_custom_json(res)
#                 # print(res)
#                 return res


class ActionWikiQuestions(Action):
    def name(self):
        return "action_wiki_questions"

    def run(self, tracker):
        response = ''
        if tracker.dummy_tracker["latest_message"]["intent"] in ['wiki_what', 'wiki_when', 'wiki_which', 'wiki_who']:
            client = wolframalpha.Client("HP33YL-PXT5VKUTAP")
            print(tracker.dummy_tracker["latest_message"]["text"])
            res = client.query(tracker.dummy_tracker["latest_message"]["text"])
            print(res)
            if int(res["@numpods"]) > 2:
                flag = 0
                for i in range(1, int(res["@numpods"])):
                    if res["pod"][i]["@title"] == 'Wikipedia summary':
                        flag = 1
                        print(res["pod"][i]["subpod"]["plaintext"])
                        response = res["pod"][i]["subpod"]["plaintext"]
                if flag == 0:
                    try:
                        if res["pod"][1]["@primary"] == "true":
                            print(res["pod"][1]["subpod"]['plaintext'], 'here')
                            response = res["pod"][1]["subpod"]['plaintext']
                        else:
                            print("No results!")
                            response = "No results!"
                    except(KeyError):
                        response = res["pod"][1]["subpod"]['plaintext']
            else:
                print("No results!")
                response = "No results!"
        return response


class ActionMathQuestions(Action):
    def name(self):
        return "action_math_questions"

    def run(self, tracker):
        response = ''
        if tracker.dummy_tracker["latest_message"]["intent"] in ['math']:
            client = wolframalpha.Client("HP33YL-PXT5VKUTAP")
            print(tracker.dummy_tracker["latest_message"]["text"])
            res = client.query(tracker.dummy_tracker["latest_message"]["text"])
            if int(res["@numpods"]) > 2:
                print(res)
                if res["pod"][1]["@title"] == "Result":
                    if res["pod"][1]["@primary"] == "true":
                        response = res["pod"][1]["subpod"]["plaintext"]
                    else:
                        response = "Sorry, I don't get it :("
                else:
                    response = res["pod"][1]
            else:
                response = "Sorry, I don't get you"
        return response


def find_amount(query):
    amount_re = "\d+?((\.|\,)\d*)?(\s+k\s+?(million|billion|hundred|thousand)|\s+k?(million|billion|hundred|thousand)|k\s+?(million|thousand|hundred|billion)|k?(million|billion|hundred|thousand)|\s+?(million|billion|hundred|thousand))|\d+?((\.|\,)\d*)?(\s+k|k|\s+)"
    amount_in_words = "(?:sixty|seventy|eighty|ninety|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|hundred|thousand|million|billion|trillion|and)"
    temp_amount = ''
    if re.search(amount_re, query, re.IGNORECASE) is None:
        if re.findall(amount_in_words, query, re.IGNORECASE) is not None:
            temp_amount = " ".join(re.findall(amount_in_words, query, re.IGNORECASE))
        else:
            temp_amount = 1.0
    else:
        temp_amount = re.search(amount_re, query, re.I).group(0)
    print(temp_amount)
    return temp_amount


class ActionCurrencyConverter(Action):
    def name(self):
        return "action_currency_converter"

    def run(self, tracker):
        currency_list_dict = {
"INR": ["INR", "inr", "indian rupees", "indian currency", "indian rupee", "rupee", "rupees"],
"EUR": ["EUR", "euro", "Euro", "germany currency", "eur", "france currency", "Belgium currency", "Italy curreny", "spain currency"],
"USD": ["USD", "dollars", "usd", "United states dollar", "US dollar", "United States of America dollar", "United states of America currency",  "US currency", "United States currency"],
"YEN": ["Yen", "Japan yen", "Japanese yen", "YEN", "JPY", "jpy yen", "japan currency", "japanese currency"],
"Pound":["POUND", "pound sterling", "gbp", "GBP", "UK pound", "united kingdom pound", "UK currency", "United kingdom currency", "UK pound sterling", "United Kingdom pound sterling", "gbp sterling"],
"NZD":  ["NZD", "Newzland dollar", "nzd", "new zealand dollar", "new zealand currency", "newzealand currency", "nz dollar", "nz currency", "NZD"],
"AUD":  ["AUD", "Australian dollar", "AU dollar", "au dollar", "aud", "australia dollar", "australia currency", "australian currency", "AUD"],
"PKR":  ["PKR", "pakistan rupee", "pakistani rupee", "pak rupee", "pkr", "pakistani currency","pakistan currency", "pak currency", "PKD"],
"Yuan": ["Yuan", "Chinese yuan", "yuan renminbi", "renminbi", "china renminbi", "chinese yuan renminbi", "china yuan", "chinese currency", "china currency", "cny",  "CNY", "yuan", "cn yuan", "YUAN"],
}
        temp = ''; response = ''; flag = 0
        from_currency = None;to_currency = None
        p = inflect.engine()
        c = CurrencyRates(force_decimal=False)
        for each_entity in range(len(tracker.dummy_tracker['latest_message']['entities'])):
            if 'from_curr' in list(tracker.dummy_tracker['latest_message']['entities'][each_entity].keys()):
                from_currency = tracker.dummy_tracker['latest_message']['entities'][each_entity]['from_curr'][0]
            if 'to_curr' in list(tracker.dummy_tracker['latest_message']['entities'][each_entity].keys()):
                print(tracker.dummy_tracker['latest_message']['entities'][each_entity]['to_curr'][0])
                to_currency = tracker.dummy_tracker['latest_message']['entities'][each_entity]['to_curr'][0]
        # from_currency = tracker.dummy_tracker['latest_message']['entities']
        # to_currency = tracker.dummy_tracker['latest_message']['entities']
        for keys in list(currency_list_dict.keys()):
            if from_currency is None or to_currency is None:
                flag = 1

            if from_currency in currency_list_dict[keys]:
                from_currency = keys
            elif to_currency in currency_list_dict[keys]:
                to_currency = keys

        if flag == 1 and tracker.dummy_tracker["latest_message"]["intent"] != 'check_currency_value':
            response = "Couldn't find the currency codes"
        else:
            if tracker.dummy_tracker["latest_message"]["intent"] == 'currency_converter_with_amount':
                print(from_currency, to_currency, 'here')
                print(tracker.dummy_tracker["latest_message"]["text"])
                amount = find_amount(tracker.dummy_tracker["latest_message"]["text"])
                print(amount, 'Amount')
                if amount is not None and amount != " " and amount != "":
                    print(amount, 0)
                    amount = amount.lower().rstrip(' ').split(' ')
                    print(amount, 'After Split')
                    if len(amount) == 1:
                        if 'k' in amount[0]:
                            amount = int(amount[0].rstrip("k"))
                            amount = amount * 1000
                            print(amount, 1)
                        else:
                            amount = amount[0]
                            print(amount, 'Simple Integer')
                        print(type(amount), 10)
                    else:
                        for i in range(len(amount)):
                            amount[i] = amount[i].lower()
                            if re.match("\d.*k", amount[i], re.IGNORECASE):
                                amount[i] = amount[i].replace("k", "")
                                amount[i] = (int(amount[i])) * 1000
                                amount[i] = p.number_to_words(amount[i])
                            elif re.match("\d.*", amount[i], re.IGNORECASE):
                                if amount[i + 1] == 'k':
                                    amount[i] = (int(amount[i])) * 1000
                                    amount[i] = p.number_to_words(amount[i])
                                else:
                                    amount[i] = p.number_to_words(amount[i])
                            temp = temp + ' ' + amount[i]
                        amount = temp
                    print(amount, "here")
                    try:
                        amount = w2n.word_to_num(amount)
                        print(amount)
                        amount = float(amount)

                    except ValueError:
                        amount = float(amount)
                if amount is None or amount == "" or amount == " ":
                    amount = 1.0
                try:
                    converted_value = c.get_rate(from_currency, to_currency)

                    response = str(amount) + ' in  ' + from_currency + ' = ' + str(converted_value * amount) + ' ' + to_currency
                except TypeError:
                    if from_currency is None:
                        response = "Sorry, Couldn't get the from currency code."
                    elif to_currency is None:
                        response = "Sorry, Couldn't get the to currency code."
            elif tracker.dummy_tracker["latest_message"]["intent"] == 'currency_value':
                converted_value = c.get_rate(from_currency, to_currency)
                response = from_currency + ' rate is ' + str(converted_value) + ' ' + to_currency

            elif tracker.dummy_tracker["latest_message"]["intent"] == 'check_currency_value':
                print("YAY!!!!")
                if to_currency is not None and from_currency is None:
                    print(to_currency, "###############################")
                    converted_value = c.get_rate(to_currency, 'USD')
                    response = from_currency + ' rate is ' + str(converted_value) + ' USD'
                elif to_currency is None and from_currency is not None:
                    print(from_currency, "###############################")
                    converted_value = c.get_rate(from_currency, 'USD')
                    response = from_currency + ' rate is ' + str(converted_value) + ' USD'
                elif from_currency is None and to_currency is None:
                    response = "Sorry, I couldn't server you with this :("

        return response


class CreateEventResponse(FormAction):
    def name(self):
        return "create_event_response"

    def required_slots(self):
        return ["day_time", 'title', 'time']

    def submit(self, tracker):
        print("Working fine for a single form action")
        print(tracker.dummy_tracker['latest_message']["entities"], "##########################################")
        return "slot filling happened successfully"


class dummy1FormAction(FormAction):
    def name(self):
        return "create_project_event"

    def required_slots(self):
        return ["gpe"]

    def submit(self, tracker):
        print("Working fine for a single form action")
        print(tracker.dummy_tracker['latest_message']["entities"])
        return "slot filling happened successfully"


class dummy2FormAction(FormAction):
    def name(self):
        return "create_dummy_event"

    def required_slots(self):
        return ["gpe"]

    def submit(self, tracker):
        print("Working fine for a single form action")
        print(tracker.dummy_tracker['latest_message']["entities"])
        return "slot filling happened successfully"


