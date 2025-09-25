class DiceCheck:
    def __init__(self, choice, choice_text, roll_prompt, pass_threshold, low_outcome, high_outcome):
        self.choice = choice
        self.choice_text = choice_text
        self.roll_prompt = roll_prompt
        self.pass_threshold = pass_threshold
        self.low_outcome = low_outcome
        self.high_outcome = high_outcome
        self.check_result = None

    def _roll_the_dice(self):
        valid_choices = [int(i) for i in range(1, 7)]
        while True:
            try:
                dice_res = int(input("What did you roll? "))
                if dice_res in valid_choices:
                    self.result = dice_res
                    return None
                else:
                    print(f"That wasn't a valid choice. Pick from 1 to 6, like a dice!\n")
            except ValueError:
                print(f"That wasn't a valid choice. Pick from 1 to 6, like a dice!\n")
            except KeyboardInterrupt:
                print("\nThanks for playing!")
                exit()

    def _handle_dicecheck(self):
        print(self.roll_prompt)
        return self.get_check_result()
    
    def get_check_result(self):
        self._roll_the_dice()
        if self.result >= self.pass_threshold:
            self.check_result = (True, self.high_outcome)
        else:
            self.check_result = (False, self.low_outcome)
        return self.check_result