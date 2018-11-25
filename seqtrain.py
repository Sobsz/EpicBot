import os

seq_name       = "sequence.txt" # the sequence you'll be training from 
db_name        = "database.txt" # the database you'll be training to
use_both_sides = True           # if True:  [a, b, c, d] -> [(a, b), (b, c), (c, d)]
                                # if False: [a, b, c, d] -> [(a, b), (c, d)]
                                # basically you should use False if you're trying to make the bot have a certain character (bot's replies in even lines) and false otherwise
def clean(s):
    stripped = s.strip().translate(str.maketrans("", "", ".,?!:;'\"()*_<>")).lower()
    if stripped == "":
        return s
    else:
        return stripped

def learn(query, response):
    if len(response) > 0:
        db.append((clean(query), response))
        global count
        count += 1
        if count%10 == 0:
            print(str(count), end=" ")

print("* EpicBot Sequence Trainer v6.2.1 - made by zsboS#8977")

print("* Loading sequence file...")
try:
    seq_file = open(seq_name)
    seq = [line.strip() for line in seq_file]
    seq_file.close()
    print("* Successfully loaded " + str(len(seq)) + " entries.")
    if len(seq) < 2:
        print("* However, that's not enough for sequence training!")
        print("* Please supply a file with at least 2 lines and try again.")
        input("* Press Enter to continue...")
        exit()
except IOError:
    print("* Sequence file does not exist! Please create a file called " + seq_name + " with the sequence data.")
    input("* Press Enter to continue...")
    exit()

print("* Loading database...")
try:
    db_file = open(db_name)
    if os.path.getsize(db_name) == 0:
        raise IOError
    db = eval(db_file.read())
    db_file.close()
    print("* Successfully loaded " + str(len(db)) + " entries.")
except IOError:
    db = []
    print("* Database does not exist, creating...")
    db_file = open(db_name, "w")
    db_file.write(repr(db))
    db_file.close()
    print("* Successfully created database.")
except ValueError:
    print("* Database may be corrupt! Please remove or rename the " + db_name + " file, then restart.")
    input("* Press Enter to continue...")
    exit()


if use_both_sides:
    print("* Using both sides for training (default mode).")
else:
    print("* Using one side for training (character mode).")

print("* Training...", end = " ")
count = 0
for i in range(0, len(seq) - 1, 2):
    learn(seq[i], seq[i+1])
    if use_both_sides and seq[i+2]:
          learn(seq[i+1], seq[i+2])
print()
print("* Successfully taught " + str(count) + " things!")

print("* Saving...")
db_file = open(db_name, "w")
db_file.write(repr(db))
db_file.close()
print("* Saved!")
print("* ok bye *poof*")
