from rap_rpg.events.new_ai_agent import NewAIAgent
from rap_rpg.events.review_event import Review
from rap_rpg.classes.game import Game

if __name__ == "__main__":
    events_list = [Review, NewAIAgent]

    rap_game = Game(events_list)
    rap_game.run()