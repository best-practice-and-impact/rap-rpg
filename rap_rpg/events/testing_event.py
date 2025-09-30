from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message

class Testing(Event):
    def __init__(self):
        self.event_text = """The team are thinking about implementing some new tests in their code.\n
Kim says it will take too long, but Georgia thinks it will be worth it for helping to assure their work. What should they do?"""
        self.options = ["Don't bother with more testing - the code will change anyway",
                        "Add some additional tests - what harm could it do?"]
        super().__init__(self.event_text, self.options)
        
        self._prompt_choice()
        self._handle_choice()
    
    def _handle_choice(self):
        if self.choice == 0:
            print_long_message("""\
                               The team decide not to add more tests due to the time it would take. Everything's
                               been working fine until now, anyway.
                               """)
            self.game_state_modifier = {"more_tests": False, "process_quality": -1}

        elif self.choice == 1:
            print("The team decide to add some more tests. Let's roll to find out how it goes: ")
            self._roll_the_dice()

            if self.dice_res <= 2:
                print_long_message("""\
                                    The team add loads and loads of tests. It gets quite confusing - they use two
                                    frameworks which work slightly differently. They test for several operations that
                                    don't really reflect real-world useage, or could have been handled more efficiently with error
                                    handling. While there are some good tests in there, most of them don't do much in terms of
                                    assuring that their processes work as intended - it probably goes as far as offering a false
                                    level of assurance. It took ages too...
                                   """)
                self.game_state_modifier = {"more_tests": True, "late_risk": 1, "team_motivation": -1}
             
            elif self.dice_res <= 4:
                print_long_message("""\
                                   The team add some tests. They don't cover absolutely everything the team would like,
                                   but what they have been able to do has adds some assurance.
                                   """)
                self.game_state_modifier = {"more_tests": True, "process_quality": 1}
            
            else:
                print_long_message("""\
                                   The team agree on one of the standard frameworks, Pytest, for adding more unit tests. They
                                   identify some of the most important functions and edge cases to test for first, and start with
                                   those. Some tests are written to check that errors are raised under the right conditions and the
                                   team find that in a couple of places this isn't happening correctly, so they update the code.
                                   Then they move onto some 'nice-to-haves', which for them were some integration tests. Kim's really
                                   glad Georgia challenged her view on this, because it was worth it in the end.
                                   """)
                self.game_state_modifier = {"more_tests": True, "process_quality": 1, "team_motivation": 1}
        
        self._print_game_mod_outcome()
        return None