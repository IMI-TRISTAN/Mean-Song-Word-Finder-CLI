# Mean_Song_Word_Finder_CLI
The file avgWordsSong.py contains an application that when passed the name of an artist, calculates the average number of words in one of their songs.  It has a Command Line Interface.  When avgWordsSong.py is run, it creates a virtual environment on your computer and installs all the packages used by this application.  Upon completion of the calculation, the virtual environment is removed. 

The calculation of the average number of words in an artist's song can be lengthy.  So the progress of the calculation is printed on the command prompt screen as the calculation progresses. 


## How to use
1. Download the files avgWordsSong.py and requirements.txt to a folder on your computer.  The name of the folder must contain no spaces.
2. To run the application, put your computer online and open a command prompt in the folder created in step 1.
3. At the command prompt type 
4. 
    python avgWordsSong.py <artist's name>
    
For example

    python avgWordsSong.py oasis
    
Or

    python avgWordsSong.py "The Who"
    
Note, artist names with spaces in them must be enclosed by double quotes " "

## Automated Testing
The tests in test in test.py are not exhaustive.  Full coverage would require the construction of sets of song data with known numbers of words in them, which is outside the scope of this project.  This repository has continuous integration set up.
