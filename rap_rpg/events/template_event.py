from rap_rpg.classes.event_abc import Event
from rap_rpg.classes.dice_check import DiceCheck

option1 = DiceCheck("name_of_decision", "what happens from this decision",
                   "roll to do xyz... ", #option1_threshold_for_better_outcome,
"""bad_outcome""",
"""better_outcome""")

option2 = DiceCheck("name_of_decision", "what happens from this decision",
                   "roll to do xyz... ", #option2_threshold_for_better_outcome,
"""bad_outcome""",
"""better_outcome""")

# Or, options can just be strings.

class NameOfEvent(Event):
    def __init__(self):
        self.event_text = "Coming up to the team's deadline, their workplace introduces a new AI agent. They need to implement a new feature to their pipeline, do they use AI to help?"
        self.options = ["option 1", "option 2"]
        self.outcomes = [option1, option2]
        self.got = None
        super().__init__(self.event_text, self.options, self.outcomes)
    
    def _handle_choice(self):
        choice = self.outcomes[self.user_choice-1]
        if isinstance(choice, DiceCheck):
            print(choice.choice_text, end = "")
            self.got = choice._handle_dicecheck()

            # use self.game_state_modifier to increment "process_quality", "late_risk", or add/update other statuses.
            if ((self.user_choice == 1) and (self.got[0] == False)): # Option 1, fail roll
                self.game_state_modifier = {"late_risk": 1}
            elif ((self.user_choice == 1) and (self.got[0] == True)): # Option 1, pass roll
                self.game_state_modifier = {"process_quality": 1}
            elif (self.user_choice == 2 and self.got[0] == False): # Option 2, fail roll
                self.game_state_modifier = {"other_status": True}
            elif (self.user_choice == 2 and self.got[0] == False): # Option 2, pass roll
                
            print(self.got[1])

        else:
            self.got = choice
            print(self.got)
        
        return None