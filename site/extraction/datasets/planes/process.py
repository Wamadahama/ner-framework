import random
import pandas as pd 

df = pd.read_csv('THOR_WWI_CLEAN_NEW_12072016.csv', encoding='cp1252')
print(df.columns)


tag_names = [

   ["O-UNIT",
    "I-UNIT",],

    ["O-BOMBLOAD",
    "I-BOMBLOAD",],
    
   ["O-DEPARTURE",
     "I-DEPARTURE",],

    ["O-TGTLOCATION",
     "I-TGTLOCATION",],

    ["O-TGTTYPE",
     "I-TGTTYPE",],

    ["O-MSNDATE",
     "I-MSNDATE",],

    ["O-MDS",
     "I-MDS",],

     ["O-NUMBEROFPLANESATTACKING",
      "I-NUMBEROFPLANESATTACKING"]
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
#    [""]
]

df = df.dropna(axis=0, subset=[tag[0].replace("O-", "") for tag in tag_names])
#print(df.shape)
#print(df["UNIT"])


messages = []
for i in df.index:
    # pick 6 tags and create the tag
    tags = set(random.choices(range(0, len(tag_names)), k=8))
    message = []
    for tag in tags:
        counter = 0
        wrapper = random.choice(tag_wrappers[tag])
        itr = wrapper.split(" ")
        itr = itr[:-1]
        xtr = []
        for word in itr: 
            l = []
            if counter == 0:
                piece = df[tag_names[tag][0].replace("O-", "")][i]
                #print(piece.split(" "))
                #print(len(piece.strip().split(" ")))
                if(len(str(piece).strip().split(" ")) <= 1):
                    xtr.append([word.format(str(piece).lstrip().replace(",", "")), tag_names[tag][0]])
                else:
                    l = [ [w, tag_names[tag][0]] for w in piece.split(" ")]
                    #print(itr)
                    xtr += l
            else:
                piece = df[tag_names[tag][1].replace("I-", "")][i]
                if(len(str(piece).strip().split(" ")) <= 1):
                    xtr.append([word.format(str(piece).lstrip().replace(",", "")), tag_names[tag][1]])
                else:
                    l = [ [w, tag_names[tag][1]] for w in piece.split(" ")]
                    xtr += l
            counter+= 1
            message.append(xtr)
    messages.append(message)

#print("\n".join(messages))
#messages=messages[::-2]


with open('ww1_planes.csv', 'w') as f:
    for msg in messages:
        for part in msg:
            for word in part:
                w1= word[0].replace(",", " ")
                f.write(word[0].replace(",", "") + "," + word[1] + "\n")
        f.write("dummy,O\n")
        f.write(",\n")
