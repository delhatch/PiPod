#!/usr/bin/python3
import playback
import display
import navigation
import device
import pygame
import RPi.GPIO as GPIO

done = False
music = playback.music()
music.enableEQ()
view = display.view()
menu = navigation.menu()
PiPod = device.PiPod()
clock = pygame.time.Clock()

# Updating 6750 files takes 50 seconds
#view.popUp("Updating Library")
#music.updateLibrary()  # This creates the info.csv file by reading every .MP3 file metadata.
menu.loadMetadata()   # This reads the info.csv file
status = PiPod.getStatus()
songMetadata = music.getStatus()

# This timer is used to update the LCD screen, 5 times per second..
displayUpdate = pygame.USEREVENT + 1
pygame.time.set_timer(displayUpdate, 200)

view.update(status, menu.menuDict, songMetadata)

while not done:
    music.loop()    # Checks if song has ended, and starts playing next song on que (if not empty).
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if menu.menuDict["current"] == "musicController":
                    isAsleep = PiPod.toggleSleep()
                    if isAsleep == True:
                        view.setNoRefresh()
                    else:
                        view.setDoRefresh()
                else:
                    action = menu.escape()

            elif event.key == pygame.K_u:
                music.volumeUp()

            elif event.key == pygame.K_d:
                music.volumeDown()

            elif event.key == pygame.K_UP:
                if status[2]:
                    music.volumeUp()
                elif menu.menuDict["current"] == "musicController":
                    menu.gotomenu()
                else:
                    action = menu.up()

            elif event.key == pygame.K_DOWN:
                if status[2]:
                    music.volumeDown()
                elif menu.menuDict["current"] == "musicController":
                    music.backup( 5000 ) # Back up this many milliseconds
                    #music.shuffle()
                    #menu.menuDict["Queue"] = music.playlist
                else:
                    action = menu.down()

            elif event.key == pygame.K_LEFT:
                if status[2] or menu.menuDict["current"] == "musicController":
                    music.prev()
                else:
                    action = menu.left()

            elif event.key == pygame.K_RIGHT:
                if status[2] or menu.menuDict["current"] == "musicController":
                    music.next()
                else:
                    action = menu.right()
                    #if action == "updateList":
                    #    music.updateList(menu.menuDict["Queue"])

            elif event.key == pygame.K_RETURN:
                if status[2] or menu.menuDict["current"] == "musicController":
                    music.playPause()
                else:
                    currentMode = music.getPlaybackMode()
                    action = menu.select( currentMode )
                    if action == "play":
                        music.loadList(menu.menuDict["Queue"])
                        music.play()
                    elif action == "clearQueue":
                        menu.menuDict["Queue"] = []
                        music.clearQueue()
                    elif action == "updateLibrary":
                        view.popUp("Updating Library")
                        music.player.stop
                        music.updateLibrary()  # Re-create the info.csv file
                        menu.loadMetadata()    # Re-read the info.csv file
                        #music.clearQueue()    # TODO? If in, can't play a song after Library update.
                    elif action == "toggleSleep":
                        PiPod.toggleSleep()
                    elif action == "shutdown":
                        view.popUp("Shutdown")
                        while not PiPod.shutdown():
                            pass
                    elif action == "reboot":
                        view.popUp("Rebooting")
                        while not PiPod.reboot():
                            pass
                    elif action == "playAtIndex":
                        if menu.menuDict["selectedItem"] == 0:
                            music.clearQueue()
                            menu.menuDict["Queue"] = []
                        else:
                            music.playAtIndex(menu.menuDict["selectedItem"]-1)
                    elif action == "setSongSelectedItem":
                        # Change menuDict["selectedItem"] so that the currently-playing song is centered on the list.
                        #print("Now change selected item")
                        songList = list( menu.menuDict["Songs"] )
                        thisSong = music.playlist[music.currentSongIndex]
                        #print(thisSong)
                        if thisSong != ['', '', '', '', '']:
                            thisIndex = songList.index( thisSong )
                            #print(thisIndex)
                            menu.setSelectedItem( thisIndex )
                    elif action == "EQOn":
                        music.enableEQ()
                    elif action == "EQOff":
                        music.disableEQ()
                    elif (action == "Normal" or action == "Shuffle" or action == "Repeat1"):
                        view.setPlayMode( action ) # Used to show the current play mode on the "set mode" screen
                        currentMode = music.getPlaybackMode()
                        if( currentMode != action ):
                            music.setPlaybackMode(action)
                            # Now fill the playback que according to the new Playback Mode
                            if action == "Shuffle":
                                music.shuffle()
                            if action == "Normal":
                                music.unshuffle()

        if event.type  == displayUpdate:
            if PiPod.isAsleep() == False:
                #print(menu.menuDict["selectedItem"] )
                status = PiPod.getStatus()         # Reads battery voltage, gets "status[2]" = backlight on/off
                songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist, index of current song
                temp = view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
                #menu.setSelectedItem( temp )
                #print("Got back", temp )
                view.refresh()
        # The next line gets executed every time we check for an event on the que, no matter the event.
        pass
    clock.tick(5)  # Limit the framerate to X FPS, to retain CPU resources

