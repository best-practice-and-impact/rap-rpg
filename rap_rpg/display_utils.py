import textwrap
from questionary import Style

delim = "----------------------------------------"
continue_message = "\nPress enter to continue. "
style = Style([
            ("pointer", "fg:#F46A25 bold"),
            ("selected", "noinherit fg:#F46A25 bold"),
            ("highlighted", "fg:#F46A25 bold"),
            ("answer", "fg:#F46A25 bold")
        ])

def print_options(options):
    i = 1
    for option in options:
        print(f"{i}: {option}")
        i += 1
    return None

def print_long_message(text, wrap = 120):
    for line in textwrap.wrap(textwrap.dedent(text), wrap):
        print(line)