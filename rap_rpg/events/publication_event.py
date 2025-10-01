from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message
from random import randint

class Publication(Event):
    def __init__(self, game_state):
        self.event_text = "After several weeks of work, it's almost time for publication day!\n"
        self.game_state = game_state
        super().__init__(self.event_text, options = None, game_state=self.game_state)
        
        self._handle_choice()
    
    def _handle_choice(self):
        if self.options is None:
            self._run_chance()
        else:
            raise ValueError(f"The options associated with this event should be None, or supply an implementation of _handle_choice.")
        return None
    
    def _run_chance(self):
        process_quality = self.game_state.get("process_quality", 0) # Total range from AI, Review, Scrum, Testing: -3 to 4
        team_motivation = self.game_state.get("team_motivation", 0) # Total range from AI, Review, Scrum, Testing: -3 to 3
        late_risk = self.game_state.get("late_risk", 0) # Total range from AI, Review, Scrum, Testing: 0 to 3
        more_tests = self.game_state.get("more_tests", False)
        late = False
        error = False

        if late_risk > 0:
            if late_risk == 1:
                late_or_not = randint(0, 1)
                if late_or_not == 0:
                    print("The publication is going to be on time. Phew!\n")
                else:
                    print("The analysis isn't going to be ready on time. ", end = "")
                    late = True
                        
                        
            else:
                print("The publication is running behind schedule. ", end = "")
                late = True
        
        if late is True:
            if team_motivation > 0:
                print("Let's roll to find out how late it will be.")
                self._roll_the_dice()
                if self.dice_res <=2:
                    print_long_message("""\
                                       The team were motivated, but it wasn't enough to mitigate the delay. It takes a while
                                       to finish the analysis.
                                       """)
                    print("\n", end = "")
                else:
                    print_long_message("""\
                                       The team are thankfully well-motivated, and get the analysis finished. The delay could have been
                                       a lot worse, and they've earned a good break when this is done.
                                       """)
                    print("\n", end = "")
            else:
                print("The team are understandably very demotivated, and it takes a while to finish the analysis.\n")

        if process_quality <= 0:
            print("When the publication goes out, there's an error. Oops - let's roll to find out how bad it is.")
            self._roll_the_dice()
            if self.dice_res <= 2:
                print_long_message("""\
                                   It's a major error. Ugh! There's disruption to the downstream stakeholders in other
                                   Government departments, as well as non-Government organisations too. There is
                                   real damage to the reputation of ONS as an organisation for quality statistics. It's
                                   time for a review of what happened, and where things need to improve.\n
                                   """)
                error = True
            else:
                print_long_message("""\
                                   It's a minor error that can be resolved fairly quickly. Still it's not ideal, and a larger
                                   error could have slipped through. The team will be sure to implement a fix for the issue, and
                                   have a review to work out what could be done differently next time.\n
                                   """)
                error = True

        else:
            print("Let's roll to see how publication goes!")
            self._roll_the_dice()
            if self.dice_res == 1:
                if more_tests is False:
                    print_long_message("""\
                                       An error slips through the net! It was something silly, too. a little more testing and QA
                                       could have lead to the error being detected. The damage has been done to external stakeholders,
                                       who really aren't happy about this.
                                       """)
                    error = True
                else:
                    print_long_message("""\
                                       The team detect a minor error last minute! Thanks to some robust testing, they can narrow
                                       down the cause. Phew! The team address the problem, and publication comes out great in the end.
                                       It's a good thing they spent the extra time doing those tests.
                                       """)
            elif self.dice_res <= 4:
                print_long_message("""\
                                   The team publish to the standard expected by their stakeholders. It's a win! The
                                   team are really happy to be done.
                                   """)
            else:
                print_long_message("""\
                                   The team publish to the standard expected by their stakeholders. They do a range of
                                   show-and-tells interally, showing the continuous improvements they've been able to do.
                                   It was a real team effort, and a great win.
                                   """)
        
        if team_motivation <= -2:
            if late or error:
                print_long_message("""After a difficult publication round, Ian's been feeling really demotivated and has
                                   decided to leave the team. It's a real shame for the team and organisation to be losing
                                   his talent. Fingers crossed the team can find someone like Ian to replace him...
                                   """)
            else:
                print_long_message("""\
                                   Despite a successful publishing round, Ian's been feeling really demotivated and has
                                   decided to leave the team. It's a real shame for the team and organisation to be losing
                                   his talent. Fingers crossed the team can find someone like Ian to replace him...
                                   """)

        return None