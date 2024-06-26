# PiPod
<p>From https://github.com/delhatch/PiPod_Zero2W</p>
<p>I am implementing a major overhaul of the GUI functions to operate more like the Sony NWZ-A17. This repository is to hold the new GUI, while still keeping the other project as a stand-alone working version.</p>
<p>Just clone the <b>PiPod_Zero2W</b> project, then over-write the files from this project to directly over-write the corresponding files in the <b>PiPod_Zero2W</b> project.</p>
<H3>Original PiPod UI Scheme</H3>
<p>In the original PiPod project, the user would select a song track (or artist, or album) and then push it onto the song que.</p>
<p>The user can continue to scroll around, pushing tracks onto the que stack. The PiPod plays the tracks in the que.</p>
<H3>New PiPod UI Scheme</H3>
<p>This repository holds the code to implement a scheme where the user selects a song playing/selection <b>algorithm</b>, and the PiPod fills the que according to the user's wishes.</p>
<ul>
  <li>For example, the user selects "songs, in random sequence" and that is how the songs are played (how the que is filled).</li>
  <li>Or, "songs, sequentially" and the que is filled with all of the song tracks in alphabetical order.</li>
</ul>
<p>Another key change is that while scrolling a list of Songs (or Artists, or Albums), the right (and left) arrow keys move to the next (or previous) song that starts with the next (or previous) letter.</p>
<ul>
  <li>So by clicking the right arrow key, if you are looking at songs that start with 'A', it jumps to songs that start with 'B'. Much faster scrolling through long lists!</li>
</ul>
<H3>Minor Structural Change</H3>
<p>For handling button presses, changed from the Adafruit GPIO library to the Adafruit Blinka library. See device.py</p>
<H3>Known Bugs</H3>
<ul>
  <li>After doing a Library Update, the playback que should be cleared. But if done, then cannot play a selected song from a list.</li>
</ul>
<H3>Known Annoyances</H3>
<ul>
  <li>After doing "Clear Que" then go back to top screen, pressing play still plays the song, but top screen is blank.</li>
</ul>
