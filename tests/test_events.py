import pytest
from rap_rpg.events import Event, Choice


VALID_CHOICE = {
    "text": "Choice A",
    "roll_boundaries": [3],
    "bad_outcome_text": "Bad outcome.",
    "bad_outcome_modifiers": {"process_quality": -1},
    "good_outcome_text": "Good outcome.",
    "good_outcome_modifiers": {"process_quality": 1},
}

VALID_CHOICE_MID = {
    "text": "Choice B",
    "roll_boundaries": [2, 4],
    "bad_outcome_text": "Bad outcome.",
    "bad_outcome_modifiers": {"process_quality": -1},
    "mid_outcome_text": "Mid outcome.",
    "mid_outcome_modifiers": {"process_quality": 0},
    "good_outcome_text": "Good outcome.",
    "good_outcome_modifiers": {"process_quality": 1},
}


class TestEventInit:
    def test_valid_event_creates_instance(self):
        event = Event(id="test", text="Test event.", choices=[VALID_CHOICE])
        assert event.id == "test"
        assert event.text == "Test event."
        assert len(event.choices) == 1

    def test_invalid_id_type_raises_type_error(self):
        with pytest.raises(TypeError):
            Event(id=123, text="Text.", choices=[VALID_CHOICE])

    def test_invalid_text_type_raises_type_error(self):
        with pytest.raises(TypeError):
            Event(id="test", text=123, choices=[VALID_CHOICE])

    def test_choices_not_list_raises_type_error(self):
        with pytest.raises(TypeError):
            Event(id="test", text="Text.", choices=VALID_CHOICE)

    def test_choice_missing_required_key_raises_value_error(self):
        bad_choice = {k: v for k, v in VALID_CHOICE.items() if k != "good_outcome_text"}
        with pytest.raises(ValueError):
            Event(id="test", text="Text.", choices=[bad_choice])

    def test_choice_unexpected_key_raises_value_error(self):
        bad_choice = {**VALID_CHOICE, "unexpected_key": "value"}
        with pytest.raises(ValueError):
            Event(id="test", text="Text.", choices=[bad_choice])

    def test_invalid_game_state_key_raises_value_error(self):
        with pytest.raises(ValueError):
            Event(id="test", text="Text.", choices=[VALID_CHOICE], game_state_attributes=["late_risk"])


class TestEventGetChoiceText:
    def test_returns_choice_text(self):
        event = Event(id="test", text="Text.", choices=[VALID_CHOICE])
        assert event.get_choice_text(0) == "Choice A"


class TestEventSetChoice:
    def test_bad_outcome_on_low_roll(self):
        event = Event(id="test", text="Text.", choices=[VALID_CHOICE])
        text, modifiers = event.set_choice(0, 1)
        assert text == "Bad outcome."
        assert modifiers == {"process_quality": -1}

    def test_good_outcome_on_high_roll(self):
        event = Event(id="test", text="Text.", choices=[VALID_CHOICE])
        text, modifiers = event.set_choice(0, 6)
        assert text == "Good outcome."
        assert modifiers == {"process_quality": 1}

    def test_mid_outcome_on_mid_roll(self):
        event = Event(id="test", text="Text.", choices=[VALID_CHOICE_MID])
        text, modifiers = event.set_choice(0, 3)
        assert text == "Mid outcome."
        assert modifiers == {"process_quality": 0}

    def test_invalid_choice_index_raises_index_error(self):
        event = Event(id="test", text="Text.", choices=[VALID_CHOICE])
        with pytest.raises(IndexError):
            event.set_choice(5, 3)


class TestChoiceGetRoll:
    def test_bad_outcome_at_boundary(self):
        choice = Choice(**VALID_CHOICE)
        text, modifiers = choice.get_roll(3)
        assert text == "Bad outcome."

    def test_good_outcome_above_boundary(self):
        choice = Choice(**VALID_CHOICE)
        text, modifiers = choice.get_roll(4)
        assert text == "Good outcome."


@pytest.mark.parametrize("bad_modifiers,mid_modifiers,good_modifiers,roll,expected_modifiers", [
    # Single-stat changes
    ({"process_quality": -1}, None, {"process_quality": 1}, 1, {"process_quality": -1}),
    ({"process_quality": -1}, None, {"process_quality": 1}, 6, {"process_quality": 1}),
    # Multi-stat bad outcome
    ({"process_quality": -2, "team_morale": -1}, None, {"process_quality": 2}, 2, {"process_quality": -2, "team_morale": -1}),
    # Multi-stat good outcome
    ({"process_quality": -1}, None, {"process_quality": 1, "team_morale": 2}, 6, {"process_quality": 1, "team_morale": 2}),
    # Zero-value modifier
    ({"process_quality": 0}, None, {"process_quality": 1}, 1, {"process_quality": 0}),
    # Three-outcome: bad
    ({"process_quality": -2}, {"process_quality": 0}, {"process_quality": 2}, 2, {"process_quality": -2}),
    # Three-outcome: mid
    ({"process_quality": -2}, {"process_quality": 0}, {"process_quality": 2}, 3, {"process_quality": 0}),
    # Three-outcome: good
    ({"process_quality": -2}, {"process_quality": 0}, {"process_quality": 2}, 6, {"process_quality": 2}),
    # Three-outcome: multi-stat mid
    ({"process_quality": -1}, {"process_quality": 0, "team_morale": 1}, {"process_quality": 2, "team_morale": 2}, 3, {"process_quality": 0, "team_morale": 1}),
    # Empty modifiers (no stat change)
    ({}, None, {}, 1, {}),
])
def test_get_roll_outcome_modifiers(bad_modifiers, mid_modifiers, good_modifiers, roll, expected_modifiers):
    has_mid = mid_modifiers is not None
    choice = Choice(
        text="Test choice",
        roll_boundaries=[2, 4] if has_mid else [2],
        bad_outcome_text="Bad outcome.",
        bad_outcome_modifiers=bad_modifiers,
        mid_outcome_text="Mid outcome." if has_mid else None,
        mid_outcome_modifiers=mid_modifiers,
        good_outcome_text="Good outcome.",
        good_outcome_modifiers=good_modifiers,
    )
    _, modifiers = choice.get_roll(roll)
    assert modifiers == expected_modifiers
