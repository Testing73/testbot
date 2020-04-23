from custom_actions.actions import *
from core.Tracker import *


class ListofActions:
    def __init__(self):
        self.list_of_actions = {}

    def get_the_subclasses(self):
        subclass_list = Action.__subclasses__()
        subclass_list.extend(FormAction.__subclasses__())
        print(subclass_list)
        for i in subclass_list:
            # print("yes")
            if issubclass(i, Action):
                # print('yesaction')
                self.list_of_actions[i().name()] = i().run
            if issubclass(i, FormAction):
                # print("yesformaction")
                self.list_of_actions[i().name()] = i().activate_form
        # to do validation based on domain file
        return self.list_of_actions


