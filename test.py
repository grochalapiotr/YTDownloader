from tkinter import *
from pytube import *


master =Tk()



var_url=StringVar()
var_url.set('https://www.youtube.com/watch?v=E1OjQ_3kh4A')

url=var_url.get()
yt=YouTube(url)

res=[]
for i in yt.streams.filter(type="video"):
    if i.resolution not in res:
        res.append(i.resolution)
res.sort(reverse=True)
print(res)

variable=StringVar(master)
variable.set(res[0])

w=OptionMenu(master, variable, *res).pack()

for j in yt.streams.filter():    
    print(j)


mainloop()