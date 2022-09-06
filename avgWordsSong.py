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
    print("Cleaning up...")
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        print("Deleting the created Python Virtual Environment...")
        os.system('rmdir .venv /S /Q')
    else:
        print("Deleting the created Python Virtual Environment...")
        os.system('rm -r .venv/')


class CalculateSongWordAverage:
    def __init__(self, artist_name):
         musicbrainzngs.set_useragent(
            "CalculateSongWordAverage", "1.0", contact="s.shillitoe1@ntlworld.com")
         self.setup_music_genius_lyric_finder()
         self.artist_name = artist_name
         self.song_list = []
         self.list_song_word_count = []


    def setup_music_genius_lyric_finder(self):
        try:
            self.music_genius = lyricsgenius.Genius(LYRICS_GENIUS_ACCESS_TOKEN)
            self.music_genius.remove_section_headers = True # Remove section headers (e.g. [Chorus]) from lyrics when searching
            self.music_genius.skip_non_songs = True
            self.music_genius.excluded_terms = ["(Remix)", "(Live)", "(remix)", 
                                                "(live)", "edit", "(demo)" , "(mix)"]
        except Exception as e:
            print('Error in function CalculateSongWordAverage.setup_music_genius_lyric_finder: ' + str(e))


    def get_song_list(self):
        try:
            offset = 0
            limit = 100
          
            while True:
                song_result = musicbrainzngs.search_recordings(
                    artistname=self.artist_name, 
                    limit=limit, offset=offset, strict=True)
            
                if song_result:
                    for song in song_result["recording-list"]:
                        song_title = song["title"]
                        #use a regular expression to 'clean up' the song titles
                        #remove [] and () and their enclosed text from song title
                        #using a regular expression
                        song_title = re.sub("[\(\[].*?[\)\]]", "", song_title)
                        song_title = song_title.strip().lower()
                        self.song_list.append(song_title)
                    #increment the offset to get the next 100 song titles
                    offset += limit
                
                #Stop the while loop when there are no more songs to retrieve or
                #after 3 iterations.
                if len(song_result["recording-list"]) == 0 or offset > 300:
                    break
            
            #Remove duplicates from the list
            self.song_list = list(dict.fromkeys(self.song_list))

            if len(self.song_list) == 0:
                print("No song titles found for {}".format(
                                self.artist_name))
            else:
                print("Song list search finished")
        except Exception as e:
            print('Error in function CalculateSongWordAverage.get_song_list: ' + str(e))
    
    
    def find_artist_song_word_average(self):
        self.get_song_list()
        self.calculate_song_word_average()


    def calculate_list_average(self, list_song_words):
        if list_song_words is not None:
            return int(sum(list_song_words) / len(list_song_words))
        else:
            return 0


    def calculate_song_word_average(self):
        """ """
        try:
           for song_title in self.song_list:
                number_words = self.get_number_words_in_one_song(song_title)
                print("Processed {} which has {} words".format(song_title, number_words))
                self.list_song_word_count.append(number_words)

           if len(self.list_song_word_count):
                averageNumberWords = self.calculate_list_average(self.list_song_word_count)
                print("The average number of words in a song by {} is {}".format(self.artist_name, averageNumberWords))
           else:
                print("Could not calculated the average number of words in a song by {}".format(self.artist_name))
        except Exception as e:
            print('Error in function CalculateSongWordAverage.calculate_song_word_average: ' + str(e))


    def word_count(self, lyrics=None):
        """Returns the number of words in a song."""
        try:
            if lyrics is not None:
                word_list = lyrics.split()
                return len(word_list)
            else:
                return 0
        except Exception as e:
            print('Error in function CalculateSongWordAverage.word_count when lyrics={}: '.format(lyrics) + str(e))


    def get_number_words_in_one_song(self, song_title):
        try:
            #search for the song
            song = self.music_genius.search_song(song_title, self.artist_name)
            if song:
                if song.lyrics is not None:
                    return self.word_count(song.lyrics)
            else:
                return 0  
        except Exception as e:
            print('Error in function CalculateSongWordAverage.get_number_words_in_one_song with song title {}: '.format(song_title) + str(e))    
            return 0
           

if __name__ == '__main__':
    install()
    import musicbrainzngs
    import lyricsgenius

    # Create the parser
    my_parser = argparse.ArgumentParser(prog='avgWordsSong',
                                        description='Calculates the average number of words in an artist\'s songs',
                                        )

    # Add the arguments
    my_parser.add_argument('Artist', type=str,
                           help='The name of the artist(s) whose average number of words in their songs you wish to find')

    args = my_parser.parse_args()

    artist_name = args.Artist
    print("Finding the average number of words in a song by {}".format(artist_name))
    calcSongWordAvgforArtist = CalculateSongWordAverage(artist_name)
    calcSongWordAvgforArtist.find_artist_song_word_average()

    cleanup()