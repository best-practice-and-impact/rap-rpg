delim = "----------------------------------------"
continue_message = "Press any key to continue. "

def print_options(options):
    i = 1
    for option in options:
        print(f"{i}: {option}")
        i += 1
    return None