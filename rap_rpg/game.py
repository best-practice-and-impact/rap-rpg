from rap_rpg.display_utils import print_long_message, delim
import json
import os
from questionary import select, Style
from rap_rpg.events import Event

style = Style([
        ("pointer", "fg:#F46A25 bold"),
        ("selected", "noinherit fg:#F46A25 bold"),
        ("highlighted", "fg:#F46A25 bold"),
        ("answer", "fg:#F46A25 bold")
    ])

class Game:
    """Main game class."""

    def __init__(self, events_folder: str, intro_msg: str, close_msg: str) -> None:
        """
        Initialise the game.

        Args:
            events_folder (str): Path to the folder containing event JSON config files.
            intro_msg (str): Message displayed at the start of the game.
            close_msg (str): Message displayed at the end of the game.
        """
        events_configs = []
        events_configs = []
        for filename in os.listdir(events_folder):
            if filename.endswith(".json"):
                with open(os.path.join(events_folder, filename), "r") as f:
                    event_data = json.load(f)
                    events_configs.append(event_data)
        self.game_state = {"process_quality": 0, "late_risk": 0, "team_motivation": 0}

        self.events = [Event(**config, game_state_attributes=list(self.game_state.keys())) for config in events_configs]
        self.intro_msg = intro_msg 
        self.close_msg = close_msg

    def _take_choice_input(self, event: Event) -> int:
        """
        Present the player with a choice prompt and return the selection index.

        Args:
            event (Event): The current event whose choices are presented.

        Returns:
            int: Index of the selected choice.
        """
        try:
            choices = [event.get_choice_text(i) for i in range(len(event.choices))]
            choice = select("What do you choose?", choices=choices, qmark="🔍 ", style=style).ask()
            choice_index = choices.index(choice)
            return choice_index
        except (KeyboardInterrupt):
            print("\nThanks for playing!")
            exit()

    def start_game(self) -> None:
        """Reset game state."""
        self.event_id = 0        
        self.game_state = {"process_quality": 0, "late_risk": 0, "team_motivation": 0}
       
        print_long_message(self.intro_msg)
        input("\nPress enter to start...")
        self.run_event()

    def run_event(self) -> None:
        """
        Run the current event.
        """
        event = self.events[self.event_id]
        print_long_message(event.text)
        input("\n....Press enter to continue...")

        choice_index = self._take_choice_input(event)
        die_roll = int(select("Roll the die:", choices=["1", "2", "3", "4", "5", "6"], qmark="🎲", style=style).ask())
        outcome_text, modifiers = event.set_choice(choice_index, die_roll)
        print_long_message(outcome_text)
        input("\n....Press enter to continue...")

        self.game_state = {key: self.game_state[key] + modifiers[key] if key in modifiers else self.game_state[key] for key in self.game_state.keys()}
        self.event_id += 1

        if self.event_id < len(self.events) - 1:
            self.run_event()
        else:
            self.end_game()

    def end_game(self) -> None:
        """Display the closing message and prompt the player to restart or quit."""
        print_long_message(self.close_msg)
        input("\nPress enter to continue...")
        restart = select("Do you want to restart?", choices=["Yes", "No"], qmark="🔄", style=style).ask()
        if restart == "Yes":
            self.start_game()
        else:
            print("Thanks for playing!")
