from random import shuffle
from dataclasses import dataclass, field
from typing import Optional

@dataclass(init=False)
class Event:
    """Represents a game event."""

    def __init__(self, id: str, text: str, choices: list):
        """
        Initialise the event.

        Args:
            id (str): Unique identifier for the event.
            text (str): Narrative text displayed to the player.
            choices (list): List of dicts, each containing the fields required by Choice.
        """
        self.id = id
        self.text = text
        self.choices = [Choice(**c) for c in choices]
        shuffle(self.choices)

    def get_choice_text(self, choice_index: int):
        """
        Return the display text for the choice at the given index.

        Args:
            choice_index (int): choice number beginning at 0.

        Returns:
            str: choice text.
        """
        return self.choices[choice_index].text

    def set_choice(self, choice_index: int, roll: int):
        """
        Resolve a player's choice and dice roll, returning the outcome text and modifiers.

        Args:
            choice_index (int): choice number beginning at 0.
            roll (int): The dice roll.

        Returns:
            tuple[str, dict]: The outcome text and dict of stat modifiers.

        Raises:
            IndexError: If choice_index is out of range.
        """
        if choice_index < 0 or choice_index >= len(self.choices):
            raise IndexError("Choice index out of range.")
        return self.choices[choice_index].get_roll(roll)

@dataclass
class Choice:
    """Represents a single player choice within an event
    
    Attributes:
        text (str): choice text.
        roll_boundaries (list[int]): The thresholds for determining bad, mid, and good outcomes.
            Supply a single value for a two-outcome choice, or two values for a three-outcome choice.
        good_outcome_text (str): good outcome text
        good_outcome_modifiers (dict): good outcome stat modifiers
        mid_outcome_text (str): mid outcome text
        mid_outcome_modifiers (dict): mid outcome stat modifiers
        bad_outcome_text (str): bad outcome text
        bad_outcome_modifiers (dict): bad outcome stat modifiers
    """

    text: str
    roll_boundaries: list[int]
    good_outcome_text: str
    good_outcome_modifiers: dict
    bad_outcome_text: str
    bad_outcome_modifiers: dict
    mid_outcome_text: Optional[str] = None
    mid_outcome_modifiers: Optional[dict] = None

    def get_roll(self, roll: int):
        """
        Return the outcome text and game modifiers based on the dice roll.

        Args:
            roll (int): The dice roll.

        Returns:
            tuple[str, dict]: The outcome text and dict of stat modifiers.
        """
        if roll <= self.roll_boundaries[0]:
            return self.bad_outcome_text, self.bad_outcome_modifiers
        elif len(self.roll_boundaries) > 1 and roll <= self.roll_boundaries[1]:
            return self.mid_outcome_text, self.mid_outcome_modifiers
        else:
            return self.good_outcome_text, self.good_outcome_modifiers
