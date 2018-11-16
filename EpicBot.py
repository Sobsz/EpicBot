import os
import random
from difflib import SequenceMatcher

filename = "database.txt"
max_responses = 0
debug = False
bot_goes_first = False   # i recommend leaving this off during the first few phases of training so the bot can learn some greetings
                         # (if you want to teach some manually just leave the "if someone says..." part blank)
class chatbot:
    """epic retrieval-based chatbot of minimal complexity (and effectiveness)"""

    def __init__(self, max_responses = 0, responses = [("hello", "hi")]):
        self.max_responses = max_responses
        self.responses = responses

    def clean(self, s):
        stripped = s.strip().translate(str.maketrans("", "", ".,?!:;'\"()*_")).lower()
        if debug:
            print("# " + stripped)
        if stripped == "":
            return s
        else:
            return stripped
    
    def dist(self, a, b):
        return SequenceMatcher(None, a, b).ratio()
    
    def respond(self, query):
        query_cleaned = self.clean(query)
        temp = [(self.dist(i[0], query_cleaned), i[1]) for i in self.responses]
        best_dist = -1
        best_responses = ["ERROR: IF YOU SEE THIS THEN SOMETHING IS WRONG WITH THE RESPONSE LIST AND THAT IS NOT A GOOD THING"]
        for i in temp:
            if i[0] > best_dist:
                best_dist = i[0]
                best_responses = [i[1]]
            elif i[0] == best_dist:
                best_responses.append(i[1])
        if debug:
            print("# accuracy: " + str(best_dist))
            print("# list: " + str(best_responses))
        return random.choice(best_responses)

    def learn(self, query, response):
        self.responses.append((self.clean(query), response))
        if self.max_responses > 0:
            if len(self.responses) > self.max_responses:
                self.responses.pop(0)

print("* EpicBot v6.2.1 - made by zsboS#8977")
print("* Loading database...")
try:
    file = open(filename)
    if os.path.getsize(filename) == 0:
        raise IOError
    bot = chatbot(max_responses, eval(file.read()))
    file.close()
    print("* Successfully loaded " + str(len(bot.responses)) + " entries.")
except IOError:
    bot = chatbot()
    print("* Database does not exist, creating...")
    file = open(filename, "w")
    file.write(repr(bot.responses))
    file.close()
    print("* Successfully created database.")
except ValueError:
    print("* Database may be corrupt! Please remove or rename the " + filename + " file, then restart.")
    input("* Press Enter to continue...")
    exit()

print("* EpicBot is now ready for your input.")
if bot_goes_first:
    response = bot.respond("")
    print("< " + response)
else:
    response = ""

while True:
    query = input("> ")
    if query:
        if query[0] == "/":
            if query in ("/learn", "/l", "/teach", "/t"):
                print("* If someone says...")
                learn_query = input("> ")
                print("* The bot should respond with...")
                learn_response = input("> ")
                bot.learn(learn_query, learn_response)
                print("* Taught successfully!")
            elif query in ("/save", "/s"):
                print("* Saving " + str(len(bot.responses)) + " entries...")
                file = open(filename, "w")
                file.write(repr(bot.responses))
                file.close()
                if debug:
                    print(repr(bot.responses))
                print("* Successfully saved database!")
            elif query in ("/quit", "/q", "exit", "/e"):
                print("* Are you sure? All unsaved changes will be lost! (Y/N)")
                if input("> ")[0].lower() == "y":
                    print("* Quitting...")
                    quit()
                else:
                    print("* Quit operation cancelled.")
            elif query in ("/count", "/c"):
                print("* Amount of entries: " + str(len(bot.responses)))
            elif query in ("/dump", "/d"):
                print("* " + str(bot.responses))
                print("* Amount of entries: " + str(len(bot.responses)))
            elif query in ("/undo", "/u"):
                print("* Successfully removed:" + str(bot.responses.pop()))
            elif query in ("/help", "/h", "/?"):
                print("* Available commands:")
                print("* /help (/?)      - prints this list")
                print("* /learn (/teach) - lets you teach the bot something manually")
                print("* /undo           - removes the latest response")
                print("* /save           - saves the response database")
                print("* /dump           - outputs the current database along with the entry count")
                print("* /count          - outputs just the entry count")
                print("* /quit (/exit)   - leaves the program")
                print("* You can use the first letter of a command as a shortcut, like so: '/s'")
            else:
                print("* Unknown command! Type /help to list the available commands.")
        else:
            bot.learn(response, query)
            response = bot.respond(query)
            print("< " + response)
