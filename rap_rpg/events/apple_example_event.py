from rap_rpg.classes.event_abc import Event
from rap_rpg.classes.dice_check import DiceCheck

eat_apple = DiceCheck("Take apple", "You take the apple. It's red and shiny. ",
                      "Roll to see if it's nice! ", 3,
                      "The apple is rotten! Yuck!", "The apple is really juicy and yum!")
dont_eat_apple = DiceCheck("Reject apple", "You politely turn down the apple. ",
                           "What happens next? Roll the dice: ", 6,
                           "*stomach rumble*", "A worm crawls out the apple. Good thing you didn't want it!")

class OfferedAnApple(Event):
    def __init__(self):
        self.event_text = "Would you like an apple?"
        self.options = ["Yes please!", "No, thank you."]
        self.outcomes = [eat_apple, dont_eat_apple]
        self.got = None
        super().__init__(self.event_text, self.options, self.outcomes)
    
    def _handle_choice(self):
        choice = self.outcomes[self.user_choice-1]
        if isinstance(choice, DiceCheck):
            print(choice.choice_text, end = "")
            self.got = choice._handle_dicecheck()

            if ((self.user_choice == 1) and (self.got[0] == False)): # Option 1, failing the roll
                self.game_state_modifier = {"ill": True}
            elif (self.user_choice == 2 and self.got[0] == False): # Option 2, failing the roll
                self.game_state_modifier = {"hungry": True}
            print(self.got[1])

        else:
            self.got = choice
            print(self.got)
        
        return None