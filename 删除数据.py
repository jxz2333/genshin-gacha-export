import os
names=os.listdir()
for i in names:
    if 'gacha' in i and 'exe' not in i:
        print(i)
        os.remove(i)

