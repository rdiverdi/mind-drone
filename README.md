# mind-drone

Memes.

This is a project for controlling a neato with eye movements. It is in pieces so as to make utilizing subsets of its utility with other code is easier

## Using the Code

1. muse-io
  - sorry, just install it
  - run `muse-io --lsl-eeg eeg --device <device MAC address>`
    - this runs muse-io in lsl mode (and names the eeg stream eeg)

2. pair your computer with the muse headset
  - then put on the muse headset

3. run `python get_muse_data.py` from this folder
  - eeg data should now be published on ros topic `/eeg`
  - follow calibration instructions
    - this is easier if someone reads the instructions out to the person with the muse headset or the screen is eye-level
    - "look left" means that you should quickly look leftward, then quickly back forward to await the next instruction

4. run `python eeg_to_dir.py` from this folder
  - eeg data is now being processed
    - directional output should now be published on ros topic `/dir`

5. run `python neato_control.py`
  - make sure you are connected to the neato
    - for the purposes of these instructions, we will assume you know how to do that

6. look in the directions that you want to neato to go
  - up = increase speed
  - left = increase counterclockwise rotation
  - right = increase clockwise rotation
  - down = stop movement