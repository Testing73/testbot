def intent_name(tracker, reference):
    intent = tracker.dummy_tracker['latest_message']['intent']
    if intent not in list(reference.keys()):
        action_name = "utter_did_not_understand_response"
    else:
        action_name = [reference[ref] for ref in reference if intent == ref][0]
    return action_name

