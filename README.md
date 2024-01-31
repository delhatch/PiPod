# PiPod
<p>From https://github.com/delhatch/PiPod_Zero2W</p>
<p>I am implementing a major overhaul of the GUI functions to operate more like the Sony NWZ-A17. This repository is to hold the new GUI, while still keeping the other project as a stand-alone working version.</p>
<p>The idea is that you could copy these files directly over to the PiPod_Zero2W project to implement this new way to operate the device.</p>
<H3>Original PiPod UI Scheme</H3>
<p>In the original PiPod project, the user would select a song track (or artist, or album) and then push it onto the song que.</p>
<p>The user can continue to scroll around, pushing tracks onto the que stack. The PiPod plays the tracks in the que.</p>
<H3>New PiPod UI Scheme</H3>
<p>This repository holds the code to implement a scheme where the user selects a song playing/selection <b>algorithm</b>, and the PiPod fills the que according to the user's wishes.</p>
<ul>
  <li>For example, the user selects "songs, in random sequence" and that is how the songs are played (how the que is filled).</li>
  <li>Or, "songs, sequentially" and the que is filled with all of the song tracks in alphabetical order.</li>
</ul>
