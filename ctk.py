import customtkinter

class Test(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Test")
        self.geometry("1000x500")
        self.bg_frame=customtkinter.CTkFrame(self,fg_color="firebrick2")
        self.bg_frame.grid(row=0,column=0)
        self.bg_frame = customtkinter.CTkFrame(self)
        self.bg_frame.grid(row=1, column=0)
        self.bg_frame = customtkinter.CTkFrame(self,fg_color="green")
        self.bg_frame.grid(row=2, column=0)

        self.bg_frame = customtkinter.CTkFrame(self, fg_color="green")
        self.bg_frame.grid(row=0, column=1)

        self.bg_frame = customtkinter.CTkFrame(self, fg_color="yellow")
        self.bg_frame.grid(row=0, column=2)

        self.grid_columnconfigure((0,1,2), weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2,weight=0)

test=Test()
test.mainloop()
