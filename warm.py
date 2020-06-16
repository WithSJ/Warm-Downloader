# Set Windows size as phone screen
from kivy.config import Config
Config.set("graphics","width",360)
Config.set("graphics","height",740)
# Remove Above lines when apk build

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.image import Image

from pytube import YouTube
from urllib.request import urlretrieve
import os

class Home(MDScreen):
    def show_video_data(self):
        """[Show thumbnail and title of video]
            
        """
        title,img = self.get_video_data()        
        self.ids.video_title.text = title
        

        if "show_img" in self.ids:            
            self.ids.video_img.remove_widget(
                self.ids["show_img"]
            )

            self.ids["show_img"]= Image(source=img)
            self.ids.video_img.add_widget(self.ids["show_img"])   
        else:
            self.ids["show_img"]= Image(source=img)
            self.ids.video_img.add_widget(self.ids["show_img"])

    
    def get_video_data(self):
        """[Get Video data using PyTube module and
            download thumbnail image save ad videoid]

        Returns:
            [tupple]: [First is Title and second is image path]
        """

        try:
            yt = YouTube(self.ids.video_url.text)
            
            img_name = yt.video_id + ".img"
            
            urlretrieve(yt.thumbnail_url,img_name)
            
            return yt.title,img_name
        except:
            return "Connection Error","test.jpeg"


class WarmApp(MDApp):
    def build(self):
        return Home()
    



if __name__ == "__main__":
    WarmApp().run()

