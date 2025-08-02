from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QVBoxLayout,QHBoxLayout,QLineEdit,QLabel,QFrame
from datetime import datetime 
from PyQt5.QtGui import QPalette,QColor
from PyQt5.QtCore import Qt
from time import strftime
from datetime import * 
import pygame.mixer
import pyttsx3
import requests
import pygame
import sys



class Weather_App(QWidget):
    def __init__(self):
        super().__init__()


        #background song
        pygame.init()
        pygame.mixer.init()

        self.engine = pyttsx3.init()

        self.palette = QPalette()

        self.setWindowTitle("Enhanced Weather app")
        self.setGeometry(400,400,500,500)


        self.time_label = QLabel(self)
        self.Intro_label = QLabel("enter the city: ",self)
        self.City_label = QLineEdit()
        self.Enter_button = QPushButton("enter",self)
        self.Temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.Enter_button.clicked.connect(self.get_weather)

        self.initUI()
    
        #connecting button with methods

        pygame.mixer.music.load("Background.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(.1)

       
        #QPalette
        self.palette.setColor(QPalette.Window, QColor("#a9cb7b"))

    def initUI(self):
      

        #self.setStyleSheet("""
        #                      background-image: url(Background.jpg);
        #                     background-repeat: no-repeat;
        #                    background-position: center;
        #
        #                   """)


        #making the layout Box
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        vbox.addWidget(self.Intro_label)
        vbox.addWidget(self.City_label)
        vbox.addWidget(self.Enter_button)
        vbox.addWidget(self.Temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

   
        self.time_label.setAlignment(Qt.AlignRight)

        #center the labels
        self.Intro_label.setAlignment(Qt.AlignCenter)
        self.City_label.setAlignment(Qt.AlignCenter)
        self.Temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        #naming the objects
        self.Intro_label.setObjectName("Intro_label")
        self.City_label.setObjectName("City_label")
        self.Temperature_label.setObjectName("Temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.Enter_button.setObjectName("Enter_button")


        self.setStyleSheet("""QLabel#Intro_label{font-size:50px}
                              QLabel#Temperature_label{font-size: 50px}
                              QLabel#emoji_label{font-size: 120px}
                              QLabel#description_label{font-size: 60px}
                           
                             
                           """)


        ADD_frame = QFrame(self)
        AF_layout = QHBoxLayout(self)

        ADD_frame.setFrameShape(QFrame.Box)
        ADD_frame.setLayout(AF_layout)
        vbox.addWidget(ADD_frame)


        #Wind Speed
        Wind_frame = QFrame(self)
        W_layout = QHBoxLayout(self)

        Wind_frame.setFrameShape(QFrame.Box)
        self.Wind_label = QLabel()
        W_layout.addWidget(self.Wind_label)
        Wind_frame.setLayout(W_layout)
        AF_layout.addWidget(Wind_frame)
        Wind_frame.setStyleSheet("""
                                     background-color: #3296cd;
                                     padding: 25px;
                                     border-radius: 25px;
                                     """)

        #pressure Speed
        pressure_frame = QFrame(self)
        p_layout = QHBoxLayout(self)

        pressure_frame.setFrameShape(QFrame.Box)
        pressure_frame.setStyleSheet("""
                                     background-color: #3296cd;
                                     padding: 15px;
                                     border-radius: 15px;
                                     """)
        self.Pressure_label = QLabel()
        p_layout.addWidget(self.Pressure_label)
        pressure_frame.setLayout(p_layout)


        AF_layout.addWidget(pressure_frame)



    def get_weather(self):
        api_key = ""
        self.city = self.City_label.text()



        try:
          respone = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={api_key}")
          respone.raise_for_status()
         
          self.data = respone.json()
          self.display_temperature()
          print(self.data)
         
        except requests.exceptions.HTTPError as e:
          match e.response.status_code:
              case 401:
                   self.display_error("Invalid API key (401)")
              case 404:
                   self.display_error("not found")
              case _:
                  self.display_error("unknown error")

        except requests.exceptions.ConnectionError:
            self.display_error("connection error")


        except requests.exceptions.Timeout:
            self.display_error("Timeout  error")



    def display_temperature(self):
        temp_k = self.data["main"]["temp"]
        temp_c = temp_k - 273.15
        temp_format = f"{temp_c:.0f}°C"
        self.Temperature_label.setText(temp_format)
        self.Temperature_label.setStyleSheet("font-size: 50px")
      
        weather_description = self.data["weather"][0]["description"]
        self.description_label.setText(weather_description)
        self.description_label.setStyleSheet("font-size: 40px")

        weather_id = self.data["weather"][0]["id"]
        self.emoji_label.setText(self.display_emoji(weather_id))
        self.emoji_label.setStyleSheet("font-size: 90px")

        wind_speed = self.data["wind"]["speed"]
        self.Wind_label.setText(f"{wind_speed:02} km/h")
        self.Wind_label.setStyleSheet("font-size: 20px")

        pressure_speed = self.data["main"]["pressure"]
        self.Pressure_label.setText(f"{pressure_speed/10} passcal")
        self.Pressure_label.setStyleSheet("font-size: 20px")

        get_time = self.data["dt"]
        current_time = datetime.utcfromtimestamp(get_time)
        readable_form = current_time.strftime('%H:%M:%S')
        self.time_label.setText(readable_form)
        self.time_label.setStyleSheet("""
                                      font-size: 20px;
                                      background-color: #3ec1b3;
                                      padding: 15px;
                                      border-radius: 15px;
                                       """)

        #reading text
        self.read_text(f"The current temperature in {self.city} is {temp_format}, and the weather is {weather_description}.")

    def display_error(self,message):
        self.Temperature_label.setText(message)
        self.setStyleSheet("font-size: 25px")
        self.description_label.clear()
        self.emoji_label.clear()
        self.Wind_label.clear()
        self.Pressure_label.clear()
        self.time_label.clear()

    
    def read_text(self,message):
          self.engine.stop()
          self.engine.say(message)
          self.engine.runAndWait()
          self.engine.say(message)

      
         


    @staticmethod
    def display_emoji(weather_id):
      if 200 <= weather_id <= 232:
         return "⛈️"
      elif 300 <= weather_id <= 321:
         return "🌦️"
      elif 500 <= weather_id <= 531:
         return "🌧️"
      elif 600 <= weather_id <= 622:
         return "❄️"
      elif 701 <= weather_id <= 781:
         return "🌫️"
      elif weather_id == 800:
         return "☀️"
      elif 801 <= weather_id <= 804:
         return "🌤️"
      else:
         return "❔"



if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = Weather_App()


    app.setPalette(weather_app.palette)
    weather_app.show()
    sys.exit(app.exec_())



