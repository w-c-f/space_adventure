###########################################################################################
# Date: 9 - 26 - 19
# Description: a text based adventure
###########################################################################################
# some notes about this project, how it has developed, what it is now, and what I wanted it to be
# i started out with grander intentions than what the end product has become
# i intended for a richer story, with more items to interact with than exist in the final version
# the items in the central room, compared to those of other rooms, is evidence of this
# i became a bit burned out after some time, but i feel like the product still stands for itself
# there are many places for improvements, one i had in mind was a way to "win" by accessing the
# computer in the officer's room when the power came back on, and calling for help
# in a way i wish i included that, but i didn't

# the comments that are in this file, later on, are a mix of things
# some describe the function of the code, while others are my thoughts at the time, or suggestions to add
# i chose to leave many of them, rather than cleaning up the comments, because i think there is value in them
# i learned much throughout this process, and were i to do it again, i would not have done it the way i did

# finally, this program is best run in the command prompt
# it makes use of ANSI escape codes to output colors to the terminal
# i cannot guarantee that they will work properly on other systems, but my understanding is that they are universal
# this program has been tested in both python 2 and 3

## edit: this version has no color module, so should be fine for any configuration
###########################################################################################
# the blueprint for a room


class Room(object):
    # the constructor
    def __init__(self, name):
        # rooms have a name, exits (e.g., south), exit locations (e.g., to the south is room n),
        # things (e.g., table), thing descriptions (for each thing), and items (things that can
        # be taken into inventory)
        # rooms have a more expository description, returned with look, or l
        self.name = name
        self.exits = []
        self.exit_locations = []
        self.things = []
        self.thing_descriptions = []
        self.items = []
        self.room_description = 0

    # getters and setters for the instance variables
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, value):
        self._exits = value

    @property
    def exit_locations(self):
        return self._exit_locations

    @exit_locations.setter
    def exit_locations(self, value):
        self._exit_locations = value

    @property
    def things(self):
        return self._things

    @things.setter
    def things(self, value):
        self._things = value

    @property
    def thing_descriptions(self):
        return self._thing_descriptions

    @thing_descriptions.setter
    def thing_descriptions(self, value):
        self._thing_descriptions = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def room_description(self):
        return self._room_description

    @room_description.setter
    def room_description(self, value):
        self._room_description = value

    # adds an exit to the room
    # the exit is a string (e.g., north)
    # the room is an instance of a room
    def add_exit(self, exit, room):
        # append the exit and room to the appropriate lists
        self._exits.append(exit)
        self._exit_locations.append(room)

    # adds a thing to the room
    # the thing is a string (e.g., table)
    # the desc is a string that describes the thing (e.g., it is made of wood)
    def add_thing(self, thing, desc=None):
        # append the item and description to the appropriate lists
        self._things.append(thing)
        if desc is None:  # sets default 'not interesting' response
            desc = ("There is nothing particularly noteworthy about the {}.".format(thing))
        self._thing_descriptions.append(desc)

    def del_thing(self, thing):
        # find position of thing, remove it from list of things and its description
        thing_position = self._things.index(thing)
        self._things.pop(thing_position)
        self._thing_descriptions.pop(thing_position)

    # adds a grabbable item to the room
    # the item is a string (e.g., key)
    def add_item(self, item):
        # append the item to the list
        self._items.append(item)

    # removes a grabbable item from the room
    # the item is a string (e.g., key)
    def del_item(self, item):
        # remove the item from the list
        self.items.remove(item)

    # sets extra info about the room, the surroundings.
    def set_room_description(self, description):
        self.room_description = description

    # adds stuff that most rooms have, ceiling, floor, etc.
    def add_bulk_shit(self):
        self.add_thing("up", "A ceiling encloses the room above you. " +
                       "I guess it would be strange if there wasn't any ceiling at all.")
        self.add_thing("ceiling")
        self.add_thing("down", "Tiles line the floor, reminiscent of a hospital.")
        self.add_thing("tiles")
        self.add_thing("floor")
        # in retrospect, if i were to do this again,
        # i would set up a different function for "generic description garbage",
        # so i could add all the generic shit in one line
        # basically look through a list, and if its in that list, return "its not very interesting" or whatever
        # rather than having a mixed list with noteworthy and non-noteworthy items
        # also i'd probably have optional synonyms link to the same thing, like "box and toolbox" both return
        # the same description, rather than having to make two separate variables with those names and identical descs


###########################################################################################
# utility and other things
# blender ANSI escape sequences for on the fly color changing

class bcolor:
    HEADER = ""  # pink
    OKBLUE = ""  # blue
    OKGREEN = ""  # bright green
    WARNING = ""  # yellow
    FAIL = ""  # red
    ENDC = ""  # NO COLOR
    BOLD = ""
    UNDERLINE = ""

## colors disabled in case of problems
###########################################################################################
# creates the rooms


def create_rooms():
    global current_room

    mainroom = Room("Central Room")
    mainten = Room("Maintenance")
    oq = Room("Officer's Quarters")
    ctrl = Room("Control Room")
    airlock = Room("Airlock")
    outside = Room("Space")

    # add shit to main room
    mainroom.add_exit("east", mainten)
    mainroom.add_exit("south", airlock)
    mainroom.add_exit("north", ctrl)
    mainroom.add_exit("west", oq)
    mainroom.set_room_description("The room you woke up in." +
                                  "\nThere are four doors, each labeled. To the north, 'Control Room'. " +
                                  "To the east, 'Maintenance'. To the south, 'Airlock'. " +
                                  "To the west, 'Officers Quarters'." +
                                  "\nIn the center of the room is a table with three chairs," +
                                  " two of which are occupied by other people.")
    mainroom.add_thing("table", "A clean white table, if not for the three empty packets laying on it.")
    mainroom.add_thing("light", "The glow from the bulb gives you an uneasy feeling.")
    mainroom.add_thing("packets", "The three packets are all ripped open. The front of the packet reads: " +
                       "'Potassium Cyanide - 250mg'.")
    mainroom.add_thing("chairs", "Two of the chairs are occupied by people-- the third one you were sitting in.")
    mainroom.add_thing("people", "The people are both slumped over with pallid expressions. They do not respond to you."
                       + "\nThe person nearest you seems to be an Officer of some sort, if their uniform is anything to"
                       + " go by.")
    mainroom.add_thing("uniform", "It's an officer's uniform.")
    mainroom.add_thing("officer", "'Officer Fairbarns' reads the badge pinned on her breast pocket." +
                       " A peculiar key hangs around her neck on a small chain.")
    mainroom.add_thing("doors", "Going in the direction of a door would probably give you a better idea")
    mainroom.add_bulk_shit()
    mainroom.add_item("badge")
    mainroom.add_item("key")
    # maybe just use this key, the officers key, for both the officer quarters and the main console
    # after all, it's secure, she'd need it for both. lock the oq door and need the key for it

    # make nametag needed for officer quarter
    ### changed, use key instead of nametag. so key for final console, and for OQ access
    ### ensures player has key, so if they are able to get key for OQ, they already have it for console
    # color interactable things, like packet, directions, etc

    #########################################ROOM 2, MAINTENANCE#################
    # add shit to room 2
    mainten.add_exit("west", mainroom)
    mainten.set_room_description(
        "A maintenance room. A console is mounted to the wall, with a fusebox beside it.\nA small toolbox sits on the floor.\nTo the west is the Central Room.")
    mainroom.add_bulk_shit()
    mainten.add_thing("console",
                      "This console controls the power to the station. You could" + bcolor.OKBLUE + " use " + bcolor.ENDC + "it to turn the power back on.")
    mainten.add_thing("fusebox", "A wall mounted fusebox. It's electronically locked.")
    mainten.add_thing("toolbox", "A toolbox stocked with an array of useful tools. " +
                                 "You could do all manner of repairs with these.")
    mainten.add_item("tools")
    # make it so console has 4 states, one without anything, one with card but no power, one with power but no card, and one with both
    # maybe make console a room? it's something to interact with. maybe "use" should put you in "console" room?

    ######################################ROOM 3, OFFICER QUARTER############
    # add shit to room 3
    oq.add_exit("east", mainroom)
    oq.set_room_description(
        "There is a desk with a computer monitor on it. \nA keycard is sitting on the desk. "
        "\nOn a table, next to a bed, sits a diary and a small framed photo."
        "\nTo the east is the Central Room.")
    oq.add_bulk_shit()
    oq.add_thing("desk")
    oq.add_thing("monitor", "You see your reflection in the black screen. The monitor isn't powered.")
    oq.add_thing("table")
    oq.add_thing("bed")
    oq.add_thing("photo", "It's a photo of someone else's children. They look like they're having a good time.")
    oq.add_thing("diary", "That's very nosy of you.")
    oq.add_item("keycard")

    ######################################ROOM 4, CONTROL ROOM############
    # add shit to room 4
    ctrl.add_exit("south", mainroom)
    ctrl.set_room_description(
        "A wall to wall window reveals an unparalleled view of Earth, in all of its splendor."
        + "\nBefore the window sits a computer, equipped with countless displays, buttons, and levers."
        + "\nTo the south is the Central Room.")
    ctrl.add_bulk_shit()
    ctrl.add_thing("computer", "Of all the blinking lights, one in particular stands out to you.\n"
                   + "The light pulses three times quickly, three times slowly, then three times quickly again." +
                   "\nOn the side of the computer, a manual is attached by a length of chain.")
    ctrl.add_thing("manual", "The manual is complex, full of diagrams and technical language." +
                   "\nYou find a relevant entry, for an incoming SOS signal." +
                   "\nTO PERFORM A HARD RESET, AN OFFICER WILL " +
                   bcolor.UNDERLINE + "\nINSERT THEIR KEY" + bcolor.ENDC + ", " +
                   bcolor.UNDERLINE + "\nTURN THE KEY" + bcolor.ENDC + ", AND" +
                   bcolor.UNDERLINE + "\nPUSH THE REVEALED BUTTON" + bcolor.ENDC)

    ######################################ROOM 5, AIRLOCK############
    airlock.add_exit("north", mainroom)
    airlock.add_exit("south", outside)
    airlock.set_room_description(
        "Allows for access outside the station. Several empty spacesuits are lined against the wall. "
        "\nA manual airlock separates you from the vacuum of space. "
        "An array of solar panels is visible on the exterior. "
        "\nTo the south is out into space. To the north is the Central Room.")
    airlock.add_thing("spacesuits", "You figure it's in your best interest to take one of these if you're headed out.")
    airlock.add_item("spacesuit")
    ######################################ROOM 6, OUTSIDE############
    # add shit to room 4
    outside.add_exit("north", airlock)
    outside.set_room_description(
        "The view is breathtaking. Vast darkness, peppered with innumerable white dots. You feel very alone out here."
        "\nThere's an array of solar panels mounted on the external body of the station."
        "\nTo the north is the Airlock, leading back into the station.")
    outside.add_thing("panels", "The panels look damaged, but you could likely fix them with the proper tools.")
    outside.add_thing("array", "The panels look damaged, but you could likely fix them with the proper tools.")

    current_room = mainroom


def death():
    print("You slowly lose consciousness as you drift aimlessly in the vacuum of space.\nYou are dead.")

def youre_out():
    print("\n\n\nYou peer out the window to see a hail of missiles plummeting to Earth, "
          "their exhausts fading to pinpoints in the distance."
          "\nA brilliant white flash floods your vision. You blink desperately as your sight slowly returns."
          "\nFireballs erupt across the Earth's surface like a pox."
          "\nSeconds tick by in what feels like an eternity as you idly watch the spectacle."
          "\nThe control room is silent as the the Earth is engulfed in nuclear hellfire.")


def intro():
    print("You stand up from your chair to find yourself in an unfamiliar room." +
          "\nA dim red lamp on the wall just barely illuminates your surroundings." +
          "\nThe eerie silence contrasts with the pounding pain you feel within your head."
          "\nYou should have a" + bcolor.OKBLUE + " look " + bcolor.ENDC + "around.")


# moved room change to here as a function, since it's called multiple times. "dry style coding"
def room_change(noun):
    global response
    global current_room
    # check exits to see if valid
    for i in range(len(current_room.exits)):
        if noun == current_room.exits[i]:
            # CHANGE CURRENT room to the next one
            current_room = current_room.exit_locations[i]
            response = "Entered " + bcolor.OKBLUE + "{}".format(
                current_room.name) + bcolor.ENDC + "\n{}".format(current_room.room_description)
            break


###########################################################################################
# START THE GAME!!!


# binds input() to raw_input() for backwards compatibility in python 3 and 2
# i'd rather learn on 3, but this saves me from dancing between interpreters
try:
    input = raw_input
except NameError:
    pass

inventory = []  # initialize list to store inventory
create_rooms()  # create room objects used in game
power = 0  # the power has to be turned on eventually
consoleUnlocked = 0  # console is locked
oqUnlocked = 0  # officers quarters door locked
panelsFixed = 0  # panels broke
strike = 0  # three strikes and you're out (don't deduct points for this. it's funny in a morbid way)

intro()

while True:

    if current_room is None:
        death()
        break

    print("=" * 30)
    # prints = 30 times
    #    print(status)

    # get player input
    action = input(">")
    action = action.strip().lower()  # sets whatever they enter to lowercase
    # strip removes spaces on left and right

    # check if player wants to quit
    if action in ["quit"]:
        break

    # default value for response if input is unusual
    response = "I don't understand. \ntype <help> for help."

    if action in ["h", "help"]:
        response = "type in 2 words, in <verb> <noun> format. examples:\nlook, go, " \
                   "take" \
            #               "\n<quit> to quit "
    if action in ["inventory", "i"]:
        response = "Inventory:\n{}".format(inventory)

    # check if player typed in 2 words (correct format), like "go east"
    words = action.split()
    # split takes 2 words and turns it into a list of 2 elements

    # returns room description if they enter look without anything else
    if len(words) == 1:
        if action in ["l", "look"]:
            response = (bcolor.OKBLUE + "{}".format(
                current_room.name) + bcolor.ENDC + "\n{}".format(current_room.room_description))

    if len(words) == 2:
        verb = words[0]
        noun = words[1]
        # verb is first element, noun is second element
        # check what verb is in position 1
        if verb == "go":
            response = "invalid exit"
            # check to see if in central room, and deny entry
            if current_room.name == "Central Room" and noun in ["west", "north"]:
                if noun == "west":
                    if oqUnlocked == 0:
                        response = ("The door to the Officer's Quarters won't budge."
                                    " It's locked and needs a key to open it.")
                        # player needs to check body first, so they get the key for the final computer
                    else:
                        room_change(noun)
                elif noun == "north":
                    if power == 0:
                        response = ("The door to the Control Room has an electronic lock."
                                    " It's not opening until the power is back on.")
                    else:
                        room_change(noun)
            elif current_room.name == "Airlock" and noun == "south" and "spacesuit" not in inventory:
                death()
                break
                # don't go outside without a space suit what's wrong with you

            else:
                room_change(noun)  # runs roomchange function
                # kind of a wet solution to call it a few times like this,
                # but i like having rooms in blocks for the go function

        elif verb in ["l", "look"]:
            response = "I don't see what you're talking about."
            # if looking around room, return room description
            if noun in ["around", "room"]:
                response = current_room.room_description

            # check if thing is in room
            for i in range(len(current_room.things)):
                if noun == current_room.things[i] or noun + "s" == current_room.things[i]:
                    # appends an s to noun to check for plurals in the
                    # case of input being singular. saves on duplicating things for singular and plural
                    # if thing is there, respond with description of thing
                    response = current_room.thing_descriptions[i]
                    break

        elif verb == "take":
            response = "That's not a thing you can take."

            # grabbbales is just a single list, not like 2 parts so you dont need to index it with i
            for items in current_room.items:
                if noun == items:
                    # then add element to inventory
                    inventory.append(items)
                    response = "You take the {}.".format(items)
                    current_room.del_item(items)  # remove that item from the room
                    break

        elif verb == "use":
            response = "It doesn't work that way."

            # check if they have the item in inventory they're trying to use
            # perhaps put this at the top of functions, so that others can be run if they do a proper answer
            for items in inventory:
                if noun == items:
                    # if so, prompt for "on what", if they don't respond properly for "on what" then break
                    on_what = input("Use {} on what?\n".format(items))
                    # i'd like to make this discard first word if a 2 word string is entered
                    # like if its "on door" it would discard the on, and just used door
                    # come back and do that if you remember, otherwise it's not super important
                    response = "I don't understand."  # default response for using item on thing
                    if on_what == "console" and noun == "keycard":
                        if consoleUnlocked == 0:
                            consoleUnlocked = 1
                            response = (bcolor.UNDERLINE + "Keycard accepted. Welcome 'Officer Fairbarns'."
                                        + bcolor.ENDC)
                        else:
                            response = "You already have access to the console."
                    elif on_what == "door" and noun == "key" and current_room.name == "Central Room":
                        # open OQ door with key
                        if oqUnlocked == 0:
                            oqUnlocked = 1
                            response = "You unlock the door to the Officer's Quarters with the key."
                        else:
                            response = "The door is already unlocked."
                    elif on_what in ["panels", "panel", "array"] and noun == "tools" and current_room.name == "Space":
                        # if they try to fix the panels, fix em. if they're fixed, let em know that
                        if panelsFixed == 0:
                            response = "You repair the panels. It was actually a lot less difficult than you imagined."
                            current_room.del_thing("array")
                            current_room.del_thing("panels")
                            current_room.add_thing("array", "The panels are in working order.")
                            current_room.add_thing("panels", "The panels are in working order.")
                            panelsFixed = 1
                        else:
                            response = "The panels are already fixed."

            if noun == "console" and current_room.name == "Maintenance":
                response = (
                        bcolor.UNDERLINE + "Welcome, 'Officer Fairbarns'.\nStation power: Online"
                                           "\nOxygen subsystems: Online\n" +
                        "Access to Control Room restored" + bcolor.ENDC)
                if power == 0:
                    response = (
                            bcolor.UNDERLINE + "Station Power Control Console:" + bcolor.ENDC)
                    if panelsFixed == 0 or consoleUnlocked == 0:
                        if panelsFixed == 0:
                            response = (response + bcolor.FAIL + "\nEmergency Low Power mode enabled.\n"
                                        "Significant damage to external solar panel array detected." + bcolor.ENDC)
                        if consoleUnlocked == 0:
                            response = (
                                    response + bcolor.FAIL +
                                    "\nOverride can only be authorized by an Officer.\nPlease insert keycard."
                                    + bcolor.ENDC)
                    else:
                        response = (
                                response + bcolor.UNDERLINE +
                                "\nPrimary power restored. All systems online.\nControl Room door unlocked."
                                + bcolor.ENDC +
                                "\n\nThe silence is broken by the gentle hum of machinery as the lights flicker on.")
                        power = 1

        # this is intentionally not an elif, as the control room sort of takes precedence over other rooms
        # the strikes and checks prevent doing the computer interaction in a weird order
        if current_room.name == "Control Room":
            if verb == "take" and noun == "key" and strike > 0:
                response = "The key is locked in. You can't remove it."
            elif verb in ["use", "insert"] and noun == "key":
                if strike == 0:
                    response = "The key locks into place with a soft click."
                    strike = 1
                elif strike > 0:
                    response = "You've already inserted the key."
            elif verb == "turn" and noun == "key":
                if strike == 0:
                    response = "You've got to insert the key first."
                elif strike == 1:
                    response = "As you turn the key, a panel pops open to reveal a button."
                    strike = 2
                else:
                    response = "You've already turned the key."
            elif verb in ["press","push", "use"] and noun == "button" and strike == 2:
                strike = 3  # this does nothing but i wanted the baseball joke to work
                youre_out()
                break

    print("\n{}".format(response))
