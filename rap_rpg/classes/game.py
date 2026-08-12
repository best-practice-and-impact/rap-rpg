from utils.display_utils import print_long_message, delim
from events.publication_event import Publication
import events
import json
import os
from questionary import select, Style

style = Style([
        ("pointer", "fg:#F46A25 bold"),
        ("selected", "noinherit fg:#F46A25 bold"),
        ("highlighted", "fg:#F46A25 bold"),
        ("answer", "fg:#F46A25 bold")
    ])

class Game:
    def __init__(self, events_folder, intro_msg, close_msg):
        events_configs = []
        for filename in os.listdir(events_folder):
            if filename.endswith(".json"):
                with open(os.path.join(events_folder, filename), "r") as f:
                    event_data = json.load(f)
                    events_configs.append(events.Event(**event_data))

        self.events = [events.Event(**event_config) for event_config in events_configs]
        self.intro_msg = intro_msg 
        self.close_msg = close_msg

    def _take_and_validate_choice_input(self, options):
        try:
            choice = select("What do you choose?", choices=options.text, qmark="🔍 ", style=self.style).ask()
            choice_index = self.options.index(choice)
            return choice_index
        except (KeyboardInterrupt, ValueError):
            print("\nThanks for playing!")
            exit()

    def start_game(self):
        self.event_id = 0        
        self.game_state = {"process_quality": 0, "late_risk": 0, "team_motivation": 0}
       
        print_long_message(self.intro_msg)
        input("\nPress enter to start...")
        self.run_event()



    def run_event(self):
        event = self.events[self.event_id]
        print_long_message(event.text)
        input("\n....Press enter to continue...")

        choices = [event.get_choice_text(i) for i in range(len(event.choices))]
        choice_index = self._take_and_validate_choice_input(choices)
        die_roll = int(input("Roll the die (1-6): "))
        outcome_text, modifiers = event.set_choice(choice_index, die_roll)
        print_long_message(outcome_text)
        input("\n....Press enter to continue...")

        self.game_state = {key: self.game_state[key] + modifiers[key] for key in self.game_state.keys()}
        self.event_id += 1

        if self.event_id < len(self.events) - 1:
            self.run_event()
        else:
            self.end_game()



    def end_game(self):
        print_long_message(self.close_msg)
        input("\nPress enter to continue...")
        Publication(self.game_state)
        restart = input("\nDo you want to restart (Y/N)? ")
        if restart.upper() == "Y":
            self.start_game()
        else:
            print("Thanks for playing!")


intro_msg = f"""{delim}
This is a role-playing game about a statistics production team.
Throughout this story the team will be faced with choices about their code and how they work together. 
We’re going to find out if they can successfully produce their statistic on time and without errors!

Choices that help them work together effectively and improve the quality of their processes
make it less likely that there will be a delay or an error.

Play along with a dice or virtual dice roller. To quit at any time, use CTRL and C. 
"""

outro_msg = f"""{delim}\nThank you for playing the demo of RAP-RPG!

If you're interested in continuous improvement, take a look at some of these resources:

For tips on improving your code quality, check out Quality Assurance of Code for Analysis and Research
(lovingly known as the Duck Book) which is just an online search away.

YouTube is a fantastic resource too - search for software development best practice.

Check out Atlassian for help getting started with git.

For broader process assurance tips, ONS Quality Central is your one-stop shop; find the link on Reggie, or just search 'Quality'.

For bespoke coding advice and a friendly chat, come talk to us at Analysis Standards and Pipelines. We
take a holistic look at process quality to make personalised recommendations, deliver workshops
on RAP and git, and signpost other awesome learning. :)

We'd really welcome your feedback on our game, and you're welcome to contribute too!

Get in touch at ASAP@ons.gov.uk. Have a great day!"""