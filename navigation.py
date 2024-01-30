import csv

class menu():
    menuDict = {
        "selectedItem": 0,
        "Main": ["Songs", "Albums","Artists","Genres","Play Mode","Settings"],
        "Songs": [],
        "Artists": [],
        "Albums": [],
        "Genres": [],
        "Play Mode":["Normal","Shuffle","Repeat 1 Song"],
        "Settings": ["Turn EQ On","Turn EQ Off","Sleep", "Shutdown", "Reboot", "Update library"],
        "current": "musicController",
        "Queue": [],
        "history": [],
    }

    def __init__(self):
        pass

    def up(self):
        if self.menuDict["selectedItem"] > 0:
            self.menuDict["selectedItem"] -= 1
        return None

    def down(self):
        if self.menuDict["current"] == "Queue" and self.menuDict["selectedItem"] < len(self.menuDict[self.menuDict["current"]]):
            self.menuDict["selectedItem"] += 1
        elif self.menuDict["selectedItem"] < len(self.menuDict[self.menuDict["current"]]) - 1:
            self.menuDict["selectedItem"] += 1
        return None

    def left(self):
        self.menuDict["selectedItem"] = 0
        if self.menuDict["history"]:  # check if history is empty
            self.menuDict["current"] = self.menuDict["history"][-1::][0]
            self.menuDict["history"].pop()
        else:
            self.menuDict["current"] = "musicController"
        return None

    def right(self):
        if self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs":  # move selected item to queue
            self.menuDict["Queue"].append(menu[menu["current"]][self.menuDict["selectedItem"]])
        elif self.menuDict["current"] == "Artists":  # move selected artist to queue
            for item in self.menuDict["Songs"]:
                if item[1] == self.menuDict["Artists"][self.menuDict["selectedItem"]]:
                    self.menuDict["Queue"].append(item)
        elif self.menuDict["current"] == "Albums":  # move selected album to queue
            for item in self.menuDict["Songs"]:
                if item[2] == self.menuDict["Albums"][self.menuDict["selectedItem"]]:
                    self.menuDict["Queue"].append(item)

        return "updateList"

    def gotomenu(self):
        if self.menuDict["current"] == "musicController":
            self.menuDict["selectedItem"] = 0
            self.menuDict["current"] = "Main"
        return None

    def select(self):
        if self.menuDict["current"] == "Artists":
            tempList = []
            for item in self.menuDict["Songs"]:
                if item[1] == self.menuDict["Artists"][self.menuDict["selectedItem"]]:
                    tempList.append(item)
            self.menuDict["list"] = tempList
            self.menuDict["current"] = "list"
            self.menuDict["selectedItem"] = 0

        elif self.menuDict["current"] == "Albums":
            tempList = []
            for item in self.menuDict["Songs"]:
                if item[2] == self.menuDict["Albums"][self.menuDict["selectedItem"]]:
                    tempList.append(item)
            self.menuDict["list"] = tempList
            self.menuDict["current"] = "list"
            self.menuDict["selectedItem"] = 0

        elif self.menuDict["current"] == "Queue":
            if self.menuDict["Queue"]:
                return "playAtIndex"

        elif self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs":
            print("Got here.")
            if self.menuDict["Queue"]:
                for item in list(self.menuDict[self.menuDict["current"]]):
                    if item not in self.menuDict["Queue"]:
                        self.menuDict["Queue"].append(item)
            else:
                self.menuDict["Queue"] = list(
                    self.menuDict[self.menuDict["current"]])  # copy the list where the song is selected to the queue
                print("Put Songs on the que.")
                return "play"
            self.menuDict["Queue"].remove(self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])  # Remove selected
            self.menuDict["Queue"].insert(0, self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])  # Put selected at first position

        elif self.menuDict["current"] == "Settings":
            if self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Update library":
                return "updateLibrary"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Sleep":
                return "toggleSleep"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Shutdown":
                return "shutdown"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Reboot":
                return "reboot"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Turn EQ On":
                return "EQOn"
            elif self.menuDict["Settings"][self.menuDict["selectedItem"]] == "Turn EQ Off":
                return "EQOff"

        else:
            if self.menuDict[self.menuDict["current"]]:  # check if empty
                self.menuDict["history"].append(self.menuDict["current"])  # update history
                self.menuDict["current"] = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]  # go to next menu
                #print(self.menuDict["current"])
            self.menuDict["selectedItem"] = 0

        return None

    def loadMetadata(self):
        file = open("info.csv", "rt")
        self.menuDict["Artists"] = []
        self.menuDict["Albums"] = []
        self.menuDict["Songs"] = []
        self.menuDict["Genres"] = []
        metadata = []
        try:
            reader = csv.reader(file)
            for row in reader:
                artistClear = row[1].lstrip().lower().title()
                albumClear = row[2].lstrip().lower().title()
                genreClear = row[4].lstrip().lower().title()
                if artistClear is not "":
                    if artistClear not in self.menuDict["Artists"]:
                        self.menuDict["Artists"].append(artistClear)
                if albumClear is not "":
                    if albumClear not in self.menuDict["Albums"]:
                        self.menuDict["Albums"].append(albumClear)
                if genreClear is not "":
                    if genreClear not in self.menuDict["Genres"]:
                        self.menuDict["Genres"].append(genreClear)
                if row[3].lstrip() is not "":
                    metadata.append(
                        [row[0], artistClear, albumClear, row[3].lstrip(), genreClear])  # [filename, artist, album, title, genre]
        finally:
            file.close()

        self.menuDict["Artists"].sort()
        self.menuDict["Albums"].sort()
        self.menuDict["Genres"].sort()
        self.menuDict["Songs"] = sorted(metadata, key=lambda meta: meta[3])
