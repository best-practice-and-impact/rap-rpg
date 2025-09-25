from abc import ABC, abstractmethod
from rap_rpg.classes.dice_check import DiceCheck
from rap_rpg.utils.display_utils import print_options

class Event(ABC):
    def __init__(self, event_text, options:list, outcomes:list, game_state_modifier = None):
        self.event_text = event_text # What the event is
        self.options = options # Options for the user to choose from
        self.outcomes = outcomes # Outcomes corresponding to the options
        self.user_choice = None # What the user picks - this starts at 1
        self.game_state_modifier = game_state_modifier # Effects on the game

        for outcome in outcomes:
            if not isinstance(outcome, DiceCheck|str):
                raise TypeError(f"All outcomes need to be DiceChecks or strs. Check the type of {outcome}.")
    
        print(self.event_text)
        self._prompt_choice()
        self._handle_choice()

    def _prompt_choice(self):
        print_options(self.options)
        self.user_choice = self._take_and_validate_choice_input()
        return None
    
    def _take_and_validate_choice_input(self):
        valid_choices = [int(i) for i in range(1, len(self.options) + 1)]
        while True:
            try:
                choice = int(input("What do you choose? "))
                if choice in valid_choices:
                    return choice
                else:
                    print(f"That wasn't a valid choice. Pick an integer from 1 to {len(valid_choices)}.")
            except ValueError:
                print(f"That wasn't a valid choice. Pick an integer from 1 to {len(valid_choices)}.")
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                exit()
    
    @abstractmethod
    def _handle_choice(self): # Abstract because events can return different game modifiers
        pass