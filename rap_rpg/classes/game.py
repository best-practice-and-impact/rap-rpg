from rap_rpg.utils import display_utils

class Game:
    def __init__(self, events_list):
        self.events = events_list
        self.game_state = {"process_quality": 0, "late_risk": 0, "team_motivation": 0}
    
    def run(self):
        input(intro_msg)
        for event in self.events:
            print(display_utils.delim)
            stage = event()
            if stage.game_state_modifier:
                for k, v in stage.game_state_modifier.items():
                    if k in ("process_quality", "late_risk", "team_motivation"):
                        self.game_state[k] += stage.game_state_modifier.get(k, 0)
                    else:
                        self.game_state[k] = v
            input(display_utils.continue_message)
        print(self.game_state)
        # Todo: add publication day
        print(outro_msg)
        return None

intro_msg = f"""{display_utils.delim}\nThis is a role-playing game about a statistics production team.

Throughout this story the team will be faced with choices about their code and how they work together. 
We’re going to find out if they can successfully produce their statistic on time and without errors!
Choices that help them work together effectively will boost their process and code quality.
But, choices that make it harder to collaborate will make it more likely there will be a delay or an error.\n
Play along with a dice, or virtual dice roller.

To quit at any time, use CTRL and C. {display_utils.continue_message}"""

outro_msg = f"""{display_utils.delim}\nThank you for playing the demo of RAP-RPG!"

If you're interested in continuous improvement, take a look at some of these resources:

For tips on improving your code quality, check out Quality Assurance of Code for Analysis and Research
(lovingly known as the Duck Book) which is just an online search away.

YouTube is a fantastic resource too - search for software development best practice.

Check out Atlassian for help getting started with git.

For broader process assurance tips, ONS Quality Central is your one-stop shop; find the link on Reggie, or just search 'Quality'.

For bespoke coding advice and a friendly chat, come talk to us at Analysis Standards and Pipelines. We
take a holistic look at process quality to make personalised recommendations, deliver workshops
on RAP and git, and signpost other awesome learning. :)

We'd really welcome your feedback on our game - let us know at ASAP@ons.gov.uk. You're welcome to contribute too!

Have a great day!"""