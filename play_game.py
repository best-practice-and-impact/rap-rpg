from rap_rpg.events.new_ai_event import NewAIAgent
from rap_rpg.events.review_event import Review
from rap_rpg.events.scrum_master_event import Agile
from rap_rpg.classes.game import Game

import logging
import traceback

if __name__ == "__main__":
    events_list = [Agile, Review, NewAIAgent]

    try:
        rap_game = Game(events_list)
        rap_game.run()
    
    except KeyboardInterrupt:
        print("\n\nThank you for playing!")
    except Exception as e:
        logging.error(traceback.format_exc())