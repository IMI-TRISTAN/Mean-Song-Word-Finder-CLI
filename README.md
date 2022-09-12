# Mean_Song_Word_Finder_CLI
This software was written in Python 3.9 and the file avgWordsSong.py contains an application that when passed the name of an artist, calculates the average number of words in one of their songs.  It has a Command Line Interface.  When avgWordsSong.py is run, it creates a virtual environment on your computer and installs all the packages used by this application.  Upon completion of the calculation, the virtual environment is removed. 

After the user inputs the name of an artist, it uses the MusicBrainzngs API to retrieve the song list for that artist. It then uses the LyricsGenius API to retrieve the lyrics for each song in the song list. The number of words in each song is counted and used to calculate the word average for a song by the artist.

The calculation of the average number of words in an artist's song can be lengthy.  So the progress of the calculation is printed on the command prompt screen as the calculation progresses. 


## How to use
1. Make sure you have Python 3.9 installed on your computer.
2. Download the files avgWordsSong.py and requirements.txt to a folder on your computer.  **The name of the folder must contain no spaces**.
2. To run the application, put your computer online and open a command prompt in the folder created in step 1.
3. At the command prompt type 
4. 
    python avgWordsSong.py <artist's name>
    
For example

    python avgWordsSong.py oasis
    
Or

    python avgWordsSong.py "The Who"
    
Note, **artist names with spaces in them must be enclosed by double quotes " "**

## Automated Testing
The tests in test in test.py are not exhaustive.  Full coverage would require the construction of sets of song data with known numbers of words in them, which is outside the scope of this project.  This repository has continuous integration set up.
