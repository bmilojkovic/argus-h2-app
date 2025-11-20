# How Argus Works

If you wish to dive deeper into how Argus works, you might want to look at two other relevant repositories:

- [Argus Backend](https://github.com/bmilojkovic/argus-h2-backend)
- [Argus Twitch Extension](https://github.com/bmilojkovic/argus-h2-twitch)

The main flow of data from the game to Twitch is as follows:

1. The data is read and assembled from a save file.
2. We parse the raw data on the app and send the relevant parts of it to our backend service.
3. Our backend service does additional parsing and data transformation to prepare everything for the frontend. It then uses the Twitch pubsub API to broadcast information to viewers.
4. The Twitch extension receives this broadcast and displays information to viewers.

## Reading the save file

The main execution loop of the app wants to do two things:

- Check if a run save file has changed.
- Parse the file and send the parsed data to our backend service.

### Observing the saves

Most of this is done in [argus_observing.py](../src/argus_observing.py). The `observer_loop` is run in a background thread and every 5 seconds reads the state of the save directory set in the GUI. It notes change times and looks specifically for files that end with `_Temp.sav` because that denotes saves made during the run (as opposed to non-`_Temp` files which are made between runs). If any one of those files has changed, we can assume that a run is in progress and we want to send it to twitch.

We use [Hades Saves Extractor](https://github.com/TheNormalnij/Hades-SavesExtractor) to read the save file and make a temporary .lua file in our directory. That LUA file contains objects that we can parse and pull all the data we need. We then use the [slpp](https://pypi.org/project/SLPP/) library to convert the LUA data to a python-friendly form.

### Building data for our backend

The function that does all the object parsing is `parseData` in [argus_parsing.py](../src/argus_parsing.py). It delegates a lot of its logic to other various `argus_parsing_*` modules.

**Step one - building Argus objects that are represented by Traits**

This function goes through all the traits on the current hero to build all the Argus objects that are represented by traits. These are:

- All boons
- Weapons
- Familiars
- Keepsakes
- Hexes
- Chaos curses
- Hammers

That initial loop builds up the following objects for our backend: `boonData`, `extraData`, `weaponData`, `familiarData`, `arcanaData`. The difference between `boonData` and `extraData` is that extra should go under the main panel on the final UI. So keepsakes, hexes, timed boons, etc.

**Step two - non trait data**

There are still things we are interested that are not traits on the hero. Namely, they are:

- Element counts
- Pins (forget-me-nots)
- Vows

We read each of those from their respective global places, mostly outside the `Hero` table. They will form the following objects for our backend: `elementalData`, `pinData`, `vowData`, `arcanaData`.

**Side note: data format**

This is the format in which we represent each object when sending to the backend. You can find examples of full data loadouts in `argus_testing.py`.

- General considerations: we use space (` `) to separate items in a list. We use two semicolons (`;;`) to separate properties within items. In most cases lists will look like: `rarity1;;name1 rarity2;;name2`... Values for rarity are taken from the game code, so they are usually `Common`, `Rare`, `Epic`, `Legendary`. Exceptions are noted below. Names are usually the `Name` property inside a trait or other table.
- `boonData`: A list of boons, each having a rarity and name.
- `weaponData`: A single item with rarity and name. Here rarity can include `Perfect` as well.
- `familiarData`: Familiar name, followed by exactly two traits. The two traits need to be the ones that get leveled up (in code terms, they have a `Stack` number), excluding the damage traits. A full list of these is available in `util.lua`.
- `extraData`: Same as `boonData`. These just go on the bottom of the UI.
- `pinData`: Up to three boons that should go on the pin tab. No whitespace here, just names separated by `;;`. It is fine to include more than three items here, as well as non-boons. The backend will just keep the first three actual boons it finds in the list.
- `vowData`: A list of vows. They are different from boons in that they have a level isntead of rarity. Levels start at `1`.
- `arcanaData`: Same format as `vowData`.

### Sending to backend

The final step in the main loop is sending to backend via `send_run_data` in [argus_network.py](../src/argus_network.py). We assume that we have a good argus token in our config file at this point. If the token is confirmed by the backend, we perform a POST request to the `/run_info` endpoint of the backend. The endpoint expects the following JSON object:

```
{
  argusProtocolVersion: "2", //we use this protocol number since 1.1.0
  argusToken: token, //the token we got from the config file
  runData: { //all the strings have the same format as described above
    boonData: ...
    weaponData: ...
    familiarData: ...
    extraData: ...
    arcanaData: ...
    elementalData: ...
    pinData: ...
    vowData: ...
  }
}
```

## Connecting the user's Twitch account with Argus

We want to be able to ensure that the user that is playing the game and streaming is one and the same. If we just had say a twitch user id (`X_ID`) as a config parameter somewhere, it would be possible for a troll chatter to simply use the same id in their own game and mess up the data on stream, since that number is public and can be obtained easily.

### Argus Token flow

To solve the above problem, we are asking the mod user to connect their Twitch account to our backend. This is an OAuth2 sequence where the following steps occur:

1. The app opens a browser window at URL `https://id.twitch.tv/oauth2/authorize` which is a Twitch authorization system. We provide the following:

   1. We tell twitch that it should send a one-time authorization code to Argus backend if everything is ok.
   2. We provide a random `state` that we generated and kept.
   3. We say that the scope of authorization is the user ID and profile picture.

2. If the user performs the authorization, Twitch sends a request to the Argus backend with a one-time authorization code. It also tells the backend the `state` variable that was provided.
3. After opening the browser page, the python code continues executing and starts pinging the Argus backend. It tries 60 times (with breaking for 1 sec. between tries) to reach the `/get_argus_token` endpoint. It sends the `state` value as a parameter.
4. At some point, the backend will have received the one-time authorization code from Twitch with the `state` variable. The backend can use the one-time code to retreive the actual Twitch user id (`X_ID`) and profile picture of the person that did the authorization (this is the thing we didn't want to have in a config file). Now the backend responds to the `/get_argus_token` request with a random Argus token that it generates. The backend stores this Argus token paired with the Twitch user ID and profile picture.
5. The python code now stores the received Argus token in its own config file. In the future, python will simply use this Argus token to identify with the backend, and the backend will be certain that the person using this token is indeed the one with the `X_ID` Twitch id.

![Argus Auth flow](ArgusLoginFlow.png)
