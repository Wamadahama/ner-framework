import random

import pandas as pd
import numpy as np

df = pd.read_csv('thor_wwii_data_clean.csv', encoding='cp1252')
print(df.columns)

def p(item):
    print(item)
    exit()


tag_names = [

   ["O-UNIT",
    "I-UNIT",],

    ["O-BOMBLOAD",
    "I-BOMBLOAD",],

   ["O-DEPARTURE",
     "I-DEPARTURE",],

    ["O-tgt_location",
     "I-tgt_location",],

    ["O-tgt_industry",
     "I-tgt_industry",],

    ["O-MSNDATE",
     "I-MSNDATE",],

    ["O-MDS",
     "I-MDS",],

     ["O-NUMBEROFPLANESATTACKING",
      "I-NUMBEROFPLANESATTACKING"],

   # ["O-ENEMYACTION",
   #  "I-ENEMYACTION"]
#    "O"
]

tag_wrappers = [
    ["unit: {} ", "Unit {} ", "{} "],
    ["bl: {} ", "Payload: {}kg ", "{}kg dropped "],
    ["dept: {} ", "{} ", "at {} ", "during {}"],
    ["tloc: {} ", "target {} ", "trgt {} ", "to {} "],
    ["type: {} ", "{} "],
    ["dt: {}", "date {} ", "on {} "],
    ["desig: {} ", "{} "],
    ["pc: {}", "qty: {} "],
   # ["{}"]
   # [""]
]

df = df.dropna(axis=0, subset=[tag[0].replace("O-", "") for tag in tag_names])
#print(df.shape)
#print(df["UNIT"])


messages = []
for i in df.index:
    tags = set(random.choices(range(0, len(tag_names)), k=8))
    message = []
    for tag in tags:
        wrapper = random.choice(tag_wrappers[tag])
        piece = df[tag_names[tag][0].replace("O-", "")][i]
        string = wrapper.format(piece).lower()

        itr = string.split(" ")
        itr = itr[:-1]
        counter = 0

        xtr = []
        for word in itr:
            l = []
            if counter == 0:
                xtr.append([word.format(str(string).strip().replace(",", "")), tag_names[tag][0]])
                counter +=1
            else:
                xtr.append([word.format(str(string).strip().replace(",", "")), tag_names[tag][1]])
        message.append(xtr)
    messages.append(message)

#print("\n".join(messages))
#messages=messages[::-2]
#print(messages[1:3])
with open('ww2_planes.csv', 'w') as f:
    for msg in messages:
        for part in msg:
            for word in part:
                w1= word[0].replace(",", " ")
                f.write(word[0].replace(",", "") + "," + word[1] + "\n")
        f.write("dummy,O\n")
        f.write(",\n")
