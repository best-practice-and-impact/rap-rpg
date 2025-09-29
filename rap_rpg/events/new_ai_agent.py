from rap_rpg.classes.event_abc import Event

use_ai = ("Use AI", "They choose to use the AI agent. ",
                   "Roll to see how it goes! ", 4,
"""The AI comes up with some code which seems fine, so they merge it into main.
It breaks another part of the pipeline. They spend longer debugging than it would have taken to write the new feature!""",
"""The AI comes up with some code which gets them on the right track straight away.
They interrogate the code and with some tweaks they implement the new feature successfully.
The AI even helps them write the documentation and unit tests, saving lots of time!""")

dont_use_ai = ("Reject AI", "They're not fussed about AI, and stick to doing it themselves. ",
                           "What happens next? Roll the dice! ", 4,
"""They spend 2 days on Stack Overflow before coming up with a convoluted way to implement the new feature that they won't be
able to understand in a few months' time.""",
"""It takes some time but they manage to implement the feature and are confident they know what the code is doing.
It's not perfect but they learnt a few things along the way that they can improve with the next iteration.""")


class NewAIAgent(Event):
    def __init__(self):
        self.event_text = "Coming up to the team's deadline, their workplace introduces a new AI agent. They need to implement a new feature to their pipeline, do they use AI to help?"
        self.options = ["Yes", "No"]
        self.outcomes = [use_ai, dont_use_ai]
        super().__init__(self.event_text, self.options, self.outcomes)
    
    def _handle_choice(self):
        choice = self.outcomes[self.user_choice-1]

        print(choice.choice_text, end = "")
        self.got = choice._handle_dicecheck()

        if ((self.user_choice == 1) and (self.got[0] == False)):
            self.game_state_modifier = {"late_risk": 1}
        elif ((self.user_choice == 1) and (self.got[0] == True)):
            self.game_state_modifier = {"process_quality": 1}
        elif (self.user_choice == 2 and self.got[0] == False):
            self.game_state_modifier = {"process_quality": -1}
            print(self.got[1])
        else:
            self.got = choice
            print(self.got)
        
        return None