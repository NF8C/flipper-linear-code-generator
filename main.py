# Python implementation 2023 jmr based on the work of Justin_T
# Inspired by AdvJosh and his research
# Linear garage door remotes calculator
# We would love to see it ported to the Flipper

def validate(acceptable_answers, user_input, questions_to_ask, low="n", high="f"):
    """If the user doesn't give an appropriate answer ask again.  Use "int" if an integer is a valid option.
    Example ["int", "c] """
    custom = "f"
    if user_input.lstrip('-').isdigit() and "int" in acceptable_answers:
        user_input = int(user_input)
        if not low.isdigit():
            return user_input

        elif low.isdigit() and high.isdigit():
            low = int(low)
            high = int(high)
            if low <= user_input <= high:
                return user_input
            while user_input <= low or user_input >= high and custom != "c":
                print("{} is not between {} and {}".format(user_input, low, high))
                custom = input("Please enter C to confirm a custom value or N to choose a new number: ")[0].lower()
                return user_input
            else:
                validate(acceptable_answers, input(menu), menu, str(low), str(high))

    else:
        user_input = user_input[0].lower()
        if user_input in acceptable_answers:
            return user_input
        else:
            print("That is not a valid option.")
            validate(acceptable_answers, input(questions_to_ask), questions_to_ask, low, high)


menu = "Is the key being generated to act as a Wireless keypad or remote? k(keypad)/r(remote) "
version = validate(["k", "r"], input(menu), menu)

if version == "r":
    menu = "Enter a facility code. Facility codes are usually between 0 and 15: "
    fc = validate(["int"], input(menu), menu, "0", "15")

    menu = "Enter the transmitter number.  Transmitter numbers are usually between 1 and 65535: "
    tn = validate(["int"], input(menu), menu, "1", "65535")

    menu = "Enter the button number.  The range is usually between 1 and 7.\n  " \
           "The default value is 2 for a single button remote: "
    bn = validate(["int"], input(menu), menu, "1", "7")

else:
    fc = 0
    bn = 1
    menu = "Enter an entry code between 1 and 999999: "
    tn = int(validate(["int"], input(menu), menu, "1", "999999"))

frequency = float(input("Enter the frequency in mHz default 318: "))


# Change the frequency to kHz
frequency = int(frequency * 1000000)

# The formula
dec2hex = (((tn*8)+8388608)+(fc*524288)+bn).to_bytes(8, "big").hex(" ").upper()

text = '''Filetype: Flipper SubGhz Key File
Version: 1.0
Frequency: {}
Preset: FuriHalSubGhzPresetOok650Asyn
Protocol: MegaCode
Bit: 24
Key: {}
'''.format(frequency, str(dec2hex))

print(text)

a = input("Would you like to save this as a file? y/n ").lower()[0]


name = ""
if a == "y":
    name = input("Enter a file name without an extension ex. garage "
                 "or press enter for the default file naming option: ").replace(" ", "_") + "_FC{}_TN{}_BN{}.sub".format(fc, tn, bn)

    try:
        with open(name, 'w') as f:
            f.write(text)
    except FileNotFoundError:
        print("Error creating the file.")


