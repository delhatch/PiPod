import csv
import random
import string

alphaList = list(string.ascii_uppercase)[:]

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

    def escape(self):
        self.menuDict["selectedItem"] = 0
        if self.menuDict["history"]:  # check if history is empty
            self.menuDict["current"] = self.menuDict["history"][-1::][0]
            self.menuDict["history"].pop()
        else:
            self.menuDict["current"] = "musicController"
        return None

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
        print("Left. Screen =", self.menuDict["current"])
        if self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs":  # move to previous letter in the alphabet
            #self.menuDict["Queue"].append(self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])
            songInfo = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            #songTitle = songInfo[3]
            # Get first letter of selected song.
            firstL = songInfo[3][0]
            # Now scan up until find a song who's first letter is smaller than this one. Save that letter.
            if (firstL in alphaList) and (firstL != 'A') and (self.menuDict["selectedItem"] != 0):
                nextL = chr(ord(firstL) - 1)
                #print("Want to find first song in list that starts with the letter", nextL)
                # Find index of the first song that starts with a letter LESS THAN this one
                index = self.menuDict["selectedItem"]
                index -= 1
                nextSong = self.menuDict[self.menuDict["current"]][index]
                nextSongFirstL = nextSong[3][0]
                while( nextSongFirstL >= nextL ):
                    index -= 1
                    nextSong = self.menuDict[self.menuDict["current"]][index]
                    nextSongFirstL = nextSong[3][0]
                #print("Out of first loop at song",nextSong)
                self.menuDict["selectedItem"] = index + 1
            else:
                # Selected song title did not start with a letter in B-Z. So just go to top of list.
                self.menuDict["selectedItem"] = 0
        else:
            self.escape()
        return "updateList"

    def right(self):
        print("Right. Screen =", self.menuDict["current"])
        if self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs":  # move to next letter in the alphabet
            self.menuDict["Queue"].append(self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])
            songInfo = self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]]
            #songTitle = songInfo[3]
            # Get first letter of selected song.
            firstL = songInfo[3][0]
            # Increment to next letter.
            if (firstL in alphaList) and (firstL != 'Z'):
                nextL = chr(ord(firstL) + 1)
                #print("NextL =", nextL)
                # Find index of the first song that starts with that letter, or greater.
                index = self.menuDict["selectedItem"]
                index += 1
                nextSong = self.menuDict[self.menuDict["current"]][index]
                nextSongFirstL = nextSong[3][0]
                while( nextSongFirstL <= firstL ):
                    index += 1
                    nextSong = self.menuDict[self.menuDict["current"]][index]
                    nextSongFirstL = nextSong[3][0]
                self.menuDict["selectedItem"] = index
            elif ( firstL != 'Z'):
                # Selected song title did not start with a letter in A-Z. So just go to first 'A' song.
                index = self.menuDict["selectedItem"]
                index += 1
                nextSong = self.menuDict[self.menuDict["current"]][index]
                nextSongFirstL = nextSong[3][0]
                while( nextSongFirstL != 'A' ):
                    index += 1
                    nextSong = self.menuDict[self.menuDict["current"]][index]
                    nextSongFirstL = nextSong[3][0]
                self.menuDict["selectedItem"] = index
        elif self.menuDict["current"] == "Artists":  # move songs by the selected artist to queue
            for item in self.menuDict["Songs"]:
                if item[1] == self.menuDict["Artists"][self.menuDict["selectedItem"]]:
                    self.menuDict["Queue"].append(item)
        elif self.menuDict["current"] == "Albums":  # move songs on the selected album to queue
            for item in self.menuDict["Songs"]:
                if item[2] == self.menuDict["Albums"][self.menuDict["selectedItem"]]:
                    self.menuDict["Queue"].append(item)

        return "updateList"

    def gotomenu(self):
        if self.menuDict["current"] == "musicController":
            self.menuDict["selectedItem"] = 0
            self.menuDict["current"] = "Main"
        return None

    def select(self, playMode):
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

        elif self.menuDict["current"] == "Genres":
            tempList = []
            for item in self.menuDict["Songs"]:
                if item[4] == self.menuDict["Genres"][self.menuDict["selectedItem"]]:
                    tempList.append(item)
            self.menuDict["list"] = tempList
            self.menuDict["current"] = "list"
            self.menuDict["selectedItem"] = 0

        elif self.menuDict["current"] == "Queue":
            if self.menuDict["Queue"]:
                return "playAtIndex"

        elif self.menuDict["current"] == "list" or self.menuDict["current"] == "Songs":
            if self.menuDict["Queue"]:   # If Que is NOT empty
                for item in list(self.menuDict[self.menuDict["current"]]): # Select a list of all the Songs
                    if item not in self.menuDict["Queue"]:  # Push all songs not already in the que, onto the que
                        self.menuDict["Queue"].append(item)
                # Done pushing the songs onto the que.
                self.menuDict["Queue"].remove(self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])  # Remove selected
                self.menuDict["Queue"].insert(0, self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])  # Put selected at first position
            else:
                # Que IS EMPTY. If play mode is NOT Repeat1, then put every song into the play que.
                if( playMode == "Normal" ):
                    tempList = list(self.menuDict[self.menuDict["current"]])
                    indexOfSelected = self.menuDict["selectedItem"]
                    self.menuDict["Queue"] = tempList[indexOfSelected::]
                elif( playMode == "Shuffle" ):
                    tempList = list(self.menuDict[self.menuDict["current"]])
                    self.menuDict["Queue"] = random.sample( tempList, len(tempList) )
                    # Now put the selected song at the beginning of the que, so it plays first.
                    self.menuDict["Queue"].insert(0, self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])
                else:
                    # Play mode is "Repeat1" so put just that song onto the play que. After it plays, main.py will figure it out.
                    self.menuDict["Queue"].insert(0, self.menuDict[self.menuDict["current"]][self.menuDict["selectedItem"]])

                #print("Put Songs on the que. Here's how many:", len(self.menuDict["Queue"]) )
                return "play"

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

        elif self.menuDict["current"] == "Play Mode":
            if self.menuDict["Play Mode"][self.menuDict["selectedItem"]] == "Normal":
                return "Normal"
            elif self.menuDict["Play Mode"][self.menuDict["selectedItem"]] == "Shuffle":
                return "Shuffle"
            elif self.menuDict["Play Mode"][self.menuDict["selectedItem"]] == "Repeat 1 Song":
                return "Repeat1"

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
