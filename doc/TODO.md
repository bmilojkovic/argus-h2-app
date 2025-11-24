# Development

- Frontend bugs:
  - Arcana and Vows have rarity slightly misaligned
- Backend bugs:
  - Migrate the storage object "twitchIdByArgusToken" to "twitchProfileByArgusToken"

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
- Make a benchmark for number of messages sent to twitch. Make sure it is below 100/min. Also, add a warning log if we get close.
- Check Linux
