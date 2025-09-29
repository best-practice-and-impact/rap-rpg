from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message

class NewAIAgent(Event):
    def __init__(self):
        self.event_text = """Coming up to the team's deadline, their workplace introduces a new AI agent.
Do they use the AI to help implement a new feature in the pipeline?"""
        self.options = ["Yes", "No"]
        super().__init__(self.event_text, self.options)

    def _handle_choice(self):
        if self.choice == 0:
            print("They choose to use the AI agent. Roll to see how it goes!\n")
            self._roll_the_dice()

            if (self.dice_res <= 2):
                print_long_message("""\
                                   The AI comes up with some code which seems fine, so they merge it into main.
                                   It breaks another part of the pipeline. They spend longer debugging than it would
                                   have taken to write the new feature!""")
                self.game_state_modifier = {"late_risk": 1}
            else:
                print_long_message("""\
                                   The AI comes up with some code which gets them on the right track straight away.
                                   They interrogate the code and with some tweaks they implement the new feature successfully.
                                   The AI even helps them write the documentation and unit tests, saving lots of time!""")
                self.game_state_modifier = {"process_quality": 1, "team_motivation": 1}

        elif self.choice == 1:
            print("They're not fussed about AI, and stick to doing it themselves. What happens next? Roll the dice!\n")
            self._roll_the_dice()

            if self.dice_res <= 4:
                print_long_message("""\
                                   They spend 2 days on Stack Overflow before coming up with a convoluted way to implement the
                                   new feature that they won't be able to understand in a few months' time.""")
                self.game_state_modifier = {"process_quality": -1}
            else:
                print_long_message("""\
                                   It takes some time but they manage to implement the feature and are confident they know what
                                   the code is doing. It's not perfect but they learnt a few things along the way that they can
                                   improve with the next iteration.""")
        
        self._print_game_mod_outcome()
        return None    