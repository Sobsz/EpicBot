import os
import time
import random
import discord
import asyncio
from difflib import SequenceMatcher

filename         = "database.txt"      # i didn't want to put a comment here but it looks weird otherwise so e
learn            = True                # (default: True) disable if you want to keep your database pristine
autosave_delay   = 300                 # (default: 300)  you probably don't need to change this tbh
typing_delay     = 0.05                # (default: 0.05) seconds per character, set to 0 to turn off
typing_delay_max = 5                   # (default: 5)    maximum delay
token            = "INSERT_TOKEN_HERE" # you need to put your discord bot token here, look it up
admin_ids        = []                  # put your and your friends' ids (in quotes) here, you can check them using developer mode

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
        cleaned = s.lower().translate(str.maketrans("", "", ".,?!:;'\"()*_[]{}<>")).strip()
        if cleaned == "":
            return s.lower().strip()
        else:
            return cleaned
    
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
        if len(response) > 0:
            self.responses.append((self.clean(query), response.strip(), author))
            self.needs_saving = True

    def save(self, filename):
        if self.needs_saving == True:
            log("Saving " + str(len(self.responses)) + " entries...")
            if os.path.exists(filename + ".bak"):
                os.remove(filename + ".bak")
            if os.path.exists(filename):
                os.rename(filename, filename + ".bak")
            with open(filename, "w", encoding = "utf-8") as f:
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
            log("[" + message.server.name + " #" + message.channel.name + "] " + message.author.name + "#" + message.author.discriminator + ": " + message.content[1:].strip())
            
            if len(message.content) < 2:
                if typing_delay > 0:
                    yield from dbot.send_typing(message.channel)
                    yield from asyncio.sleep(min(len(response) * typing_delay, typing_delay_max))

                query = message.content[1:]
                response = cbot.respond(query)
                    
                yield from dbot.send_message(message.channel, response)
            
                if learn:
                    if message.channel.id not in last_responses:
                        last_responses[message.channel.id] = ("", 0)
                    cbot.learn(last_responses[message.channel.id][0], query, message.author.id)
                    last_responses[message.channel.id] = (response, time.time())
            
                log("[" + message.server.name + " #" + message.channel.name + "] " + "EpicBot: " + response)
            elif message.content[1:].lower() == "!count":
                yield from dbot.send_message(message.channel, "current entry count: " + str(len(cbot.responses)))
            elif message.author.id in admin_ids and message.content[1:].lower == "!save":
                yield from dbot.send_message(message.channel, "ok, saving...")
                if cbot.save(filename):
                    yield from dbot.send_message(message.channel, "saved")
                else:
                    yield from dbot.send_message(message.channel, "actually nevermind there's no need")
            elif message.author.id in admin_ids and message.content[1:] == "!CEASE":
                log(message.author.name + "#" + message.author.discriminator + " (" + message.author.id + ") has requested ceasure!")
                log("Goodbye, cruel world!")
                quit()
            elif message.author.id in admin_ids and message.content[1:].lower == "!cease":
                yield from dbot.send_message(message.channel, "sorry mate, you're gonna wanna use uppercase on that/nsecurity measures, you know")
            elif message.content[1] == "!":
                yield from dbot.send_message(message.channel, "haha no (invalid command or not enough perms)")
            else:
                if typing_delay > 0:
                    yield from dbot.send_typing(message.channel)
                    yield from asyncio.sleep(min(len(response) * typing_delay, typing_delay_max))

                query = message.content[1:]
                response = cbot.respond(query)
                    
                yield from dbot.send_message(message.channel, response)
            
                if learn:
                    if message.channel.id not in last_responses:
                        last_responses[message.channel.id] = ("", 0)
                    cbot.learn(last_responses[message.channel.id][0], query, message.author.id)
                    last_responses[message.channel.id] = (response, time.time())
            
                log("[" + message.server.name + " #" + message.channel.name + "] " + "EpicBot: " + response)
        
log("EpicBot v6.2.1-discord - made by zsboS#8977")
log("Loading database...")
try:
    file = open(filename, "r", encoding = "utf-8")
    if os.path.getsize(filename) == 0:
        raise IOError
    s = file.read()
    s = s[1:] if s.startswith(u"\ufeff") else s
    cbot = chatbot(eval(s))
    file.close()
    log("Successfully loaded " + str(len(cbot.responses)) + " entries.")
except IOError:
    log("Database does not exist, loading backup...")
    try:
        file = open(filename + ".bak", "r", encoding = "utf-8")
        if os.path.getsize(filename + ".bak") == 0:
            raise IOError
        s = file.read()
        s = s[1:] if s.startswith(u"\ufeff") else s
        cbot = chatbot(eval(s))
        file.close()
        log("Successfully loaded " + str(len(cbot.responses)) + " entries.")
    except IOError:
        log("Backup does not exist, creating new database......")
        cbot = chatbot()
        log("Successfully created database.")
    except ValueError:
        log("Backup may be corrupt! Please remove or rename the " + filename + ".bak file, then restart.")
        input("Press Enter to continue...")
        exit()
except ValueError:
    log("Database may be corrupt! Please remove or rename the " + filename + " file, then restart.")
    input("Press Enter to continue...")
    exit()
if s:
    del s

log("Connecting to Discord...")
dbot.loop.create_task(autosave())
dbot.run(token)
