# WorldCupViewer
A python app that allows you to quickly view the world cup games and scores.

# How to use
Run the script normally to get the games.


If you want to turn this into an executable or app use the following steps.
## On mac
- On macos, download the main python file, and make sure you are running the `currentGame()` function.
- Open a terminal window and locate the folder with the script in it.
- Make sure you have pyinstaller, requests, and bs4 installed. If not run `pip install` and type `pyinstaller`, `requests`, or `bs4`.
- Then run pyinstaller FILENAME.py.
- In the dist folder, there should be an executable called FILENAME.
- Click that to run the code.

# How it works
The script fetches the html from the SkySports website and parses the data.

The script includes a function to get the current games in a day, and one to write to the file `data.txt` to see all games.
