# Python implementation 2023 jmr based on the work of Justin_T
# Inspired by AdvJosh and his research
# Linear garage door remotes calculator
# We would love to see it ported to the Flipper


def validate(acceptable_answers, user_input, questions_to_ask="error", low="n", high="f"):

    if user_input == "":
        user_input = "z"
    elif user_input.lower()[0] == "q":
        return "q"

    custom = "f"

    # It's a number let's validate it
    if user_input.lstrip('-').isdigit() and "int" in acceptable_answers:
        user_input = int(user_input)

        # Create boundaries
        if low.isdigit():
            low = int(low)
        else:
            low = user_input

        if high.isdigit():
            high = int(high)
        else:
            high = int(user_input)

        # Check if the answer is between low and high
        if low <= user_input <= high:
            return user_input

        # Not between low and high
        else:
            print("{} is not between {} and {}".format(user_input, low, high))
            custom = input("Please enter C to confirm a custom value or N to choose a new number: ")[0].lower()
            if custom == "c":
                return user_input
            else:
                user_input = validate(acceptable_answers, input(questions_to_ask), questions_to_ask, str(low), str(high))

    # It's not a number
    else:
        user_input = user_input[0].lower()
        if user_input in acceptable_answers:
            return user_input
        else:
            print("That is not a valid option. {}", acceptable_answers)
            user_input = validate(acceptable_answers, input(questions_to_ask), questions_to_ask, low, high)
    return user_input


def frequency():
    # 281-361 MHz, 378-481 MHz, and 749-962 MHz.

    def error_message():
        print("That was an invalid frequency.")
        frequency()

    x = input("Enter the frequency in mHz default 318: ")
    if x == "q":
        return "q"
    if x == "":
        x = "318"

    try:
        x = float(x)
        if x == 0:
            error_message()
        else:
            # Test the limits
            if 281 <= x <= 361 or 378 <= x <= 481 or 749 <= x <= 962:

                # Change the frequency to kHz
                x = x * 1000000
                return x
            else:
                error_message()
    except ValueError:
        error_message()


def loop(times=1):

    while times > 0:
        menu = "Is the key being generated to act as a Wireless keypad or remote? k(keypad)/r(remote) "
        version = validate(["k", "r"], input(menu), menu)
        if version == "q":
            break

        if version == "r":
            menu = "Enter a facility code. Facility codes are usually between 0 and 15: "
            fc = validate(["int"], input(menu), menu, "0", "15")
            if fc == "q":
                break

            menu = "Enter the transmitter number.  Transmitter numbers are usually between 1 and 65535: "
            tn = validate(["int"], input(menu), menu, "1", "65535")
            if tn == "q":
                break

            menu = "Enter the button number.  The range is usually between 1 and 7.\n  " \
                   "The default value is 2 for a single button remote: "
            bn = validate(["int"], input(menu), menu, "1", "7")
            if bn == "q":
                break

        else:
            fc = 0
            bn = 1
            menu = "Enter an entry code between 1 and 999999: "
            tn = validate(["int"], input(menu), menu, "1", "999999")
            if tn == "q":
                break

        freq = frequency()
        if freq == "q":
            break

        # The formula
        print("tn:{} fc:{} bn:{} frequency:{}".format(tn, fc, bn, freq))
        dec2hex = (((tn*8)+8388608)+(fc*524288)+bn).to_bytes(8, "big").hex(" ").upper()

        text = '''Filetype: Flipper SubGhz Key File
        Version: 1.0
        Frequency: {}
        Preset: FuriHalSubGhzPresetOok650Async
        Protocol: MegaCode
        Bit: 24
        Key: {}
        '''.format(frequency, str(dec2hex))

        print(text)

        a = input("Would you like to save this as a file? y/n ").lower()[0]
        if a == "q":
            break

        name = ""
        if a == "y":
            name = input("Enter a file name without an extension ex. garage "
                      "or press enter for the default file naming option: ").replace(" ", "_") + "_FC{}_TN{}_BN{}.sub".format(fc, tn, bn)

            try:
                with open(name, 'w') as f:
                    f.write(text)
            except FileNotFoundError:
                print("Error creating the file.")


# start the loop
print("Enter Q at any time to quit.")
loop()

