# apodpy
Python script to fetch the APOD so I can use it as a wallpaper

## Description

* The script downloads the APOD at most once per day
* The APOD changes at midnight (00:00) US/Eastern
* The script saves the original image, a wallpaper version, and a thumbnail in its folder
* It adds references to these to the json manifest from APOD and saves that in the same place
* The last line of output is a reference to the json manifest
* The script will fall back on the most recent manifest it can find
* TODO: easily set aspect ratio of the wallpaper (it's hard coded to 16:9)

## Requires

* pillow
* pytz

