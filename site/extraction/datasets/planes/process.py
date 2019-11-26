import random
import pandas as pd 

df = pd.read_csv('THOR_WWI_CLEAN_NEW_12072016.csv', encoding='cp1252')
print(df.columns)


tag_names = [
    "UNIT",
    "BOMBLOAD",
    "DEPARTURE",
    "TGTLOCATION",
    "TGTTYPE",
    "MSNDATE",
    "MDS",
    "NUMBEROFPLANESATTACKING",
#    "O"
]

tag_wrappers = [
    ["unit: {} ", "Unit {} ", "{} "],
    ["bl: {} ", "Payload:{}kg ", "{}kg dropped "],
    ["dept: {} ", "{} ", "at {} ", "during the {}"],
    ["tloc: {} ", "target {} ", "trgt {} ", "to {} "],
    ["type: {} ", "{} "],
    ["dt: {}", "date {} ", "on {} "],
    ["desig: {} ", "{} "],
    ["pc: {}", "qty: {} "],
#    [""]
]

print(df.shape)
df = df.dropna(axis=0, subset=tag_names)
#print(df.shape)
#print(df["UNIT"])

newline_prob = .38
messages = []
for i in df.index:
    # pick 6 tags and create the tag
    tags = set(random.choices(range(0, len(tag_names)), k=8))
    message = []
    counter = 0
    for tag in tags:
        wrapper = random.choice(tag_wrappers[tag])
        piece = df[tag_names[tag]][i]
            
        if counter == 0:
            message.append([wrapper.format(str(piece).lstrip().replace(",", "")), tag_names[tag]])
        else:
            message.append([wrapper.format(str(piece).strip().replace(",", "")), tag_names[tag]])
        counter+=1
    messages.append(message)

#print("\n".join(messages))

with open('ww1_planes.csv', 'w') as f:
    for message in messages:
        for word in message:
            w1= word[0].replace(",", " ")
            f.write(word[0].replace(",", "") + "," + word[1] + "\n")
        f.write("dummy,O\n")
        f.write(",\n")
