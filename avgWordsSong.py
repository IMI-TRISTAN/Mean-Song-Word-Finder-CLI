"""
This module contains a class for the calculation of the average number of words
in a song by a particular artist.

It uses the package musicbrainzngs to get a list of the songs of a particular artist.
It uses the package lyricsgenius to a get the lyrics of each song in the above list.

It runs in a CLI 
"""
import venv
import argparse
import re
import os
import sys

__app_name__ = "avgWordsSong"
__version__ = "0.1.0"

#constant
LYRICS_GENIUS_ACCESS_TOKEN = "Xggm2iesVVTObjSTWDUIVfWoyGhftueOxOowgkCR5LKRyYS8Ml9K8oam4zBM3sR7"

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
         self._setup_music_genius_lyric_finder()
         self._artist_name = artist_name
         self._song_list = []
         self._list_song_word_count = []


    def _setup_music_genius_lyric_finder(self):
        """
        This function configures how lyrics are returned by lyricsgenius
        """
        try:
            self.music_genius = lyricsgenius.Genius(LYRICS_GENIUS_ACCESS_TOKEN)
            # Remove section headers (e.g. [Chorus]) from lyrics when searching
            self.music_genius.remove_section_headers = True
            # Ignore things like interviews & film appearances
            self.music_genius.skip_non_songs = True
            self.music_genius.excluded_terms = ["(Remix)", "(Live)", "(remix)", 
                                                "(live)", "edit", "(demo)" , "(mix)"]
        except Exception as e:
            print('Error in function CalculateSongWordAverage.setup_music_genius_lyric_finder: ' + str(e))


    def _get_song_list(self):
        """
        This function uses musicbrianzngs to get a list of songs
        by an artist.

        Song titles are cleaned up to remove [] and () and their
        enclosed text from the title.

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
                        song_title = song_title.strip().lower()
                        self._song_list.append(song_title)
                    #increment the offset to get the next 100 song titles
                    offset += limit
                
                #Stop the while loop when there are no more songs to retrieve or
                #after 3 iterations.
                if len(song_result["recording-list"]) == 0 or offset > 300:
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
                word_list = lyrics.split()
                return len(word_list)
            else:
                return 0
        except Exception as e:
            print('Error in function CalculateSongWordAverage._word_count when lyrics={}: '.format(lyrics) + str(e))


    def _get_number_words_in_one_song(self, song_title):
        """
        This function finds the number of words in a song whose
        title is song_title.
        """
        try:
            #search for the song
            song = self.music_genius.search_song(song_title, self._artist_name)
            if song:
                if song.lyrics is not None:
                    return self._word_count(song.lyrics)
            else:
                return 0  
        except ConnectionError as ce:
            print('Connection Error in function CalculateSongWordAverage._get_number_words_in_one_song with song title {}: '.format(song_title) + str(ce))
            return 0
        except Exception as e:
            print('Error in function CalculateSongWordAverage._get_number_words_in_one_song with song title {}: '.format(song_title) + str(e))    
            return 0
           

if __name__ == '__main__':
    #Install dependencies.
    install()
    import musicbrainzngs
    import lyricsgenius

    # Create the parser
    artist_parser = argparse.ArgumentParser(prog='avgWordsSong',
                                        description='Calculates the average number of words in an artist\'s songs',
                                        )

    # Add the arguments
    artist_parser.add_argument('Artist', type=str,
                          help='The name of the artist(s) whose average number of words in their songs you wish to find')

    args = artist_parser.parse_args()

    artist_name = args.Artist
    print("Finding the average number of words in a song by {}".format(artist_name))
    calcSongWordAvgforArtist = CalculateSongWordAverage(artist_name)
    calcSongWordAvgforArtist.find_artist_song_word_average()

    #Remove virtual environment created above
    cleanup()