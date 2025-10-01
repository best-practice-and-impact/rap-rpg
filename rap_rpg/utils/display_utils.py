import textwrap
delim = "----------------------------------------"
continue_message = "\nPress enter to continue. "

def print_options(options):
    i = 1
    for option in options:
        print(f"{i}: {option}")
        i += 1
    return None

def print_long_message(text, wrap = 120):
    for line in textwrap.wrap(textwrap.dedent(text), wrap):
        print(line)