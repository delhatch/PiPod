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

# Updating 6700 files takes 50 seconds
#print("Starting update.")
#music.updateLibrary()  # This creates the info.csv file by reading every .MP3 file metadata.
#print("Done with update")
menu.loadMetadata()   # This reads the info.csv file
status = PiPod.getStatus()
songMetadata = music.getStatus()

# If you want to do a thing periodically (ePaper?), check for this event in the pygame que.
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
                    PiPod.toggleSleep()
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
                    music.shuffle()
                    menu.menuDict["Queue"] = music.playlist
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
                    if action == "updateList":
                        music.updateList(menu.menuDict["Queue"])

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
                        music.player.stop
                        music.updateLibrary()  # Re-create the info.csv file
                        menu.loadMetadata()    # Re-read the info.csv file
                        music.clearQueue()
                    elif action == "toggleSleep":
                        PiPod.toggleSleep()
                    elif action == "shutdown":
                        view.popUp("Shutdown")
                        view.refresh()
                        while not PiPod.shutdown():
                            pass
                    elif action == "reboot":
                        view.popUp("Rebooting")
                        view.refresh()
                        while not PiPod.reboot():
                            pass
                    elif action == "playAtIndex":
                        if menu.menuDict["selectedItem"] == 0:
                            music.clearQueue()
                            menu.menuDict["Queue"] = []
                        else:
                            music.playAtIndex(menu.menuDict["selectedItem"]-1)
                    elif action == "EQOn":
                        music.enableEQ()
                    elif action == "EQOff":
                        music.disableEQ()
                    elif (action == "Normal" or action == "Shuffle" or action == "Repeat1"):
                        currentMode = music.getPlaybackMode()
                        if( currentMode != action ):
                            music.setPlaybackMode(action)
                            # Now fill the playback que according to the new Playback Mode

        if event.type  == displayUpdate:
            status = PiPod.getStatus()         # Reads battery voltage, gets "status[2]" = backlight on/off
            songMetadata = music.getStatus()   # Get song length, how far in, song info, vol, playlist
            view.update(status, menu.menuDict, songMetadata) # Creates the screen and writes to frame buffer
            view.refresh()
        # The next line gets executed every time we check for an event on the que, no matter the event.
        pass
    clock.tick(15)  # Limit the framerate to X FPS, to retain CPU resources

