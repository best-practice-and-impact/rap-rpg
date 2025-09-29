from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message

class Review(Event):
    def __init__(self):
        self.event_text = "After adding a new feature to the team code, what does Brian do?"
        self.options = ["He merges into main right away. It's busy, afterall!",
                        "He requests a code review - Lena said she'd be happy to take a look."]
        super().__init__(self.event_text, self.options)
        
        self._prompt_choice()
        self._handle_choice()
    
    def _handle_choice(self):
        if self.choice == 0:
            print("There's no code review, and it turns out there was a bug in Brian's code. Oops...")
            self.game_state_modifier = {"process_quality": -1}

        elif self.choice == 1:
            print("Lena takes a look at Brian's code. Let's roll to see how it went!")
            self._roll_the_dice()

            if self.dice_res <= 2:
                print_long_message("""\
                    Lena didn't feel psychologically safe enough to raise an issue with Brian's code.
                    It was a bit hard to understand, and maybe one or two extra tests would have been good...
                    But it's probably fine, right?
                """)

                self.game_state_modifier = {"team_motivation": -1}
            else:
                print_long_message("""\
                      Lena spotted a bug in Brian's code, and let him know about it. She complimented his use of
                      a the factory design pattern, which she'd recently learned about - it was helpful to see
                      it in action.
                """)

                self.game_state_modifier = {"process_quality": 1}
        
        self._print_game_mod_outcome()
        return None