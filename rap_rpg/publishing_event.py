from classes.dice_check import DiceCheck

def publishing_day(game_state = None, success_threshold = 4):
    publication = DiceCheck("Publiation success or not", "It's publishing day! ",
                            "Roll to see how the team got on! ", success_threshold,
                            "Oh no, there was a problem!",
                            "The publication went great - it came out on time, and up to standard.")

    print(publication.choice_text, end = "")
    pass # Todo
    return None

publishing_day()