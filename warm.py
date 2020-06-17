# Set Windows size as phone screen
from kivy.config import Config
Config.set("graphics","width",360)
Config.set("graphics","height",740)
# Remove Above lines when apk build

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem,MDList
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image

from pytube import YouTube
from urllib.request import urlretrieve
from threading import Thread
import os

_Downloading_Threads = list()

def Download_Video(obj):
    obj.download()



class Home(MDScreen):
    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.current_video_data = {
            "title": None,
            "img_name": None,
            "quality_list": None,
            "select_video": None,
        }
        
    def select_download_quality(self,obj):
        
        self.ids.select_video.text = "Quality " + obj.text
        for quality in self.current_video_data["quality_list"]:

            if obj.text == quality.resolution:
                self.current_video_data["select_video"]= quality

        # print(self.current_video_data["select_video"])
    
    def click_download(self,obj):
        # self.current_video_data.get("select_video").download()
        D_TH = Thread(target=Download_Video,
        args=(self.current_video_data.get("select_video"),))

        _Downloading_Threads.append(D_TH)
        D_TH.start()

    def show_download_btn(self,obj):
        print(self.current_video_data["select_video"].filesize)
        if "download_btn" not in self.ids:
            self.ids["download_btn"] = MDRaisedButton(
                    text= "Download Video",
                    pos_hint= {"center_x": .5, "center_y": .21},
                    on_release= self.click_download,
                )

            self.add_widget(self.ids.get("download_btn"))

    
    def show_video_data(self):
        """[Show thumbnail and title of video]
            
        """
        title = self.current_video_data.get("title")
        img = self.current_video_data.get("img_name")

        if self.current_video_data.get("quality_list"):
            for quality in self.current_video_data.get("quality_list"):
                if quality.resolution != None:
                    # print(quality.resolution)
                    self.ids.quality_list.add_widget(
                        OneLineListItem(
                            text= quality.resolution,
                            on_press= self.select_download_quality,
                            on_release= self.show_download_btn,
                            ))

        
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
        """
        Get Video data using PyTube module and
        download thumbnail image save ad videoid

        """
        try:
            yt = YouTube(self.ids.video_url.text)            
            img_name = yt.video_id + ".img"
            urlretrieve(yt.thumbnail_url,img_name)
            
            self.current_video_data["title"] = yt.title
            self.current_video_data["img_name"] = img_name
            self.current_video_data["quality_list"] = yt.streams.filter(
                only_video = True,
                file_extension = "mp4"
            
                )
        except:
            self.current_video_data["title"] = "Connection Error"
            self.current_video_data["img_name"] = "test.jpeg"



class WarmApp(MDApp):
    def build(self):
        return Home()

    def on_stop(self):
        # for D_TH in _Downloading_Threads:
        #     D_TH.cl
        for get_file in os.listdir():
            if ".img" in get_file:
                os.remove(get_file)
        
    



if __name__ == "__main__":
    WarmApp().run()

