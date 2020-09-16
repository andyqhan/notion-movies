import os
from notion.client import NotionClient
import exiftool
from pathlib import Path

""" This script takes data from folder names (in my case, these folders contain
movies or TV) and adds them to a Notion database (table). In order for the
script to find the lengths of videos, it's necessary to import Phil Harvey's
ExifTool. And, of course, for the script to be able to access your Notion it
requires the Notion API as well as your client key.

The input directory is set with "folder_dir". It should contain folders with
names of the form MOVIE_NAME (YEAR) W, where MOVIE_NAME is the name of the movie
(spaces are ok), YEAR is the year of the movie, and W is an optional value ---
equal to either 'w' or absent --- that indicates whether I've watched the movie.

The script also includes a function called "find_tv()" which does the same thing
to television-containing directories as "find_videos()" does to movies, but TV
has a slightly different format.

I've only tested this on macOS."""

exif_executable = 'LOCATION_OF_EXIFTOOL'

client = NotionClient(
    token_v2 = "YOUR_NOTION_KEY"

folder_dir = 'LOCATION_OF_SOURCE'


def find_videos(path):  # turns folders into tuples of form (name, year, watched)
    video_tuple_list = []
    with os.scandir(path) as videos:
        for video in videos:  # video gives me name of folder, videos is list of video
            if video.name[0] != '.':    # checks it's not a hidden file
                for i in range(len(video.name)):
                    if video.name[i] == '(':
                        open_paren_index = i
                for j in range(len(video.name)):
                    if video.name[j] == ')':
                        closed_paren_index = j

                video_name = video.name[:open_paren_index].strip()
                video_year = video.name[open_paren_index + 1:closed_paren_index].strip()
                watched = video.name[-1] == 'w'

                files_in_video = Path(video).iterdir()  # gives me list of files in movie directory
                for file in files_in_video:     # iterates over all the files in movie directory
                    if file.is_file() and file.parts[-1] != '.DS_Store':
                        for i in range(len(str(file))):
                            if str(file)[i] == '.':
                                filetype_index = i
                        filetype = str(file)[filetype_index+1:]     # determines file ending
                        with exiftool.ExifTool(executable_=exif_executable) as et:  # gets length data
                            metadata = et.get_metadata(str(file))
                            if filetype.lower() == 'mkv':
                                length = metadata['Matroska:Duration']
                            elif filetype.lower() == 'mp4' or filetype.lower() == 'mov' or filetype.lower() == 'm4v':    # mov and mp4 are treated the same
                                length = metadata['QuickTime:Duration']
                            elif filetype.lower() == 'avi':
                                length = metadata['Composite:Duration']

                length = int(length / 60)   # converts length to minutes
                video_tuple = (video_name, video_year, watched, length)
                video_tuple_list.append(video_tuple)
                print(video_tuple)    # verbose adding of tuples

        '''for movie in range(len(video_tuple_list)):  # remove the macos hidden files — might not be needed
            if video_tuple_list[movie][0][0] == '.':
                pop_index = movie
        video_tuple_list.pop(pop_index)'''

    return video_tuple_list


notion_movie_db = client.get_collection_view('NOTION_OUTPUT_LINK')


def add_videos(source, target, video_type):  # where source is the output of find_videos or find_tv, a list of tuples
    for movie in source:
        print("Adding " + str(movie))    # verbose adding of movies
        new_row = target.collection.add_row()
        new_row.title = movie[0]
        new_row.year = movie[1]
        # new_row.watched = movie[2]    # has to be commented out for tv
        new_row.downloaded = True
        # new_row.length = movie[3]     # has to be commented out for tv
        new_row.type = str(video_type)


def find_tv(path):  # turns folders into tuples of form (name, year, watched)
    video_tuple_list = []
    with os.scandir(path) as videos:
        for video in videos:  # video gives me name of folder, videos is list of video
            if video.name[0] != '.':    # checks it's not a hidden file
                for i in range(len(video.name)):
                    if video.name[i] == '(':
                        open_paren_index = i
                for j in range(len(video.name)):
                    if video.name[j] == ')':
                        closed_paren_index = j

                video_name = video.name[:open_paren_index].strip()
                video_year = video.name[open_paren_index + 1:closed_paren_index].strip()

                video_tuple = (video_name, video_year)
                video_tuple_list.append(video_tuple)
                print(video_tuple)    # verbose adding of tuples

        '''for movie in range(len(video_tuple_list)):  # remove the macos hidden files — might not be needed
            if video_tuple_list[movie][0][0] == '.':
                pop_index = movie
        video_tuple_list.pop(pop_index)'''

    return video_tuple_list
