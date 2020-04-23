"""Class which maintains the entire state info for the agent to refer"""
from nlu.intent_classification import test_input
from nlu.named_entity import entity_extraction_rules


class Action:
    def name(self):
        raise NotImplementedError("Something will come here")

    def run(self, tracker):
        raise NotImplementedError("Something will come here")


class FormAction:
    def name(self):
        raise NotImplementedError("Something will come here")

    def activate_form(self, tracker):
        form_action_name = tracker.dummy_tracker['latest_action_name']
        print("{} is active".format(form_action_name))
        tracker.dummy_tracker['active_form'] = form_action_name
        slots_to_fill = self._check_for_required_slots(tracker)
        form_filled_entities = self.slot_filling(tracker, slots_to_fill)
        print(form_filled_entities, "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        tracker.dummy_tracker["latest_message"]["entities"] = form_filled_entities
        dispatcher = self.submit(tracker)
        return dispatcher

    def _check_for_required_slots(self, tracker):
        slots_to_fill = self.required_slots()
        # Checking the tracker for populated slots
        for each_entity in slots_to_fill:
            if each_entity in list(tracker.dummy_tracker['latest_message']['entities'][0].keys()):
                slots_to_fill.remove(each_entity)
        print("Slots to fill array", slots_to_fill)
        return slots_to_fill

    def required_slots(self):
        raise NotImplementedError("Something will come here")

    def slot_filling(self, tracker, slots_to_fill):
        form_filled_entities = [{}]
        # if tracker.dummy_tracker["latest_message"]["intent"] == "create_event":
        required_slots = slots_to_fill
        for iter in range(len(required_slots)):
            print(required_slots[0])
            print("Provide the value for {}".format(required_slots[0]))
            user_input_for_slot_filling = input()
            while len(required_slots) != 0:
                """
                using spacy identify the entities
                """
                # nlp = spacy.load("en")
                # doc = nlp(user_input_for_slot_filling)
                intent, intent_dict_with_confidence = test_input(user_input_for_slot_filling)
                if intent == 'stop_create_event':
                    break
                else:
                    entities = entity_extraction_rules(intent, user_input_for_slot_filling)
                    print(entities)

                    # print(doc.ents, "SPACY ENTITIES")
                    print('current slot',required_slots[0].lower())
                    print('entity filled list', list(entities[0].keys()))
                    if required_slots[0].lower() not in list(entities[0].keys()):
                    # if required_slots[0].upper() not in [doc_.label_ for doc_ in doc.ents]:
                        print("Sorry I don't get the value {}".format(required_slots[0]))
                        user_input_for_slot_filling = input()

                    else:
                        for each_ent in list(entities[0].keys()):
                        # for doc_ in doc.ents:
                            if each_ent.lower() in required_slots:
                                identified_entity = each_ent
                                identified_value = entities[0][each_ent]
                                form_filled_entities[0].__setitem__(identified_entity.lower(), identified_value)
                                required_slots.remove(identified_entity.lower())
                        break
        return form_filled_entities

    def submit(self, tracker):
        raise NotImplementedError("Something will come here")


class Tracker:
    def __init__(self):
        self.dummy_tracker = {
            "user_id": "",  # sender_id
            "slots": {},  # slots to be filled for this domain
            "latest_message": {"intent": "", "entities": [], "text": ''},
            # {"intent": current msg's intent, "entities": identified entities, "text": actual user query}
            "events": [],  # list of events so for
            "paused": "",
            "followup_action": "",
            "active_form": "",  # if any form action to be performed
            "latest_action_name": "",  # action to be performed
        }

    def get_latest_intent(self):
        latest_intent = self.dummy_tracker['latest_message']['intent']
        return latest_intent

    def get_latest_entity(self, entity_name):
        entities = self.dummy_tracker['latest_message'].get("entities", [])
        return (x.get("value") for x in entities if x.get("entity") == entity_name)

    def latest_action_name(self):
        return self.dummy_tracker['latest_action_name']
