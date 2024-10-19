import time
import matplotlib.pyplot as plt
import kivy
kivy.kivy_configure()
import numpy as np
import MySQLdb.cursors
import random
import mysql.connector


from keras.models import load_model
from keras.utils import load_img, img_to_array
from kivy.config import Config
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.graphics.texture import Texture


Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '500')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'position', 'auto')
Config.set('graphics', 'fullscreen', '0')
Config.set('kivy', 'keyboard_mode', '')
Config.set('kivy', 'exit_on_escape', '1')
Config.set('kivy', "desktop", '1')
Config.write()

class mysql_connection:
    def create_connection():
        try:
            db = mysql.connector.connect(host='103.200.23.139',
                                user='capstone_capstonegr5',
                                passwd='THANHba0@@',
                                db='capstone_username')
            print("connected to server....")
            return db
        except:
            print("do not connect....")
            return None

plt.switch_backend('agg')
# kivy.kivy_data_dir="C://python_Code/Capstone/test_app/"
connection = mysql_connection.create_connection()
mymodel = load_model('/Users/nhatminh/Downloads/Senior/CapstoneDesign2/Python/models/best_model.h5')

class testing:
    def test(img):
        CATEGORIES = ['Cassava Bacterial Blight (CBB)', 'Cassava Brown Streak Disease (CBSD)', 'Cassava Green Mottle (CGM)', 'Cassava Mosaic Disease (CMD)', 'Healthy']
        IMG_SIZE = 512
        test_image = load_img(img, target_size = (IMG_SIZE, IMG_SIZE))
        test_image = img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)

        prediction = mymodel.predict([test_image])
        print(prediction)
        max_item = max(prediction[0])
        print(max_item)
        max_index = max([index for index, item in enumerate(prediction[0]) if item == max_item])
        print(max_index)
        out = CATEGORIES[max_index]
        return max_index, max_item
        pass


#**********************các loại bệnh***********************
class CBB(Screen):
    def close(ojb):
        App.get_running_app().stop()
        Window.close()


class CBDS(Screen):
    def close(ojb):
        App.get_running_app().stop()
        Window.close()


class CGM(Screen):
    def close(ojb):
        App.get_running_app().stop()
        Window.close()


class CMD(Screen):
    def close(ojb):
        App.get_running_app().stop()
        Window.close()


class Healthy(Screen):
    def close(ojb):
        App.get_running_app().stop()
        Window.close()


#******************data entering*****************************
class Page1_take_a_picture(Screen):
    img = ObjectProperty(None)
    camera = ObjectProperty(None)

    def capture(self):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("image.png".format(timestr))
        max_index, max_item = testing.test("image.png")
        CATEGORIES = ['Cassava Bacterial Blight (CBB)', 'Cassava Brown Streak Disease (CBSD)', 'Cassava Green Mottle (CGM)', 'Cassava Mosaic Disease (CMD)', 'Healthy']
        if max_index == 4:
            if max_item >= .83:
                sm.current = 'Healthy'
            else:
                invalidImgae()
        elif max_index == 3:
            if max_item >= .83:
                sm.current = 'CMD'
            else:
                invalidImgae()
            return max_index
        elif max_index == 2:
            if max_item >= .83:
                sm.current = 'CGM'
            else:
                invalidImgae()
        elif max_index == 1:
            if max_item >= .83:
                sm.current = 'CBDS'
            else:
                invalidImgae()
        elif max_index == 0:
            if max_item >= .83:
                sm.current = 'CBB'
            else:
                invalidImgae()
        pass

#********************login*****************************
class Register(Screen):
    fullname = ObjectProperty(None)
    email = ObjectProperty(None)
    usernamee = ObjectProperty(None)
    password = ObjectProperty(None)


    def register(self):
        connection = mysql_connection.create_connection()
        id_user = random.randint(111111, 999999)
        if self.fullname.text != "" and self.usernamee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password.text != "":
                cur = connection.cursor()
                query = f"INSERT INTO `username` (`id`, `full_name`, `email`, `username`, `password`) VALUES ('{id_user}', '{self.fullname.text}', '{self.email.text}', '{self.usernamee.text}','{self.password.text}');"
                cur.execute(query)
                connection.commit()

            else:
                invalidForm()
                self.reset()
                sm.current = "register"
        else:
            invalidForm()
            self.reset()
            sm.current = 'register'


    def login(self):
        self.reset()
        sm.current = "UI"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.usernamee.text = ""
        self.fullname.text = ""


class Forget(Screen):
    email_forget = ObjectProperty(None)
    def forget(self):

        global reset_email
        reset_email = self.email_forget.text
        connection = mysql_connection.create_connection()
        cur = connection.cursor()
        if self.email_forget.text != "" and self.email_forget.text.count("@") == 1 and self.email_forget.text.count(".") > 0:
            query = f"SELECT * FROM username WHERE email=%s"
            cur.execute(query, [self.email_forget.text])
            row = cur.fetchone()
            if row == None or self.email_forget.text == "":
                invalidEmail()
            else:
                self.email_forget.text = ""
                sm.current = "Newpw"
        else:
            invalidEmail()


class Newpw(Screen):
    ti1fg = ObjectProperty(None)
    ti2fg = ObjectProperty(None)
    
    def resetpw(self):
        if self.ti1fg.text == self.ti2fg.text:
            connection = mysql_connection.create_connection()
            cur = connection.cursor()
            query = f"UPDATE username SET password=%s WHERE email=%s"
            cur.execute(query, (self.ti1fg.text, reset_email))
            connection.commit()
            sm.current = "UI"
        else:
            invalidPW()


class UserInterface(Screen):
    fullname = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    username = ObjectProperty(None)
    
    def login(self):
        connection = mysql_connection.create_connection()
        cur = connection.cursor(MySQLdb.cursors.DictCursor)
        query = f"SELECT * FROM username WHERE username=%s and password=%s"
        cur.execute(query, (self.username.text, self.password.text))
        row = cur.fetchone()
        if row == None:
            invalidLogin()
        else:
            self.reset()
            sm.current = "page1"

    def register(self):
        self.reset()
        sm.current = "register"

    def reset(self):
        self.username.text = ""
        self.password.text = ""


class WindowManager(ScreenManager):
    pass


def invalidImgae():
    pop = Popup(title='invalid image', content=Label(text='please enter cassava leaf'),
                size_hint=(None, None), size=(400,200))
    pop.open()


def invalidEmail():
        pop = Popup(title='Invalid email.',
                  content=Label(text='Invalid email.'),
                  size_hint=(None, None), size=(400, 200))
        pop.open()


def invalidPW():
        pop = Popup(title='Invalid Password.',
                  content=Label(text='Invalid Password.'),
                  size_hint=(None, None), size=(400, 200))
        pop.open()


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 200))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 200))
    pop.open()


#**********************screen******************************
Builder.load_file('main.kv')
sm = ScreenManager(transition=NoTransition())
screens = [Forget(name="Forget"), Newpw(name="Newpw"),UserInterface(name="UI"), Register(name="register"), Page1_take_a_picture(name="page1"), CBB(name="CBB"), CBDS(name="CBDS"), CGM(name="CGM"), CMD(name="CMD"), Healthy(name="Healthy")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "UI"

#**********************main app******************************
class mainApp(App):
    def build(self):
        return sm

#**********************run app******************************
if __name__=="__main__":
    mainApp().run()