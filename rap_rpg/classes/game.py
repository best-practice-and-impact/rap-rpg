from rap_rpg.utils import display_utils
from rap_rpg.events.publication_event import Publication

class Game:
    def __init__(self, events_list):
        self.events = events_list
        self.game_state = {"process_quality": 0, "late_risk": 0, "team_motivation": 0}
    
    def run(self):
        print(intro_msg, end="")
        input(display_utils.continue_message)
        for event in self.events:
            print(display_utils.delim)
            stage = event()
            if stage.game_state_modifier:
                for k, v in stage.game_state_modifier.items():
                    if isinstance(v, bool):
                        self.game_state[k] = v
                    elif isinstance(v, int):
                        self.game_state[k] += stage.game_state_modifier.get(k, 0)
            input(display_utils.continue_message)
        # print(self.game_state)
        print(display_utils.delim)
        Publication(self.game_state)
        input(display_utils.continue_message)
        print(outro_msg)
        return None

intro_msg = f"""{display_utils.delim}
This is a role-playing game about a statistics production team.
Throughout this story the team will be faced with choices about their code and how they work together. 
We’re going to find out if they can successfully produce their statistic on time and without errors!

Choices that help them work together effectively and improve the quality of their processes
make it less likely that there will be a delay or an error.

Play along with a dice or virtual dice roller. To quit at any time, use CTRL and C. 
"""

outro_msg = f"""{display_utils.delim}\nThank you for playing the demo of RAP-RPG!

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