import pytest
import rap_rpg.game
from rap_rpg.game import Game
EVENTS_FOLDER = "tests/event_configs/"


@pytest.fixture
def game(intro = "Welcome!", close = "Goodbye!"):
    return Game(
        events_folder=EVENTS_FOLDER,
        intro_msg=intro,
        close_msg=close
    )


class TestGameInit:
    def test_loads_all_events_from_folder(self, game):
        assert len(game.events) == 2

    def test_events_are_event_instances(self, game):
        from rap_rpg.events import Event
        assert all(isinstance(e, Event) for e in game.events)

    def test_event_ids_match_configs(self, game):
        assert {e.id for e in game.events} == {"test1", "test2"}

    def test_initial_game_state_keys(self, game):
        assert set(game.game_state.keys()) == {"process_quality", "late_risk", "team_motivation"}

    def test_initial_game_state_values_are_zero(self, game):
        assert all(v == 0 for v in game.game_state.values())

    def test_intro_msg_stored(self, game):
        assert game.intro_msg == "Welcome!"

    def test_close_msg_stored(self, game):
        assert game.close_msg == "Goodbye!"

    def test_ignores_non_json_files(self, tmp_path):
        (tmp_path / "event.json").write_text('{"id":"e1","text":"t","choices":[{"text":"c","roll_boundaries":[3],"bad_outcome_text":"b","bad_outcome_modifiers":{"process_quality":-1},"good_outcome_text":"g","good_outcome_modifiers":{"process_quality":1}}]}')
        (tmp_path / "readme.txt").write_text("not an event")
        g = Game(events_folder=str(tmp_path), intro_msg="Hi", close_msg="Bye")
        assert len(g.events) == 1

    def test_empty_folder_loads_no_events(self, tmp_path):
        g = Game(events_folder=str(tmp_path), intro_msg="Hi", close_msg="Bye")
        assert g.events == []

class TestTakeChoiceInput:
    @pytest.mark.parametrize("choice_index", [0, 1])
    def test_valid_choice_returns_index(self, game, monkeypatch, choice_index):
        event = game.events[0]
        choice_text = event.get_choice_text(choice_index)
        def mock_select(*args, **kwargs):
            return type('obj', (object,), {'ask': lambda self: choice_text})()
        monkeypatch.setattr(rap_rpg.game, 'select', mock_select)
        index = game._take_choice_input(event)
        assert index == choice_index

    def test_keyboard_interrupt_exits_game(self, game, monkeypatch):
        event = game.events[0]
        monkeypatch.setattr(rap_rpg.game, 'select', lambda *args, **kwargs: type('obj', (object,), {'ask': lambda self: (_ for _ in ()).throw(KeyboardInterrupt)})())
        with pytest.raises(SystemExit):
            game._take_choice_input(event)


class TestStartGame:
    def start_game_resets_game_state(self, game):
        game.game_state = {"process_quality": 5, "late_risk": 3, "team_motivation": 2}
        game.event_id = 10
        game.start_game()
        assert game.game_state == {"process_quality": 0, "late_risk": 0, "team_motivation": 0}
        assert game.event_id == 0

    @pytest.mark.parametrize("intro_msg", ["Welcome!", "Hello, adventurer!", "Let the game begin!"])
    def test_start_game_prints_intro_message(self, intro_msg, monkeypatch, capsys):
        game = Game(events_folder=EVENTS_FOLDER, intro_msg=intro_msg, close_msg="Goodbye!")
        monkeypatch.setattr('builtins.input', lambda prompt="": "")
        monkeypatch.setattr(game, 'run_event', lambda: None)
        game.start_game()
        captured = capsys.readouterr()
        assert intro_msg in captured.out

