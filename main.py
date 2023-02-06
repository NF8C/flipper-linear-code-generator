# Python implementation 2023 jmr based on the work of Justin_T
# Inspired by AdvJosh and his research
# Linear garage door remotes calculator
# We would love to see it ported to the Flipper

fc = int(input("Enter the facility Code: "))
tn = int(input("Enter the transmitter number ex. 17316: "))
bn = int(input("Enter the button number default is 2 for a single button remote: "))
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

# Create the text for the file
print("Filetype: Flipper SubGhz Key File")
print("Version: 1")
print("Frequency: " + str(frequency))
print("Preset: FuriHalSubGhzPresetOok650Asyn")
print("Protocol: MegaCode")
print("Bit: 24")
print("Key: " + str(dec2hex))

print(text)

a = input("Would you like to save this as a file? y/n ").lower()[0]

if a == "y":
    name = input("Enter a file name without an extension ex. garage: ").replace(" ", "_") + ".sub"

    try:
        with open(name, 'w') as f:
            f.write(text)
    except FileNotFoundError:
        print("Error creating the file.")
