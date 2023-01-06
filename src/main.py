import csv
import random
import firebase_admin
from firebase_admin import credentials, firestore


# multConst = 1987654787.8379

with open("input.csv", "r") as f:
    raw = csv.reader(f)
    keys = next(raw)
    data = [dict(zip(keys, values)) for values in raw]

    idList = []
    for x in data:
        # Generate unique UUID
        uuid = str(random.randrange(10000000, 99999999))
        while True:
            if idList.count(uuid) > 0:
                uuid = str(random.randrange(10000000, 99999999))
            else:
                break

        idList.append(uuid)
        # Add a new key for ID
        x.update(id=uuid)
    
