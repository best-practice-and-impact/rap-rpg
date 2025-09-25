from rap_rpg.classes.event_abc import Event
from rap_rpg.classes.dice_check import DiceCheck

no_code_review = "There's no code review, and it turns out there was a bug in Brian's code. Oops..."

code_review = DiceCheck("code_review", "Lena takes a look at Brian's code.",
                   "Let's roll to see how it went! ", 2,
"""Lena didn't feel psychologically safe enough to raise an issue with Brian's code.
It was a bit hard to understand, and maybe one or two extra tests would have been good... But it's probably
fine, right?""",
"""Lena spotted a bug in Brian's code, and let him know about it as well as complimenting how he'd
followed the principle of loose-coupling. It made things really easy to follow, having all the concerns
seperated out""")

class Review(Event):
    def __init__(self):
        self.event_text = "After adding a new feature to the team code, what does Brian do?"
        self.options = ["He merges into main right away. It's busy, afterall!",
                        "He requests a code review - Lena said she'd be happy to take a look."]
        self.outcomes = [no_code_review, code_review]
        self.got = None
        super().__init__(self.event_text, self.options, self.outcomes)
    
    def _handle_choice(self):
        choice = self.outcomes[self.user_choice-1]
        if isinstance(choice, DiceCheck):
            print(choice.choice_text, end = "")
            self.got = choice._handle_dicecheck()

            if (self.user_choice == 2 and self.got[0] == False):
                self.game_state_modifier = {"process_quality": -1}
            elif (self.user_choice == 2 and self.got[0] == False):
                self.game_state_modifier = {"team_motivation": 1}

            print(self.got[1])

        else:
            self.got = choice
            if self.user_choice == 1:
                self.game_state_modifier = {"process_quality": -1}
            print(self.got)
        
        return None