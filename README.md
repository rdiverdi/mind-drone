# mind-drone

Memes.

## Using the Code

1. muse-io
  - sorry, just install it
  - run `muse-io --lsl-eeg eeg --device <device MAC address>`
    - this runs muse-io in lsl mode (and names the eeg stream eeg)

2. run `python get_muse_data.py` from this folder
  - eeg data should now be published on ros topic `/eeg`
