"""
This module contains a class for the calculation of the average number of words
in a song by a particular artist.

It uses the package musicbrainzngs to get a list of the songs of a particular artist.
It uses the ChartLyrics Lyric API to get the lyrics of each song in the above list.

It runs in a CLI 
"""
import requests
import xml.etree.ElementTree as ET
import venv
import argparse
import re
import os
import sys

__app_name__ = "avgWordsSong"
__version__ = "0.1.0"


def activate():
    """Active virtual environment"""
    venv_dir = os.path.join(os.getcwd(), ".venv")
    os.makedirs(venv_dir, exist_ok=True)
    venv.create(venv_dir, with_pip=True)
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        return os.path.join(venv_dir, "Scripts", "activate")
    else: # MacOS and Linux
        return '. "' + os.path.join(venv_dir, "bin", "activate")

def install():
    """Install requirements to a virtual environment"""
    print('Creating virtual environment..')
    os.system('py -3 -m venv .venv')

    print('Installing requirements..')
    os.system(activate() + ' && ' + 'py -m pip install -r requirements.txt') 


def cleanup():
    """Remove virtual environment"""
    print("Cleaning up...")
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        print("Deleting the created Python Virtual Environment...")
        os.system('rmdir .venv /S /Q')
    else:
        print("Deleting the created Python Virtual Environment...")
        os.system('rm -r .venv/')


class CalculateSongWordAverage:
    """
    A class for the calculation of the average number of words
    in a song by a particular artist.
    """
    def __init__(self, artist_name):
         musicbrainzngs.set_useragent(
            "CalculateSongWordAverage", "1.0", contact="s.shillitoe1@ntlworld.com")
         self._artist_name = artist_name
         self._song_list = []
         self._list_song_word_count = []


    def _get_song_list(self):
        """
        This function uses musicbrianzngs to get a list of songs
        by an artist.

        Song titles are cleaned up to remove [] and () and their
        enclosed text from the title. Punctuation is also removed.

        Duplicate song titles are also removed from the list
        """
        try:
            offset = 0
            limit = 100
          
            while True:
                song_result = musicbrainzngs.search_recordings(
                    artistname=self._artist_name, 
                    limit=limit, offset=offset, strict=True)
            
                if song_result:
                    for song in song_result["recording-list"]:
                        song_title = song["title"]
                        #use a regular expression to 'clean up' the song titles
                        #remove [] and () and their enclosed text from song title
                        #using a regular expression
                        song_title = re.sub("[\(\[].*?[\)\]]", "", song_title)
                        #remove punctation and new lines from title
                        song_title = re.sub(r'[^\w\s]','', song_title.replace('\n', " "))
                        #remove leading and trailing white space & convert to lower case
                        song_title = song_title.strip().lower()
                        self._song_list.append(song_title)
                    #increment the offset to get the next 100 song titles
                    offset += limit
                
                #Stop the while loop when there are no more songs to retrieve or
                #after 4 iterations.
                if len(song_result["recording-list"]) == 0 or offset > 400:
                    break
            
            #Remove duplicates from the list
            self._song_list = list(dict.fromkeys(self._song_list))

            if len(self._song_list) == 0:
                print("No song titles found for {}".format(
                                self._artist_name))
            else:
                print("Song list search finished")
        except Exception as e:
            print('Error in function CalculateSongWordAverage._get_song_list: ' + str(e))
    
    
    def find_artist_song_word_average(self):
        """
        Public function that calculates the number of words in a song by an artist
        """
        self._get_song_list()
        self._calculate_song_word_average()


    def _calculate_list_average(self, list_song_words):
        if list_song_words is not None:
            return int(sum(list_song_words) / len(list_song_words))
        else:
            return 0


    def _calculate_song_word_average(self):
        """
        This function finds the number of words in a song and adds that number to 
        a list.

        This list is then used to calculate the number of words in a song by the artist.
        """
        try:
           for song_title in self._song_list:
                number_words = self._get_number_words_in_one_song(song_title)
                print("Processed {} which has {} words".format(song_title, number_words))
                self._list_song_word_count.append(number_words)

           if len(self._list_song_word_count):
                averageNumberWords = self._calculate_list_average(self._list_song_word_count)
                print("The average number of words in a song by {} is {}".format(self._artist_name, averageNumberWords))
           else:
                print("Could not calculated the average number of words in a song by {}".format(self._artist_name))
        except Exception as e:
            print('Error in function CalculateSongWordAverage._calculate_song_word_average: ' + str(e))


    def _word_count(self, lyrics=None):
        """Returns the number of words in a song."""
        try:
            if lyrics is not None:
                word_list = lyrics.split(" ")
                return len(word_list)
            else:
                return 0
        except Exception as e:
            print('Error in function CalculateSongWordAverage._word_count when lyrics={}: '.format(lyrics) + str(e))


    def _get_song_lyrics(self, song_title):
        """
        This function uses the chartlyrics.com webservice to get the lyrics of a song 
        with the title, song_title.

        This webservice returns the song data in XML format
        """
        try:
            url = 'http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist=' \
                + self._artist_name + '&' + 'song=' + song_title

            response = requests.get(url)

            root = ET.fromstring(response.content)
            lyrics = root.find('{http://api.chartlyrics.com/}Lyric').text
            if lyrics:
                #Prepare lyrics for analysis by removing punctuation & replacing newlines
                cleaned_lyrics = re.sub(r'[^\w\s]','', lyrics.replace('\n', " "))
                return cleaned_lyrics
            else:
                return ''
        except Exception as e:
            print('Error in function CalculateSongWordAverage._get_song_lyrics with song title {}: '.format(song_title) + str(e))    
            print('The contents of the response are: ', response.content)
            return ''


    def _get_number_words_in_one_song(self, song_title):
        """
        This function finds the number of words in a song whose
        title is song_title.
        """
        try:
            #search for the song lyrics
            lyrics = self._get_song_lyrics(song_title)
            if lyrics:
                return self._word_count(lyrics)
            else:
                return 0  
        except Exception as e:
            print('Error in function CalculateSongWordAverage._get_number_words_in_one_song with song title {}: '.format(song_title) + str(e))    
            return 0
           

if __name__ == '__main__':
    # Create the parser
    artist_parser = argparse.ArgumentParser(prog='avgWordsSong',
                                        description='Calculates the average number of words in an artist\'s songs',
                                        )

    # Add the arguments
    artist_parser.add_argument('Artist', type=str,
                          help='The name of the artist(s) whose average number of words in their songs you wish to find')

    args = artist_parser.parse_args()

    artist_name = args.Artist
   
    #Install dependencies.
    install()
    import musicbrainzngs
    
    print("Finding the average number of words in a song by {}".format(artist_name))
    calcSongWordAvgforArtist = CalculateSongWordAverage(artist_name)
    calcSongWordAvgforArtist.find_artist_song_word_average()

    #Remove virtual environment created above
    cleanup()
    