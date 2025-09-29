from abc import ABC, abstractmethod
from rap_rpg.utils.display_utils import print_options

class Event(ABC):
    def __init__(self, event_text, options, game_state = None):
        self.event_text = event_text
        self.options = options # ["option 1", "option 2"...] or None
        self.game_state = game_state # If the event needs to know about the game state
        self.choice = None # This is -1 what the user sees (e.g user option 1 gives self.choice 0)
        self.game_state_modifier = None # Updated from effect of event on the game. Mainly: "process_quality", "team_motivation", "late_risk"
        self.dice_res = None
    
        print(self.event_text)

    def _prompt_choice(self):
        print_options(self.options)
        self.choice = self._take_and_validate_choice_input() - 1
        return None
    
    def _take_and_validate_choice_input(self):
        valid_choices = [int(i) for i in range(1, len(self.options) + 1)]
        while True:
            try:
                choice = int(input("\nWhat do you choose? "))
                if choice in valid_choices:
                    return choice
                else:
                    print(f"That wasn't a valid choice. Pick an integer from 1 to {len(valid_choices)}.")
            except ValueError:
                print(f"That wasn't a valid choice. Pick an integer from 1 to {len(valid_choices)}.")
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                exit()
    
    def _roll_the_dice(self):
        valid_choices = [int(i) for i in range(1, 7)]
        print("\n", end = "")
        while True:
            try:
                dice_res = int(input("What did you roll? "))
                if dice_res in valid_choices:
                    self.dice_res = dice_res
                    return dice_res
                else:
                    print(f"That wasn't a valid choice. Pick from 1 to 6, like a dice!\n")
            except ValueError:
                print(f"That wasn't a valid choice. Pick from 1 to 6, like a dice!\n")
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                exit()
    
    def _print_game_mod_outcome(self):
        if self.game_state_modifier is not None:
            print("")
            for k, v in self.game_state_modifier.items():
                print(f"{"+" if v > 0 else ""}{v} to {k.replace("_", " ").lower()}")
        return None
    
    @abstractmethod
    def _handle_choice(self): # Abstract because events can return different game modifiers
        pass