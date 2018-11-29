# EpicBot
the epicest laziest retrieval-based-est chatbot ever

basically "make your own cleverbot" except more stupider

epicbot™ is "inspired" by [project charlotte](https://www.reddit.com/r/projectCharlotte/)'s chatbots (tbh i just wanted to flex on 'em neural ni:b::b:as with the least amount of effort possible)

you'll need to save the training data manually by typing `/s` every so often

also `/help` for more wacky commands

you can use `database.txt` as a starting point for your bot but i wouldn't really recommend that tbh

# ALSO THERE'S A DISCORD VERSION NOW
me and someone called "celeri" are working on a public-ish version but that's not gonna happen until she gets a raspberry pi so for now you're gonna need to host it thineself

the code is hecka dirty and undocumented for now (and maybe forever) so just contact me at zsboS#8977 if you're stucc

default chat prefix is `&`, default command prefix is `&!`

current commands for people on the admin list:
- `&!COUNT` - counts the entries
- `&!SAVE` - manual save in case you want to shut down the thing right now
- `&!CEASE` - emergency shutdown

also it adds the user id in every entry for moderation purposes but it should be compatible with regular epicbot anyway

## what's a seqtrain and how use
seqtrain is a script that lets you train the bot from chatlogs and other stuff

simply put your textage in `sequence.txt` and let seqtrain do the thing

by default it trains from both sides of the conversation but you may not want that if you're trying to make your waifu sentient or whatever

if that's the case you'll need to change the `use_both_sides` variable to `False` because commandline arguments are for losers

(also it'll assume the person speaking in the even-numbered lines is what it's supposed to emulate)

if you want to put multiple chatlogs in one database then either use the script multiple times or just add an empty line between the things

```
l
i
k
e

t
h
i
s
```

(or maybe 0 or 2 lines sometimes but that's only if you're doing the waifu thing, just make sure ~~ralsei~~ the soon-to-be bot is still speaking in the even-numbered lines)
