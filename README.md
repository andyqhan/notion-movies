# notion-movies

This script takes data from folder names (in my case, these folders contain
movies or TV) and adds them to a Notion database (table). In order for the
script to find the lengths of videos, it's necessary to import Phil Harvey's
ExifTool. And, of course, for the script to be able to access your Notion it
requires the Notion API as well as your client key.

The input directory is set with `folder_dir`. It should contain folders with
names of the form `MOVIE_NAME (YEAR) W`, where `MOVIE_NAME` is the name of the movie
(spaces are ok), `YEAR` is the year of the movie, and `W` is an optional value ---
equal to either `w` or absent --- that indicates whether I've watched the movie.

The script also includes a function called `find_tv()` which does the same thing
to television-containing directories as `find_videos()` does to movies, but TV
has a slightly different format.

I've only tested this on macOS.
