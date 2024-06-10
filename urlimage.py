import urllib.request
import base64
import PIL.Image
import customtkinter

class WebImage:
    def __init__(self,url):
        url = urllib.request.urlopen(url)
        raw_data=url.read()
        url.close()
        image=base64.encodebytes(raw_data)
        imgdata=base64.b64decode(image)
        filename="../../PycharmProjects/chat/image.png"
        with open (filename,"wb") as f:
            f.write(imgdata)

        self.image=customtkinter.CTkImage(PIL.Image.open(filename),size=(230,230))

    def get(self):
        return self.image