from tkinter import*
from tkinter import ttk
from pytube import*
from PIL import Image,ImageTk
import requests
import io
import os

class Youtube_app:
    def __init__(self, root):
        self.root=root
        self.root.title("Youtube Downloader")
        self.root.geometry("600x420+300+50")
        self.root.resizable(False, False)
        self.root.config(bg='white')
        os.chdir(os.path.dirname(os.path.realpath(__file__)))  #set downloading path to default where the program is

        title = Label(self.root,text='Youtube Downloader', font=("times new roman",15), bg='grey', fg='white', anchor='w').pack(side=TOP, fill=X)

        self.var_url=StringVar()
        lbl_url = Label(self.root, text='Video URL', font=("times new roman", 15), bg='white').place(x=10,y=50)
        txt_url = Entry(self.root, font=("times new roman", 13), textvariable=self.var_url, bg='lightyellow').place(x=120,y=50,width=440 )
        lbl_filetype = Label(self.root, text='File Type', font=("times new roman", 15), bg='white').place(x=10,y=900)

        self.var_fileType=StringVar()
        self.var_fileType.set('Video')
        video_radio = Radiobutton(self.root, text='Video', variable=self.var_fileType, value='Video', font=("times new roman", 15), bg='white', activebackground='white').place(x=120,y=90)
        audio_radio = Radiobutton(self.root, text='Audio', variable=self.var_fileType, value='Audio', font=("times new roman", 15), bg='white', activebackground='white').place(x=220,y=90)

#=============dropdown menu===============
        self.dropdown_menu = OptionMenu(self.root, variable='', value='')
        self.dropdown_menu.place(x=350, y=90)
#=========================================

        btn_search=Button(self.root, text='Search', command=self.search, font=("times new roman", 15), bg='white').place(x=458, y=90, height=25, width=100)

        self.frame1 = Frame(self.root, bd=2, relief=RIDGE, bg='lightyellow')
        self.frame1.place(x=10, y=130, width=580, height=180)

        self.video_title = Label(self.frame1 ,text='Video Title Here', font=("times new roman",15), bg='lightgrey', anchor='w')
        self.video_title.place(x=0, y=0, relwidth=1)

        self.video_image = Label(self.frame1, text='Video \nImage', font=("times new roman", 15), bg='lightgrey', bd=2, relief=FLAT)
        self.video_image.place(x=5, y=30, width=170, height=95)

        lbl_desc = Label(self.frame1, text='Description', font=("times new roman", 15), bg='lightyellow').place(x=190, y=30)

        self.video_desc = Text(self.frame1, font=("times new roman", 12), bg='lightyellow')
        self.video_desc.place(x=190, y=60, width=280, height=110)

        self.lbl_size = Label(self.root, text='Total Size: MB', font=("times new roman", 13), bg='white')
        self.lbl_size.place(x=10, y=320)

        self.lbl_percentage = Label(self.root, text='Downloading: 0%', font=("times new roman", 13), bg='white')
        self.lbl_percentage.place(x=170, y=320)

        btn_clear = Button(self.root, text='Clear', command=self.clear, font=("times new roman", 15), bg='gray').place(x=320, y=320, height=25, width=70)
        self.btn_download = Button(self.root, text='Download', state=DISABLED, command=self.download, font=("times new roman", 15), bg='green')
        self.btn_download.place(x=400, y=320, height=25, width=90)

        self.prog=ttk.Progressbar(self.root, orient=HORIZONTAL, length=590, mode='determinate')
        self.prog.place(x=10, y=360, width=580, height=20)

        self.lbl_message = Label(self.root, text='Error Messages', font=("times new roman", 13), bg='white')
        self.lbl_message.place(x=0, y=385, relwidth=1)
        #=====making directory for files=======
        if os.path.exists('Audios')==False:
            os.mkdir('Audios')
        if os.path.exists('Videos')==False:
             os.mkdir('Videos')

#=============================================
    def search(self):
        if self.var_url.get()=='':
            self.lbl_message.config(text='Video URL is required', fg='red')
        else:
            self.lbl_message.config(text='Error Messages', fg='black')
            url = self.var_url.get()
            self.yt = YouTube(url)

            title = self.yt.title
            thumbnail = self.yt.thumbnail_url
            #==========fetching image=====
            response=requests.get(thumbnail)
            img_byte=io.BytesIO(response.content)
            self.img=Image.open(img_byte)
            self.img=self.img.resize((180, 140), Image.ANTIALIAS)
            self.img=ImageTk.PhotoImage(self.img)
            #self.video_image.config(image=self.img)
            self.video_image = Label(self.frame1, image=self.img, bd=2, relief=FLAT)
            self.video_image.place(x=5, y=30, width=180, height=140)

            desc = self.yt.description[:200]

            #==========determine if file is audio or video=======
            if self.var_fileType.get()=='Audio':
                self.select_file = self.yt.streams.filter(only_audio=True).first()  #audio type file
            if self.var_fileType.get()=='Video':                    #video type file    
                #=============dropdown menu===============
                
                self.res=[]
                for i in self.yt.streams.filter(type="video", progressive=True):
                    if i.resolution not in self.res:
                        self.res.append(i.resolution)
                self.res.sort(reverse=True)
                self.var_res=StringVar()
                self.var_res.set(self.res[0])    #default value
                self.dropdown_menu.destroy()
                self.dropdown_menu = OptionMenu(self.root, self.var_res, *self.res, command=self.res_select)
                self.dropdown_menu.place(x=350, y=90)
                self.select_file = self.yt.streams.filter(res=self.var_res.get()).first()  
                
                #=========================================

            #=========updating frame elements======
            self.size_inBytes=self.select_file.filesize
            max_size=self.size_inBytes/1024000
            self.mb=str(round(max_size, 2))+'MB'
            self.lbl_size.config(text='Total Size: '+self.mb)

            self.video_title.config(text=title)
            self.video_desc.delete('1.0',END)
            self.video_desc.insert(END,desc)

            self.btn_download.config(state=NORMAL)


    def progress_(self, streams, chunk, bytes_remaining):
        percentage=(float(abs(bytes_remaining-self.size_inBytes)/self.size_inBytes))*float(100)
        self.prog['value']=percentage
        self.prog.update()
        self.lbl_percentage.config(text=f'Downloading: {str(round(percentage, 2))}%')
        if round(percentage, 2)==100:
            self.lbl_message.config(text='Download Completed', fg='green')
            self.btn_download.config(state=DISABLED)

    def download(self):
        yt=YouTube(self.var_url.get(), on_progress_callback=self.progress_)
        # ==========determine if file is audio or video=======
        if self.var_fileType.get() == 'Audio':
            select_file = yt.streams.filter(only_audio=True).first()  # audio type file
            select_file.download('Audios/')
        if self.var_fileType.get() == 'Video':
            select_file = yt.streams.filter(progressive=True, res=self.var_res.get()).first()  # video type file
            select_file.download('Videos/')

    def clear(self):
        self.var_fileType.set('Video')
        self.var_url.set('')
        self.prog['value']=0
        self.btn_download.config(state=NORMAL)
        self.lbl_message.config(text='Error Messages')
        self.video_title.config(text='Video Title Here')
        self.video_image = Label(self.frame1, text='Video \nImage', font=("times new roman", 15), bg='lightgrey', bd=2, relief=FLAT)
        self.video_image.place(x=5, y=30, width=180, height=140)
        self.video_desc.delete('1.0', END)
        self.lbl_size.config(text='Total Size: MB')
        self.lbl_percentage.config(text='Downloading: 0%')
        self.dropdown_menu.destroy()
        self.dropdown_menu = OptionMenu(self.root, variable='', value='')
        self.dropdown_menu.place(x=350, y=90)

    def res_select(self, click):
        print(click)
        self.select_file = self.yt.streams.filter(res=click).first()
        self.size_inBytes=self.select_file.filesize
        max_size=self.size_inBytes/1024000
        self.mb=str(round(max_size, 2))+'MB'
        self.lbl_size.config(text='Total Size: '+self.mb)
        
root=Tk()
obj=Youtube_app(root)
root.mainloop()