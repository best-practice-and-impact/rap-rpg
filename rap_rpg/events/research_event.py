from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message

class Research(Event):
    def __init__(self):
        self.event_text = """The team have researched a new method that they want to implement into their production round.\n
The code is not currently written to RAP standards, but the team face a tight deadline. What should they do?"""
        self.options = ["Implement the new method without rewriting the research code. They know the method works",
                        "Rewrite the research code to meet RAP standards, even though it will take a while"]
        super().__init__(self.event_text, self.options)

        self._prompt_choice()
        self._handle_choice()

    def _handle_choice(self):
        if self.choice == 0:
            print_long_message("""\
                               The team decide to implement the new method without rewriting the research code due to the time it
                               will take. Roll the dice to see what happens.
                               """)
            self._roll_the_dice()
            if self.dice_res <= 3:
                print_long_message("""\
                                   The team face a number of errors whilst running the research code, which causes a massive delay to their production round. 
                                   They miss deadlines within their production round, which causes a lot of stress among the team.
                                   """)
                self.game_state_modifier = {"process_quality": -1, "team_motivation": -1, "late_risk": 1}

            else:
                print_long_message("""\
                                   The team face a few errors whilst running the research code, which causes some delays to their production round. 
                                   They manage to meet their deadlines within their production round, but it was a stressful experience for the team 
                                   that they don't want to repeat!
                                   """)
                self.game_state_modifier = {"process_quality": -1, "team_motivation": -1}


        elif self.choice == 1:
            print_long_message("""\
                               The team decide to rewrite the research code to meet RAP standards, even though it will take a while. 
                               Let's roll the dice and see how it goes!
                               """)
            self._roll_the_dice()
            if self.dice_res <= 2:
                print_long_message("""\
                                   The team spend some time rewriting the research code to meet RAP standards, but they don't consider 
                                   the design of the code or understand what good quality RAP code looks like. They miss 
                                   their deadline for the production round with only some of the code having been rewritten and have to resort to 
                                   running the research code. 
                                   """)
                self.game_state_modifier = {"late_risk": 1, "process_quality": -1}

            elif self.dice_res <= 4:
                print_long_message("""\
                                   The team spend some time rewriting the research code to meet RAP standards, but they're not completely sure what
                                   good RAP code looks like. Luckily, Bob has some experience in writing production code, and takes on a lot of the rewriting work
                                   himself. They just about get the code ready for the production round, but only Bob understands what the code is doing.
                                   The team now carry some technical debt and a single point of failure in Bob. 
                                   """)
                self.game_state_modifier = {"process_quality": -1}
            else:
                print_long_message("""\
                                   The team reach out to the central RAP team for support with rewriting their research code. The central RAP team 
                                   provide them with guidance on how to design the code and write high-quality RAP code. The team also make use of resources
                                   such as the Duck Book to help them improve their understanding of RAPs. With the right support and guidance, the team successfully
                                   rewrite their research code as a RAP in time for their production round.
                                   """)
                self.game_state_modifier = {"process_quality": 1, "team_motivation": 1}
        
        self._print_game_mod_outcome()
        return None