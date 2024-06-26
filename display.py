import pygame
import os
import time

backgroundColor = (0, 0, 0)  # global
primaryColor = (255, 255, 255)  # global
secondaryColor = (100, 100, 255)  # global
# Create a pointer to the 2.2" LCD frame buffer. Note: No need to ever f.close() it.
f=open("/dev/fb1","wb")
#f=open("/dev/fb0","wb")
noRefresh = False # If True, the screen will NOT refresh.
displayPlayMode = "Normal"

class view():
    def __init__(self):
        os.putenv('SDL_FBDEV', '/dev/fb1')  # Route the output to framebuffer 1 (TFT display)
        #os.putenv('SDL_FBDEV', '/dev/fb0') 
        surfaceSize=(320,240)
        pygame.init()
        self.lcd=pygame.Surface(surfaceSize)
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.dispWidth, self.dispHeight = (320,240)
        self.font = pygame.font.Font("/home/drh/PiPod_Zero2W/Sofware/TerminusTTF-4.46.0.ttf", 18)
        self.noRefresh = False
        self.displayPlayMode = "Normal"

    def setPlayMode(self, PlayMode):
        self.displayPlayMode = PlayMode

    def update(self, status, menuDict, songMetadata):
        # Note: menuDict is navigate.py's ENTIRE menuDict structure, including ["Songs"][].
        if menuDict["current"] == "musicController":
            self.musicController(
            menuDict["selectedItem"],
            status[1],
            status[0],
            songMetadata["currentSong"],
            songMetadata["currentTime"],
            songMetadata["songLength"],
            songMetadata["volume"],
            len(songMetadata["playlist"]),
            songMetadata["index"]
            )
        elif menuDict["current"] == "Songs":
            # menuDict["selectedItem"] is the index of the item on the list that should be centered and highlighted.
            self.listView( list(map(lambda x: x[3], menuDict[menuDict["current"]])), menuDict["selectedItem"] )
        elif menuDict["current"] == "Queue":
            self.listView(["Clear queue"] + list(map(lambda x: x[3], menuDict[menuDict["current"]])), menuDict["selectedItem"] )
        elif menuDict["current"] == "list":  # This means I am looking at a list of Artists/Albums/Genres.
            self.listView(list(map(lambda x: x[3], menuDict["list"])), menuDict["selectedItem"] )
        else:
            self.listView(menuDict[menuDict["current"]], menuDict["selectedItem"] )

        return None

    def refresh(self):
        if self.noRefresh == False:
            f.seek(0)
            f.write(self.lcd.convert(16,0).get_buffer())

    def setNoRefresh(self):
        self.noRefresh = True

    def setDoRefresh(self):
        self.noRefresh = False

    def clear(self):
        self.lcd.fill(backgroundColor)

    def popUp(self, text):
        self.lcd.fill(backgroundColor)
        text = self.font.render(text, True, primaryColor)
        self.lcd.blit(text, ((self.dispWidth - text.get_width()) / 2, (self.dispHeight - text.get_height()) / 2))
        self.refresh()

    def listView(self, menu, selectedItem):
        self.clear()
        index = 0
        marginTop = (self.dispHeight - 9) / 2 - (21 * selectedItem)  # text height 18/2=9
        marginLeft = 10
        marginTop += 21 * (selectedItem - 12 if selectedItem > 12 else 0)
        index += (selectedItem - 12 if selectedItem > 12 else 0)
        for item in menu[
                    selectedItem - 12 if selectedItem > 12 else 0:selectedItem + 12]:  # I'm sorry, if selected item is more then 4 start slicing the list
            if ( item == "Normal") and ( self.displayPlayMode == "Normal" ):
                    item = '\u2192' + " Normal " + '\u2190'
            elif ( item == "Shuffle") and ( self.displayPlayMode == "Shuffle" ):
                    item = '\u2192' + " Shuffle " + '\u2190'
            elif ( item == "Repeat 1 Song") and ( self.displayPlayMode == "Repeat1" ):
                    item = '\u2192' + " Repeat 1 Song " + '\u2190'
            if index == selectedItem:
                text = self.font.render(item, True, secondaryColor)
            else:
                text = self.font.render(item, True, primaryColor)
            self.lcd.blit(text, (marginLeft, marginTop))
            marginTop += 21
            index += 1

    def musicController(self, selectedItem, batLevel, chargeStatus, \
                        currentSong, currentTime, songLength, volume, queLength, queIndex):
        self.clear()

        # Status bar
        volumeText = self.font.render(str(volume) + "%", True, primaryColor)
        self.lcd.blit(volumeText, (10, 1))

        if currentSong[1] == "":  # If there is no song being played, show 0/0
            queText = self.font.render(str(queIndex) + "/" + str(queLength-1), True, primaryColor)
        else:
            queText = self.font.render(str(queIndex+1) + "/" + str(queLength), True, primaryColor)
        self.lcd.blit(queText, (140, 1))

        chargeText = self.font.render(batLevel, True, primaryColor)
        self.lcd.blit(chargeText, (self.dispWidth - chargeText.get_width() - 10, 1))

        pygame.draw.line(self.lcd, primaryColor, (0, 20), (self.dispWidth, 20))

        # Current song information
        if currentSong:
            artist = self.font.render(currentSong[1], True, primaryColor)
            #album = self.font.render(currentSong[2], True, primaryColor)
            title = self.font.render(currentSong[3], True, primaryColor)
            #genre = self.font.render(currentSong[4], True, primaryColor)
            #print(currentSong[4])
            self.lcd.blit(title, (10, 30))
            self.lcd.blit(artist, (10, 51))
            #self.lcd.blit(album, (10, 72))
            #self.lcd.blit(genre, (10, 93))

        # Time bar
        pygame.draw.rect(self.lcd, primaryColor, (10, self.dispHeight - 18, self.dispWidth - 20, 15), 1)

        if songLength > 0:
            progress = round((self.dispWidth - 20) * currentTime / songLength)
            pygame.draw.rect(self.lcd, primaryColor, (10, self.dispHeight - 18, progress, 15))
            currentTimeText = self.font.render(
                "{0:02d}:{1:02d} / ".format(int(currentTime / 1000 / 60), round(currentTime / 1000 % 60)), True,
                primaryColor)
            songLengthText = self.font.render(
                "{0:02d}:{1:02d}".format(int(songLength / 1000 / 60), round(songLength / 1000 % 60)), True,
                primaryColor)
        else:
            currentTimeText = self.font.render("00:00 / ", True, primaryColor)
            songLengthText = self.font.render("00:00", True, primaryColor)

        self.lcd.blit(currentTimeText, (10, self.dispHeight - 39))
        self.lcd.blit(songLengthText, (10 + currentTimeText.get_width(), self.dispHeight - 39))
