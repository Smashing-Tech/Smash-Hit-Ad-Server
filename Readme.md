# Smash Hit Ad Server 

This is a custom reimplementation of the Smash Hit ad server that can serve ads to properly modified clients.

## Running

  1. Configure the ad server in `adserver_config.json` (if not using default):
    * Add the `revision` property (integer number) **OR** set `forceupdate` to `true`.
    * Set the name of the folder for the adverts (defaults to `default` if not added).
  2. Create new adverts (if not using defaults):
    * Create a png image and put it in `{folder}/ads.png`.
    * Create a UI XML file and put it in `{folder}/ads.xml`.
    * **Note**: You can refer to the examples in the `examples` folder.
  3. Run the server using `python ./adserver.py`.

## Configuring clients

To configure clients, you need to remove anti-tamper protection from the `lib{GAME NAME}.so` files, then find and replace the string `http://mediocre.se/smashhit/content/` with the string of your webserver name.

**Note**: The name string can't be longer than the exsiting string and must end with a `NUL` byte.

## Notes

  * The hardest part is more likely to be modifying the clients to work.
  * You can set `SERVER_PORT` in `adsever.py` to the port you want to use. It is `8000` by default.
  * This could also theoretically serve ads to modified Beyondium and PinOut clients since they use the same ad server.
  * You can edit the configuration without restarting the server and it will be used.
