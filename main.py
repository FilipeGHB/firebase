from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.core.window import Window
import firebase_admin
import requests
from firebase import firebase
from firebase_admin import credentials, auth
import pyrebase 

firebaseConfig = {
                  'apiKey': "AIzaSyDIMzqKykm21B1gS686XxjIozrLm8NsHJw",
                  'authDomain': "loginextra-7b7cc.firebaseapp.com",
                  'databaseURL': "https://loginextra-7b7cc-default-rtdb.firebaseio.com",
                  'projectId': "loginextra-7b7cc",
                  'storageBucket': "loginextra-7b7cc.appspot.com",
                  'messagingSenderId': "130591574908",
                  'appId': "1:130591574908:web:12e01b75091b2dc54832f9",
                  'measurementId': "G-3QFFBBKT6D"
};

firebas=pyrebase.initialize_app(firebaseConfig)
auth=firebas.auth()

Window.clearcolor = (1,1,1,1)
class Gerenciador(ScreenManager):
   pass

class Logado (Screen):
   pass

class Cadastro(Screen):
   pass

class Login(Screen):
   pass

class Login(App):
    def build(self):
        return Builder.load_file('main.kv')
    
    def Cadastrar(self):
      email = self.root.get_screen('cadastro').ids.email.text 
      senha = self.root.get_screen('cadastro').ids.senha.text

      try:
         user = auth.create_user_with_email_and_password(email, senha)
      except:
         self.root.get_screen('cadastro').ids.erro.color = (1,0,0,1)
      else:
         self.root.current = 'login'

    def log(self):
      email = self.root.get_screen('login').ids.email.text
      senha = self.root.get_screen('login').ids.senha.text
      try:
         auth_result = auth.sign_in_with_email_and_password(email, senha)
      except:
         self.root.get_screen('login').ids.l.color = (1, 0, 0, 1)
      else:
         self.root.current = 'Logado'



if __name__ == "__main__":
 Login().run()s