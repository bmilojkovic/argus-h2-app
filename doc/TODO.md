# Development

## To develop

- Figure out how to make an exe for python
- Change executable file icon
- Main executable checks if there are updates. If yes:
  - Separate executable downloads the new main exe and updates it.
  - New main exe updates the updater
- Add logging to a file so we can collect errors from users

# For later (2.0+)

- Have the backend throttle messages from mod if too many are coming in.
- Add icons and colors to description text (currently we are limited to bold only)
- To get actual values: look at TraitData and TraitLogic. Specifically ExtractValues and SetTraitTextData.
- Some specific keepsake details
  - Add evil eye detail (who killed you)
  - Add blackened fleece detail (current total damage)
- Artificer remaining use count
- Crimson dress current damage bonus.
- Consumables
- Support for Echo

## Need to test

- Improve the test generator:
  - Add hexes
  - Make all generators have better strategies
- Test Apollo legendary with torches - seems to be a different Trait
- Test Dio keepsake - maybe it stays as a different keepsake in followup biomes.
- Make a benchmark for number of messages sent to twitch. Make sure it is below 100/min. Also, add a warning log if we get close.
- Hammers missing legendaries?
  - Melting Swipe, Dual Moonshot, Mirrored Thrasher, Mirrored Ankh, Meltinc Sickle, Trick Knives
  - Hidden Helix, Clean Coil, Melting Helix, Inverted Blaze, Sudden Burst,
  - Dashing Heave, Iron Core, Heaven Splitter, Giga Cleaver, Executioner's Chop, Psychic Whirlwind, Melting Shredder
  - Helheim Charge, Melting Break, Wide Grin, Twisting Crash
  - Melting Cross, Exhaust Riser, Counter Barrage,
- Check Linux
