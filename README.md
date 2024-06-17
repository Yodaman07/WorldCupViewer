# WorldCupViewer
A python app that allows you to quickly view the world cup games and scores.

# How to use
Run the script normally to get the games.


If you want to build the app yourself, follow these steps
## On mac
- On macos, download the main python file, and make sure you are running the `currentDay()` function.
- Open a terminal window and locate the folder with the script in it.
- Make sure you have pyinstaller, requests, and bs4 installed. If not run `pip install -r requirements.txt`
- Then run `pyinstaller --add-data "Roboto-Bold.ttf:." --add-data "Roboto-Regular.ttf:."  display.py --onefile --windowed`
- In the dist folder, there should be an executable and an application called display.
- Double click that to run the code.
- You can also make your own custom app icons!

# How it works
The script fetches the html from the SkySports website and parses the data.

The script includes a function to get the current games in a day, and one to write to the file `data.txt` to see all games.
