import pandas as pd 

df = pd.read_csv('THOR_WWI_CLEAN_NEW_12072016.csv', encoding='cp1252')
print(df.columns)


tag_name = ["UNIT", "BOMBLOAD", "DEPARTURE", "TGTLOCATION", "TGTTYPE", "MSNDATE", "MDS", "NUMBEROFPLANESATTACKING"]
tag_prefix = ["un:", "ld:", "dept:", "tloc:", "ttype:", "dt:", "desig:", "pc:"]

print(df.shape)
df = df.dropna(axis=0, subset=tag_name)
print(df.shape)


