from rap_rpg.classes.event_abc import Event
from rap_rpg.utils.display_utils import print_long_message
from functools import partial

class Agile(Event):
    def __init__(self):
        self.event_text = """The team leader, Gail, knows Agile is generally the best way to handle software development but
don't have much experience with it. They manage to create a new post - what role do they hire for?"""
        self.options = ["A scrum master", "A delivery manager"]
        
        super().__init__(self.event_text, self.options)
        self._prompt_choice()
        self._handle_choice()
    
    def _handle_choice(self):
        outcome1 = """\
            The team make some changes to the pipeline, but the work is running behind because they had to fix issues
            where colleagues had duplicated work and not co-ordinated code changes properly.\n
            """
        outcome2 = """\
            The team manage to make some changes to the pipeline, but it has taken a while as they had to go back
            and address some bugs stemming from duplicated work. The team learn from the experience and
            commit to communicating better so they can continually improve going forward!\n
            """
        outcome3 = """\
            The team manage to make loads of improvements to the pipeline, and even clear some technical debt!
            Because the focus was on ensuring they whole team understood the bigger picture and could all input into the work,
            motivation was high and issues were anticipated before they happened. There was great
            communication and the team had plenty of ideas that were listened to about improving ways of working as well as how
            to design the new features. Well done team!\n
            """

        if self.choice == 0:
            print_long_message("""\
                               The new scrum master, Derek, can run the scrum ceremonies like standups and sprints as well as keep the
                               team motivated. Roll to see how he gets on!
                               """)
            self._roll_the_dice()
            if self.dice_res <= 2:
                print_long_message("""\
                                   Derek is enthusiastic, but inexperienced. His enthusiasm and innovative way of thinking helps keep
                                   the team motivated and moving forward, but several team members need to take an agile course to learn the basics.
                                   Worst of all, there's still loads of admin...
                                   """)
                print("\n", end = "")
                print_long_message(outcome2)
                self.game_state_modifier = {"late_risk": 1}
            else:
                print_long_message("""\
                                   Derek is experienced and helps Gail (designated the product owner) collate an organised, prioritised
                                   backlog and set up sprints. Derek ensures stand-ups are short and sweet, and there is always a retro
                                   so the team can problem solve issues together, and improve their processes.
                                   """)
                print("\n", end = "")
                print_long_message(outcome3)

                self.game_state_modifier = {"process_quality": 1, "team_motivation": 1}

        elif self.choice == 1:
            print_long_message("""\
                               The new delivery manager, Ola, will be great at helping Gail keep on top of the admin
                               and reporting in to the Programme Management Office. Roll to see how she gets on!""")
            self._roll_the_dice()

            if self.dice_res <= 2:
                print_long_message("""\
                                   Ola is keen on waterfall, and insists on creating multiple documents to keep track of things on
                                   Excel and Word. She helps clear a lot of reporting and boring tasks out the way so the team can
                                   focus on coding, but they struggle to prioritise tasks and understand the bigger picture of what they
                                   are doing. It leads to duplicated tasks and some dissatisfaction.\n
                                   """)
                print("\n", end = "")
                print_long_message(outcome1)

                self.game_state_modifier = {"team_motivation": -1}

            elif self.dice_res <= 5:
                print_long_message("""\
                                   Ola is organised, thoughtful, and has some agile knowledge. However, the team struggle to prioritise
                                   tasks and discuss them in a way that really gets things moving. Maybe an experienced scrum master would
                                   have been better...\n
                                   """)
                print("\n", end = "")
                print_long_message(outcome2)
                self.game_state_modifier = {"late_risk": 1}

            else:
                print_long_message("""\
                                   Ola is well-versed in agile and lean, gives Gail tips on how to run efficient sprints and stand-ups.
                                   Best of all, the team's work is laid out nicely on a Jira board. But, the team spend a fair bit of time
                                   sprint planning and stand-ups are quite long and unfocused. The team are interested, but don’t
                                   contribute to the overall decision making, so things take a while to get going. Maybe an experienced
                                   scrum master would know what to do? Anyhow -\n
                                   """)
                print("\n", end = "")
                print_long_message(outcome3)
                self.game_state_modifier = {"process_quality": 1, "team_motivation": 1}
                
        print("\n", end = "")
        print_long_message("""\
                           Agile works best when people collaborate to create a self-managing team where everyone is able to
                           contribute to work, decisions are made democratically, and everyone understands the bigger picture.
                           """)

        self._print_game_mod_outcome()

        return None