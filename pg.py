import json

for i in ("quick.json", "endless.json", "classic.jcon"):
    with open(i, "w") as file:
        json.dump(dict(), file)