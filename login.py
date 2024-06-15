from kivy.app import App 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import requests
import json
from firebase import firebase
import firebase_admin
from firebase_admin import credentials


cred_obj = credentials.Certificate('oi.json')
firebase_admin.initialize_app(cred_obj)


firebase = firebase.FirebaseApplication("https://loginextra-7b7cc-default-rtdb.firebaseio.com/", None)

class TelaLogin(BoxLayout):
    def __init__(self, **kwargs):
        super(TelaLogin, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [50, 20]
        self.spacing = 10

        Window.clearcolor = (0, 0, 0.1, 1)
        self.add_widget(Image(source='/Users/aluno.sesipaulista/Documents/Login/img/imagem.png'))

        self.add_widget(Label(text='L O G I N', font_size=30, bold=True))

        self.username_input = TextInput(hint_text='Digite o usuário...', multiline=False, size_hint=(None, None),
                                        size=(900, 70))
        self.password_input = TextInput(hint_text='Digite a senha...', password=True, multiline=False,
                                        size_hint=(None, None), size=(900, 70))
        self.add_widget(self.username_input)
        self.add_widget(self.password_input)

        self.buttons_layout = BoxLayout(padding=[0, 10], spacing=10)
        self.login_button = Button(text='Entrar', color=(0, 0, 0.1, 1), size_hint=(None, None), size=(450, 50),
                                   background_color=(100, 100, 100, 100))
        self.login_button.bind(on_press=self.login)
        self.signup_button = Button(text='Cadastre-se', color=(0, 0, 0.1, 1), size_hint=(None, None), size=(450, 50),
                                    background_color=(100, 100, 100, 100))
        self.signup_button.bind(on_press=self.ir_para_segunda_tela)
        self.buttons_layout.add_widget(self.login_button)
        self.buttons_layout.add_widget(self.signup_button)
        self.add_widget(self.buttons_layout)

    def ir_para_segunda_tela(self, *kwargs):
        self.parent.parent.current = 'Cadastro'

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        print('Username:', username)
        print('Password:', password)

        
        users = firebase.get('/Tabela', None)
        if users:
            for user in users.values():
                if user['Email'] == username and user['Senha'] == password:
                    self.show_popup("Logado Com Sucesso!")
                    return
        self.show_popup("Usuário ou senha incorretos!")

    def show_popup(self, message):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message, font_size=20))
        close_button = Button(text="Fechar", size_hint_y=None, height=50)
        content.add_widget(close_button)

        popup = Popup(title='Mensagem',
                      content=content,
                      size_hint=(None, None),
                      size=(400, 200))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

class TelaCadastro(BoxLayout):
    def __init__(self, **kwargs):
        super(TelaCadastro, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [50, 20]
        self.spacing = 10

        Window.clearcolor = (0, 0, 0.1, 1)

        self.add_widget(Label(text='C A D A S T R O', font_size=30, bold=True))
        self.email_input = TextInput(hint_text='Digite seu e-mail...', multiline=False, size_hint=(1, None),
                                        size=(900, 70))
        self.password_input = TextInput(hint_text='Digite a senha...', password=True, multiline=False,
                                        size_hint=(1, None), size=(900, 70))
        self.add_widget(self.email_input)
        self.add_widget(self.password_input)

        self.buttons_layout = BoxLayout(padding=[0, 10], spacing=10)
        self.signup_button = Button(text='Cadastrar', color=(0, 0, 0.1, 1), size_hint=(1, None), size=(900, 50),
                                    background_color=(100, 100, 100, 100))
        
        self.signup_button.bind(on_press=self.cadastro)
        self.buttons_layout.add_widget(self.signup_button)
        self.add_widget(self.buttons_layout)

    def ir_para_primeira_tela(self, *args):
        self.parent.parent.current = 'Login'

    def cadastro(self, instance):
        email = self.email_input.text
        senha = self.password_input.text

        dados = {'Email': email, 'Senha': senha}
        requisicao = requests.post("https://loginextra-7b7cc-default-rtdb.firebaseio.com/Tabela.json", data=json.dumps(dados))

        if requisicao.status_code == 200:
            print("Dados enviados!")
            self.ir_para_primeira_tela()
        else:
            print("Erro ao enviar")
            print(requisicao.status_code, requisicao.text)

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        tela_login = TelaLogin()
        tela_cadastro = TelaCadastro()

        screen_login = Screen(name='Login')
        screen_cadastro = Screen(name='Cadastro')

        screen_login.add_widget(tela_login)
        screen_cadastro.add_widget(tela_cadastro)

        sm.add_widget(screen_login)
        sm.add_widget(screen_cadastro)

        return sm

if __name__ == '__main__':
    MyApp().run()


