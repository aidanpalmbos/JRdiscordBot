# JRdiscordBot
A discord bot that is used by Jenison Robotics to webscrape information from the VEX Skills Standing Website.

Important!
-Please have the latest version of Chromium Chrome driver installed (https://download-chromium.appspot.com)
  On windows, put the .exe file in C:\Windows
  Otherwise, you will have to re-write line 16.
-Do not share the key (last line) with anyone. If it is leaked, other users can run their own code.

Notice:
Some times web scraping will not work. Most of the time, it is because the data has been wiped from the website.
  -> Manually check https://www.robotevents.com/robot-competitions/vex-robotics-competition/standings/skills to make sure there is scores available.
If issues still persist, it is most likely due to a slow connection. Increase the lines with 'driver1.implicitly_wait(5)' and set the number > 5 if needed.
