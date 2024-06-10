import os.path
from tkinter import PhotoImage
import customtkinter
from openai import  OpenAI
from tkinter import  filedialog
import os
from PIL import Image, ImageTk
import shutil
import threading
from urlimage import WebImage
import requests
import pyaudio
import wave



client = OpenAI(api_key="")
_model="gpt-3.5-turbo"


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        #Create window with title, size, and bg
        self.title("AIGenerator.py")
        self.geometry("1100x590")
        self.bg_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.bg_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")

        # configure grid layout (3x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2), weight=1)
        self.grid_rowconfigure(3, weight=1)

        #Text column
        self.text_gen_label = customtkinter.CTkLabel(self, height=33, corner_radius=5, fg_color=("gray95", "gray22"), text="Text Generator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.text_gen_label.grid(row=0, column=0, padx=(20, 20), pady=(15, 0), sticky="new")

        self.text_prompt = customtkinter.CTkTextbox(self, height=110)
        self.text_prompt.grid(row=0, column=0, padx=(20, 20), pady=(60, 0), sticky="new")

        self.text_gen_button = customtkinter.CTkButton(self, height=40, text="Generate", command=self.text_gen_button_event)
        self.text_gen_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 0), sticky="new")

        self.text_complete = customtkinter.CTkTextbox(self, width=250, height=450)
        self.text_complete.grid(row=1, column=0, padx=(20, 20), pady=(60, 0), sticky="nsew")

        self.appearance_mode_label = customtkinter.CTkLabel(self, bg_color=("gray95", "gray22"), text="Appearance Mode:")
        self.appearance_mode_label.grid(row=2, column=0, padx=(50, 150), pady=(0, 40), sticky="sw")

        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=2, column=0, padx=(35, 150), pady=(20, 10), sticky="sw")

        # Image Column
        self.image_number = customtkinter.IntVar()
        self.switch_image = customtkinter.IntVar()

        self.image_gen_label = customtkinter.CTkLabel(self, height=33, corner_radius=5, fg_color=("gray95", "gray22"), text="Image Generator", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.image_gen_label.grid(row=0, column=1, padx=(15, 20), pady=(15, 0), sticky="new")

        self.image_num_dropdown_button = customtkinter.CTkOptionMenu(self.image_gen_label, width=17, height=24, bg_color=("gray95", "gray22"), values=["1", "2", "3", "4", "5"], font=customtkinter.CTkFont(size=10, weight="bold"), variable=self.image_number,command=self.image_num_dropdown_button_event)
        self.image_num_dropdown_button.grid(row=0, column=0, pady=(4, 0), sticky="ne")

        self.image_prompt = customtkinter.CTkTextbox(self, height=110)
        self.image_prompt.grid(row=0, column=1, padx=(20, 20), pady=(60, 0), sticky="new")

        self.image_gen_button = customtkinter.CTkButton(self, height=40, text="Generate",command=self.image_gen_button_event)
        self.image_gen_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 0), sticky="new")

        self.image_button = customtkinter.CTkButton(self, width=250, height=260, fg_color=("gray95", "gray22"), hover_color=("gray95", "gray22"), text=" ",command=self.download)
        self.image_button.grid(row=1, column=1, padx=(20, 20), pady=(60, 35), sticky="nsew")

        self.image_num_frame = customtkinter.CTkFrame(self, width=20, height=10, fg_color=("gray70", "gray13"))
        self.image_num_frame.grid(row=1, column=1, padx=(20, 20), sticky="sew")

        self.image_num_segmented_button = customtkinter.CTkSegmentedButton(self.image_num_frame, width=70, height=20, values=["     1    "], variable=self.switch_image, command=self.switch)
        self.image_num_segmented_button.grid(row=1)

        self.image_complete = customtkinter.CTkTextbox(self)
        self.image_complete.grid(row=2, column=1, padx=(20, 20), pady=(13, 10), sticky="nsew")

        # Audio column
        self.transcript = customtkinter.IntVar()
        self.translate = customtkinter.IntVar()

        self.voice_to_text_label = customtkinter.CTkLabel(self, height=33, corner_radius=5, fg_color=("gray95", "gray22"), text="Voice to Text", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.voice_to_text_label.grid(row=0, column=2, padx=(20, 20), pady=(15, 0), sticky="new")

        self.record_button = customtkinter.CTkButton(self, width=60, height=60, border_width=8, corner_radius=80, bg_color=("gray85", "gray17"), fg_color="SeaGreen3", border_color="red", hover_color="red", text="",command=self.record_button_event)
        self.record_button.grid(row=0, column=2, padx=(10, 0), pady=(70, 0), sticky="n")

        self.transcription_button = customtkinter.CTkSwitch(self, width=20, height=10, bg_color=("gray85", "gray17"), text="Transcription", onvalue=1, offvalue=0, variable=self.transcript)
        self.transcription_button.grid(row=0, column=2, padx=(10, 120), sticky="s")

        self.translation_button = customtkinter.CTkSwitch(self, width=20, height=10, bg_color=("gray85", "gray17"), text="Translation", onvalue=1, offvalue=0, variable=self.translate)
        self.translation_button.grid(row=0, column=2, padx=(160, 0), sticky="s")

        self.audio_complete = customtkinter.CTkTextbox(self, width=250, height=250)
        self.audio_complete.grid(row=1, column=2, padx=(20, 20), pady=(30, 0), sticky="nsew")

        # create scrollable frame to house recordings
        self.recordings_frame = customtkinter.CTkScrollableFrame(self, label_text="Recordings")
        self.recordings_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(250, 0), sticky="sew")
        self.recordings_frame.grid_columnconfigure(0, weight=1)

        self.gif_button = customtkinter.CTkButton(self, width=250, height=260, fg_color=("gray95", "gray22"),
                                                  hover_color=("gray95", "gray22"), text=" ",
                                                  command=lambda: self.generate_gif_button_event)
        self.gif_button.grid(row=3, column=1, padx=(20, 20), pady=(60, 35), sticky="nsew")


        self.generate_gif_button = customtkinter.CTkButton(self, text="Generate GIF",
                                                           command=self.generate_gif_button_event)
        self.generate_gif_button.grid(row=2, column=0, padx=(20, 20), pady=(10, 0), sticky="new")
        # set default values
        self.appearance_mode_option_menu.set("Dark")
        self.image_num_dropdown_button.set(value="# of imgs")
        self.transcript.set(1)
        self.links=[]
        self.image_to_download = False
        self.recording=False


    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def text_gen_button_event(self):
        prompt = self.text_prompt.get("1.0", "end")
        chat_prompt=[
            {"role":"user","content":prompt}
        ]
        response = client.chat.completions.create(
            model=_model,
            messages= chat_prompt

        )
        self.text_complete.insert("1.0",response.choices[0].message.content)


    def image_num_dropdown_button_event(self,_event=None):
        list = []
        for i in range (0,self.image_number.get()):
            i+=1
            list.append(f"           {i}      ")
        self.image_num_segmented_button.configure(values=list)
        self.image_num_segmented_button.set(list[0])
        self.image_num_segmented_button.configure(selected_color="SeaGreen3")

    def generate_gif_button_event(self):
        # Kullanıcıya bir dizin seçim penceresi gösterin
        folder_path = filedialog.askdirectory(title="Fotoğraflar Klasörünü Seçin")
        if not folder_path:
            print("Dizin seçilmedi.")
            return

        # Seçilen klasördeki fotoğrafları alın
        image_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if
                       file.endswith(('.jpg', '.jpeg', '.png'))]

        if not image_files:
            print("Seçilen klasörde fotoğraf bulunamadı.")
            return

        # Fotoğrafları açın
        images = [Image.open(image) for image in image_files]

        # GIF oluşturun
        gif_path = os.path.join(os.path.expanduser("~"), "Desktop", "generated.gif")
        images[0].save(gif_path, save_all=True, append_images=images[1:], duration=100, loop=0)




        print("GIF başarıyla oluşturuldu:", gif_path)

    def show_gif(self, gif_path):
        image = Image.open(gif_path)
        photo = ImageTk.PhotoImage(image)
        label = customtkinter.CTkLabel(self, image=photo)
        label.image = photo  # Referansı tutmak için
        label.grid(row=3, column=0, padx=(20, 20), pady=(10, 0), sticky="new")

    def image_gen_button_event(self):
        self.image_to_download = True
        self.links = []
        self.image_complete.delete("1.0", "end")
        self.image_button.configure(hover_color="sea green")
        num = self.image_number.get()

        user_prompt = self.image_prompt.get("1.0", "end").strip()

        # Sizin içerde belirlediğiniz prompt metnini tanımlayın
        your_prompt = "act like a gif maker,the user will give you information about the image he wants, and you create photos that are very similar to each other in the type the user wants. the photos should be similar frame by frame . the photos should be like a continuation of each other."

        # Kullanıcı prompt'u ve sizin prompt'unuzu birleştirin
        prompt = f"{user_prompt} {your_prompt}"

        image_gen = client.images.generate(prompt=prompt, n=num, size="1024x1024")

        # Get the Desktop path
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        download_folder = os.path.join(desktop_path, "GifFile")

        # Ensure the directory exists
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        for img in range(0, num):
            url = image_gen.data[img].url
            self.links.append(url)
            self.image_complete.insert(1.0, f"{self.links[img]}\n\n")

            # Görüntüyü indir ve belirtilen klasöre kaydet
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(download_folder, f"image_{img + 1}.png"), 'wb') as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)

        # İlk görüntüyü uygulama içinde göster
        image = WebImage(self.links[0])
        img = image.get()
        self.image_button.configure(image=img)



    def download(self, _event=None):
        if self.image_to_download:
            directory = os.path.expanduser("~") + "/Desktop/chat"
            if not os.path.exists(directory):
                os.makedirs(directory)

            filename = filedialog.asksaveasfilename(initialdir=directory, filetypes=[("png", ".png")],
                                                    defaultextension=".png")
            if filename:
                shutil.move(os.path.join(directory, "image.png"), filename)
        else:
            print("No image to download")

    def switch(self,_event=None):
        i=self.switch_image.get()-1
        image=WebImage(self.links[i])
        img=image.get()
        self.image_button.configure(self,image=img)


    def record_button_event(self):
         if self.recording:
            self.recording = False
            self.record_button.configure(self,fg_color="grey")
            self.record_button.configure(self,border_color="red")
         else:
             self.recording=True
             self.record_button.configure(self,fg_color="red")
             self.record_button.configure(self,border_color="grey")
             threading.Thread(target=self.recorder).start()

    def recorder(self):
        audio=pyaudio.PyAudio()
        stream=audio.open(format=pyaudio.paInt16, channels=1,rate=44100,input=True,frames_per_buffer=1024)
        frames =[]


        while self.recording:
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()


        exists=True
        i=1
        while exists:
             if os.path.exists(f"myrecording{i}.wav"):
                 i+=1
             else:
                 exists=False

        sound_file=wave.open(f"myrecording{i}.wav","wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b''.join(frames))
        sound_file.close()
        self.audio_complete.delete("1.0","end")

        if self.translate.get()==1:
            audio_file=open(f"myrecording{i}.wav","rb")
            transcript = client.audio.translations.create(model="whisper-1",file=audio_file)
            self.audio_complete.insert(1.0,text=transcript.text)
        else:
            audio_file = open(f"myrecording{i}.wav", "rb")
            transcript = client.audio.transcriptions.create(model="whisper-1",file=audio_file)

            self.audio_complete.insert(1.0, text=transcript.text)


app = App()
app.mainloop()
