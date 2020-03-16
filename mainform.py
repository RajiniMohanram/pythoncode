from tkinter import *
from tkinter.ttk import *

from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

from scrap import scrape
from opinion_mining_training_module import sentiment_analysis
import opinion_mining_training_module

reviews=[]

window = Tk()
window.title("Welcome to LikeGeeks app")
window.geometry('800x500')

lbl = Label(window, text="Enter the URL")
lblp = Label(window, text="")
lbln = Label(window, text="")
txt = Entry(window,width=30)
btn = Button(window, text="Click Me", command=clicked)

lbl.place(x=10,y=10)
lblp.place(x=550, y=100)
lbln.place(x=550, y=150)
txt.place(x=100,y=10)
btn.place(x=300,y=10)
txt.focus()

# sample URL='https://www.amazon.com/Moto-PLUS-5th-Generation-Exclusive/product-reviews/B0785NN142/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber='
def clicked():
    progress = Progressbar(window, orient = HORIZONTAL, length = 100, mode = 'determinate')
    progress.pack(pady = 10)
    progress.place(x=350,y=250)
    for i in range(1,6):
        progress['value'] = i*20
        window.update_idletasks()
        m=scrape(i,txt.get())
        for rv in m:
            reviews.append(rv)
        
    progress.destroy()
    df=sentiment_analysis(reviews)
    
    figure2 = plt.Figure(figsize=(6,5), dpi=70)
    ax2 = figure2.add_subplot(111)
    line2 = FigureCanvasTkAgg(figure2, window)
    #line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    line2.get_tk_widget().place(x=50,y=100)
    #df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
    df.plot(kind='line', legend=True,y='Positive', ax=ax2, color='red', fontsize=10)
    df.plot(kind='line', legend=True,y='Negative', ax=ax2, color='blue', fontsize=10)
    df.plot(kind='line', legend=True,y='Neutral', ax=ax2, color='black', fontsize=10)
    pos = opinion_mining_training_module.pos
    neg = opinion_mining_training_module.neg
    
    lblp.configure(text="Positive: "+str((pos*100)/(pos+neg)))
    lbln.configure(text="Negative: "+str((neg*100)/(pos+neg)))
    ax2.set_title('Review Status')


window.mainloop()