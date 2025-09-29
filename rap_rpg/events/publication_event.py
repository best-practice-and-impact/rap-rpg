from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message
from random import randint

class Publication(Event):
    def __init__(self, game_state):
        self.event_text = "After several weeks of work, it's time for publication day! "
        self.game_state = game_state
        super().__init__(self.event_text, options = None, game_state=self.game_state)
        
        self._handle_choice()
    
    def _handle_choice(self):
        if self.options is None:
            self._run_chance()
        else:
            raise ValueError(f"The options associated with the event should be None, or supply an implementation of _handle_choice.")
        return None
    
    def _run_chance(self):
        process_quality = self.game_state.get("process_quality", 0) # From AI, Review, Scrum: -2 to 3
        team_motivation = self.game_state.get("team_motivation", 0) # From AI, Review, Scrum: -2 to 2
        late_risk = self.game_state.get("late_risk", 0) # From AI, Review, Scrum: 0 to 2
        late = False

        if late_risk != 0:
            if late_risk == 1:
                late_or_not = randint(0, 1)
                if late_or_not == 0:
                    print("The publication is out on time. Phew!")
                    late = False
                else:
                    print("The analysis isn't going to be ready on time.")
                    late = True
                        
                        
            elif late_risk == 2:
                print("The publication is running behind schedule.")
                late = True
        
        if late is True:
            print("Let's roll to find out how late it will be.")
            self._roll_the_dice()
            if team_motivation >= 0:
                if self.dice_res >= 3:
                    print_long_message("""\
                                       The team are thankfully well-motivated, and get the analysis finished. The delay could have been
                                       a lot worse, and they've earned a good break when this is done.
                                       """)
                else:
                    print_long_message("""\
                                       The team were motivated, but it wasn't enough to mitigate the delay. It takes a while
                                       to finish the analysis.
                                       """)
            else:
                print("The team are understandably very demotivated. It takes a while to finish the analysis.")

        if process_quality <= 0:
            print("When the publication goes out, there's an error. Oops - let's roll to find out how bad it is.")
            self._roll_the_dice()
            if self.dice_res <= 2:
                print_long_message("""\
                                   It's a major error. Ugh! There's disruption to the downstream stakeholders in other
                                   Government departments, as well as organisations in other sectors too. There is
                                   damage to the reputation of ONS as an organisation for quality statistics. If our quality
                                   assurance processes and ways of working had been more robust, maybe we could have avoided this.
                                   """)
                error = True
            else:
                print_long_message("""\
                                   It's thankfully a minor error that can be resolved fairly quickly. Still, it's not ideal. A larger
                                   error could have slipped through. The team will be taking a look at their quality assurance
                                   processes to aim to prevent this next time.
                                   """)
                error = True
        else:
            print("The publication comes out without errors. Awesome!")

        return None