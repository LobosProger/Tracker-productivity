# Tracker-productivity
* Developed a productivity tracker for voice-controlled speakers and assistants for Yandex in just 2 days during participation in hackathon IT Fest 2023.
* This tool enables users to track time spent on various activities (e.g., programming or reading) with the ability to view statistics and receive productivity improvement recommendations from AI based on ChatGPT.
* Created by using Yandex Cloud Functions and Firebase to created a backend for the project.
* Was written on three programming languages: Python, JavaScript and SQL for database management
* To test it, you can use a link, but you need to submit invite to test it: https://dialogs.yandex.ru/share?key=SYQUAwd4mYLSKHeXHzxx

# Results of hackathon
* After participation, I with my team took 3rd place in this hackathon and won prize 150 thousand tenge (330 dollars):

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/d884bb29-15f7-4e23-9a8c-a6b36af33695" />
</div>

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/d153c6ef-87ca-4a8d-83a2-ad5d92e1e02e" />
</div>

* Also, we were published in the media of Kazakhstan and Forbes:
* Forbes link: https://forbes.kz//actual/technologies/yes_future_itogi_2023_goda_po_hakatonam_ot_halyk/
* Media of Kazakhstan link: https://www.inform.kz/ru/molodih-kazahstantsev-nauchili-sozdavat-naviki-dlya-golosovogo-assistenta-4add30

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/7c6116bc-e327-4d27-a418-03c361063f11" height="400"/>
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/7507ca0c-9c3c-4785-aa2e-0760cc179a58" height="400"/>
</div>

# Demonstration of project

* After launching assistant via Yandex, you see greeting in the chat with Alice (translated on the English language below images) or hear on the voice-controlled speaker:

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/8e7286a0-1cc7-4180-9dbc-ed49e9e9467c" height="400"/>
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/1d326132-6bfe-48b6-a0d8-aa5687a09287" height="400"/>
</div>
<br>

* Then, asking him about what he can do, he will explain about functionality for user:

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/b30c2013-5531-4ad6-b5c6-0aaf363fedec" />
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/8868da82-7df7-4d4c-804e-2b27e85107c7" />
</div>

# Capturing activities during day

* After entering record about activity (for example, programming with time of activity from 10:00 to 12:00) he will send a response about successful saving:

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/fb68e853-294e-4cdc-a7b1-3972fe010b21" />
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/8c7b17df-b599-4f85-b27f-08702498f263" />
</div>

* Let's try to add additional record (for example, study English language):

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/57c92dda-afbb-4f46-98b8-103ab6eaa998" />
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/59d13ff1-4fb6-4b9b-89aa-093497cb95e6" />
</div>

# Statistics and report by AI

* After capturing activities, user can see statistics of activity during day, week or month, by entering message
* Statistics is capturing on backend servers of Yandex Cloud:

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/4f64c5b8-ff74-4afd-871e-9f643cc5636d" />
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/214d16bc-2db9-4bd7-9fb2-024318dfe220" />
</div>

* Then, after entering message "Get report" user gets a generated report by ChatGPT, which analyzed activity of user for certain period of time (day, week, month)
* The service of Yandex Cloud is connecting to deployed my code on Firebase, making like "bridge" because direct communication from Yandex was not possible
* ChatGPT is set upped by prompt engineering, like analyzing input data and answering in certain manner:

<div align="center">
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/d33683b8-d1c1-40ee-a42a-beda908f3cb3" />
  <img src="https://github.com/LobosProger/Tracker-productivity/assets/78168123/8164ee03-2fdd-4f13-ade2-6d531500b1ea" />
</div>
