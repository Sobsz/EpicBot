import os
import time
import random
import discord
import asyncio
from difflib import SequenceMatcher

filename         = "database.txt" # i didn't want to put a comment here but it looks weird otherwise so e
learn            = True           # (default: True) disable if you want to keep your database pristine
autosave_delay   = 300            # (default: 300)  you probably don't need to change this tbh
typing_delay     = 0.1            # (default: 0.1)  seconds per character, set to 0 to turn off
typing_delay_max = 5              # (default: 5)    maximum delay
token            = "INSERT_TOKEN_HERE" # you need to put your discord bot token here, look it up
admin_ids        = []             # put your and your friends' ids (in quotes) here, you can check them using developer mode

last_responses   = dict()
dbot             = discord.Client()

def log(str):
    print("[{}] {}".format(time.strftime("%H:%M:%S"), str))

class chatbot:
    """epic retrieval-based chatbot of minimal complexity (and effectiveness)"""
    
    def __init__(self, responses = [("hello", "hi", 0)]):
        self.responses = responses
        self.needs_saving = False

    def clean(self, s):
        stripped = s.strip().translate(str.maketrans("", "", ".,?!:;'\"()*_")).lower()
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
        return random.choice(best_responses)

    def learn(self, query, response, author):
        self.responses.append((self.clean(query), response, author))
        self.needs_saving = True

    def save(self, filename):
        if self.needs_saving == True:
            log("Saving " + str(len(self.responses)) + " entries...")
            if os.path.exists(filename + ".bak"):
                os.remove(filename + ".bak")
            if os.path.exists(filename):
                os.rename(filename, filename + ".bak")
            with open(filename, "w") as f:
                f.write(repr(self.responses))
                f.close()
                log("Successfully saved database!")
            self.needs_saving = False
            return True
        else:
            return False

@asyncio.coroutine
def autosave():
    while not dbot.is_closed:
        yield from asyncio.sleep(autosave_delay)
        cbot.save("dab.txt")
 
@dbot.event
@asyncio.coroutine
def on_ready():
    log("Successfully logged in as: " + dbot.user.name + "#" + dbot.user.discriminator + " (" + dbot.user.id + ")")
    log("Let the chaos begin!")

@dbot.event
@asyncio.coroutine
def on_message(message):
    if message.author.id != dbot.user.id:
        if message.content.startswith("&"):
            if message.author.id in admin_ids:
                if message.content[1:] == "!COUNT":
                    yield from dbot.send_message(message.channel, "current entry count: " + len(dbot.responses))
                elif message.content[1:] == "!SAVE":
                    yield from dbot.send_message(message.channel, "ok, saving...")
                    if dbot.save():
                        yield from dbot.send_message(message.channel, "saved")
                    else:
                        yield from dbot.send_message(message.channel, "actually nevermind there's no need")
                elif message.content[1:] == "!CEASE":
                    log(message.author.name + "#" + message.author.discriminator + " (" + message.author.id + ") has requested ceasure!")
                    log("Goodbye, cruel world!")
                    quit()
            else:
                query = message.content[1:]
                response = cbot.respond(query)

                if typing_delay > 0:
                    yield from dbot.send_typing(message.channel)
                    yield from asyncio.sleep(min(len(response) * typing_delay, typing_delay_max))
                
                yield from dbot.send_message(message.channel, response)
            
                if learn:
                    if message.channel.id not in last_responses:
                        last_responses[message.channel.id] = ("", 0)
                    cbot.learn(last_responses[message.channel.id][0], query, message.author.id)
                    last_responses[message.channel.id] = (response, time.time())
            
                log("[" + message.server.name + " #" + message.channel.name + "] " + message.author.name + "#" + message.author.discriminator + ": " + query)
                log("[" + message.server.name + " #" + message.channel.name + "] " + "EpicBot: " + response)
        
log("EpicBot v6.2.1-discord - made by zsboS#8977")
log("Loading database...")
try:
    file = open(filename)
    if os.path.getsize(filename) == 0:
        raise IOError
    cbot = chatbot(eval(file.read()))
    file.close()
    log("Successfully loaded " + str(len(cbot.responses)) + " entries.")
except IOError:
    log("Database does not exist, loading backup...")
    try:
        file = open(filename + ".bak")
        if os.path.getsize(filename + ".bak") == 0:
            raise IOError
        cbot = chatbot(eval(file.read()))
        file.close()
        log("Successfully loaded " + str(len(cbot.responses)) + " entries.")
    except IOError:
        log("Backup does not exist, creating new database......")
        cbot = chatbot()
        cbot.save(filename)
        log("Successfully created database.")
    except ValueError:
        log("Backup may be corrupt! Please remove or rename the " + filename + ".bak file, then restart.")
        input("Press Enter to continue...")
        exit()
except ValueError:
    log("Database may be corrupt! Please remove or rename the " + filename + " file, then restart.")
    input("Press Enter to continue...")
    exit()

log("Connecting to Discord...")
dbot.loop.create_task(autosave())
dbot.run(token)
