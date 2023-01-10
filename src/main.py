import asyncio
import csv
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Firestore setup
cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def makeFsDoc(dict, uuid):
    doc_ref = db.collection(u'users').document(uuid)
    doc_ref.set(dict)


outList = []


async def parser():
    # Parse CSV into docs
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

            # Add various keys w/ default values for use elsewhere
            x.update(score=0)
            x.update(outBy=0)
            x.update(tagged=[])

            # Add to output list
            ref = {
                "name": x["name"],
                "id": uuid
            }
            outList.append(ref)

            # Add to Firestore
            makeFsDoc(x, uuid)


async def outputWriter():
    # Write to output CSV
    cols = ["name", "id"]
    with open("out.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=cols)
        writer.writeheader
        for data in outList:
            writer.writerow(data)

asyncio.run(parser())
asyncio.run(outputWriter())
