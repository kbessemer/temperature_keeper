<h1 align="center">Temperature Keeper</h1>

## Authored and Developed by:

Kyle Bessemer - <a href="https://www.linkedin.com/in/kyle-bessemer-606a7a1b2/">My LinkedIn</a>

## About the App

<a href="http://www.kylebessemer.com/portfolio/tempkeeper.html">Screenshots</a>

This app maintains a database of people, and you can add temperature readings for each person. The app will keep track of each person's temperature, and display temperature statistics and a bar graph on each person's profile. Each person can have a RFID or Barcode number added to their profile; people's names, RFID, and barcode must be unique - they can not be the same as any other person's in the app. You can upload a csv file to the app to add bulk profiles to the app, the format of the csv file must be:

Name, RFID, Barcode

The backend is built using Python and the Flask library to create an API, the database uses sqlite3 and SQLAlchemy.

The frontend runs off the same Flask server as the API, so you only need to start one program to launch the entire application. The frontend was built using Vuejs.

This app was built to work in the measurement of fahrenheit, fever indications will be based off that.

## Install Dependencies

*Change to api directory*<br>
*Run command: pip3 install -r requirements.txt*

## Run Application

*Change to api directory*<br>
*Run command: python3 app.py*

The application will run on port 5000, to access the app open your web browser and navigate to: http://localhost:5000

Changing the port that the Flask app runs on from 5000 may break functionality, you will need to update the frontend stored in the client directory and then rebuild the vuejs app. Move the build files to api/static

There is no login required for this application, I do not recommend running this on the internet because anyone could access it and modify the data.

## Disclaimer

This app is meant for educational purposes only, it is not intended to be used to keep track of medical data.