import tkinter as tk
from tkinter import ttk
from tkinter import *
import cx_Oracle
from tkinter import messagebox

LARGE_FONT= ("Verdana", 20, "bold")
NORMAL_FONT= ("Verdana", 14)
START_FONT= ("Times", 14)

class Tax(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self,*args, **kwargs)
        tk.Tk.wm_title(self, "Tax")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage (container, self)

        self.frames [StartPage] = frame

        frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame (StartPage)

    def show_frame (self, cont):

        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label (self, text="Salaries Tax Computation\nYear of assessment:2018/2019",
                          font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        label4 = tk.Label(self, text="Status:",
                          font=NORMAL_FONT)
        label4.place(x=1075, y=25)

        global ms
        ms = tk.StringVar()
        ycombo = ttk.Combobox(self, width=15, textvariable=ms)
        ycombo['values'] = ('Single', 'Married')
        ycombo.place(x=1075, y=55)

        label3 = tk.Label(self, text="Spouse:",
                          font=NORMAL_FONT)
        label3.place(x=750, y=90)

        label2 = tk.Label(self, text="Self:",
                          font=NORMAL_FONT)
        label2.place(x=550, y=90)

        label1 = tk.Label(self, text="Income for thr year of assessment:",
                         font=NORMAL_FONT)
        label1.place(x=150, y=120)

        global ics
        ics = tk.StringVar()
        unentry = tk.Entry(self, textvariable=ics, width=25, bg="white")
        unentry.place(x=550, y=125)


        global icm
        icm = tk.StringVar()
        unentry = tk.Entry(self, textvariable=icm, width=25, bg="white")
        unentry.place(x=750, y=125)

        label5 = tk.Label(self, text="Salaries Tax:",
                          font=NORMAL_FONT)
        label5.place(x=150, y=170)

        button = ttk.Button(self, text="Compute",
                            command=lambda: cs())

        button.place(x=550, y=170)

        def cs():

            try:
                val= int(ics.get())

                if( icm.get() == ''and ms.get()=='Married' ):
                    messagebox.showinfo(title='error', message='Select Single')
                elif(icm.get() != ''and ms.get()=='Single'):
                    messagebox.showinfo(title='error', message='Select Married')
                elif(ms.get()=='Married'):
                    cst()
                elif(ms.get()=='Single'):
                    cst1()
                else:
                    messagebox.showinfo(title='error', message='Select your status')
            except ValueError:
                messagebox.showinfo(title='error', message='Enter an interger')

        def cst():
            cstl=Toplevel()
            cstl.title("Computation of Estimated Salaries Tax Liabilities")

            label6 = tk.Label(cstl, text="Year of assessment 2018/2019", font=LARGE_FONT)
            label6.pack(pady=10, padx=10)

            label7 = tk.Label(cstl, text="Total Income:", font=NORMAL_FONT)
            label7.place(x=100,y=90)

            label11 = tk.Label(cstl, text="Self", font=NORMAL_FONT)
            label11.place(x=350, y=60)

            label11a = tk.Label(cstl, text="Spouse", font=NORMAL_FONT)
            label11a.place(x=650, y=60)

            label8 = tk.Label(cstl, text=ics.get(), font=NORMAL_FONT)
            label8.place(x=350, y=90)

            a = int(str(ics.get()))

            label9 = tk.Label(cstl, text="Mandatory:", font=NORMAL_FONT)
            label9.place(x=100, y=120)

            if (a * 5 / 100 < 7100):
                e = 0
            elif(a*5/100<18000):
                e=a*5/100
            else:
                e=18000

            label10 = tk.Label(cstl, text=e, font=NORMAL_FONT)
            label10.place(x=350, y=120)

            label12 = tk.Label(cstl, text="Allowances:", font=NORMAL_FONT)
            label12.place(x=100, y=150)

            label16 = tk.Label(cstl, text="----", font=NORMAL_FONT)
            label16.place(x=350, y=150)

            label13 = tk.Label(cstl, text="Basic:", font=NORMAL_FONT)
            label13.place(x=110, y=180)

            ba=132000

            label14 = tk.Label(cstl, text=ba, font=NORMAL_FONT)
            label14.place(x=350, y=180)

            label15 = tk.Label(cstl, text="Total Allowances:", font=NORMAL_FONT)
            label15.place(x=100, y=210)

            if (a > 900000):
                ta = e
            else:
                ta = ba + e

            label15 = tk.Label(cstl, text=ta, font=NORMAL_FONT)
            label15.place(x=350, y=210)

            label15 = tk.Label(cstl, text="Net Chargeable Income:", font=NORMAL_FONT)
            label15.place(x=100, y=240)


            if (a-ta>0):
                b = a - ta
            elif(a-ta<0):
                b=0

            label15 = tk.Label(cstl, text=b, font=NORMAL_FONT)
            label15.place(x=350, y=240)

            label15 = tk.Label(cstl, text="Tax before Reduction:", font=NORMAL_FONT)
            label15.place(x=100, y=270)

            if(b<50000):
                c=b*2/100
            elif(b==50000):
                c=1000
            elif(b>50000and b<100000):
                c=((b-50000)*6/100)+1000
            elif (b == 100000):
                c = 4000
            elif(b>100000and b<150000):
                c=((b-100000)*10/100)+4000
            elif (b == 150000):
                c = 9000
            elif(b>150000and b<200000):
                c=((b-150000)*14/100)+9000
            elif (b == 200000):
                c = 16000
            else:
                c=((b-200000)*17/100)+16000

            cc = b * 15 / 100

            if (cc > c):
                f = c
            elif (c > cc):
                f = cc
            else:
                f=c

            label15 = tk.Label(cstl, text=f, font=NORMAL_FONT)
            label15.place(x=350, y=270)

            label15 = tk.Label(cstl, text="Tax (you and your spouse):", font=NORMAL_FONT)
            label15.place(x=100, y=300)

            label15 = tk.Label(cstl, text="Tax Reduction", font=NORMAL_FONT)
            label15.place(x=100, y=330)

            label15 = tk.Label(cstl, text="Tax Payable", font=NORMAL_FONT)
            label15.place(x=100, y=360)

            label8a = tk.Label(cstl, text=icm.get(), font=NORMAL_FONT)
            label8a.place(x=650, y=90)

            a1 = int(str(icm.get()))

            if (a1 * 5 / 100 < 7100):
                e1 = 0
            elif (a1 * 5 / 100 < 18000):
                e1= a1 * 5 / 100
            else:
                e1 = 18000

            label10 = tk.Label(cstl, text=e1, font=NORMAL_FONT)
            label10.place(x=650, y=120)

            label16 = tk.Label(cstl, text="----", font=NORMAL_FONT)
            label16.place(x=650, y=150)

            ba1=132000

            label14 = tk.Label(cstl, text=ba1, font=NORMAL_FONT)
            label14.place(x=650, y=180)

            if (a1 > 900000):
                ta1 = e1
            else:
                ta1 = ba1 + e1


            label15 = tk.Label(cstl, text=ta1, font=NORMAL_FONT)
            label15.place(x=650, y=210)


            if (a1-ta1>0):
                b1 = a1 - ta1
            elif(a1-ta1<0):
                b1=0

            label15 = tk.Label(cstl, text=b1, font=NORMAL_FONT)
            label15.place(x=650, y=240)

            if (b1 < 50000):
                c1 = b1 * 2 / 100
            elif (b1 == 50000):
                c1 = 1000
            elif (b1 > 50000 and b1 < 100000):
                c1 = ((b1 - 50000) * 6 / 100) + 1000
            elif (b1 == 100000):
                c1 = 4000
            elif (b1 > 100000 and b1 < 150000):
                c1 = ((b1 - 100000) * 10 / 100) + 4000
            elif (b1 == 150000):
                c1 = 9000
            elif (b1 > 150000 and b1 < 200000):
                c1 = ((b1 - 150000) * 14 / 100) + 9000
            elif (b1 == 200000):
                c1 = 16000
            else:
                c1 = ((b1 - 200000) * 17 / 100) + 16000

            cc1 = b1 * 15 / 100

            if (cc1 > c1):
                f1 = c1
            elif (c1 > cc1):
                f1 = cc1
            else:
                f1=c1

            label15 = tk.Label(cstl, text=f1, font=NORMAL_FONT)
            label15.place(x=650, y=270)

            label15 = tk.Label(cstl, text=f+f1, font=NORMAL_FONT)
            label15.place(x=500, y=300)

            label11a = tk.Label(cstl, text="Joint Assessment", font=NORMAL_FONT)
            label11a.place(x=950, y=61)

            a2=a+a1

            label8 = tk.Label(cstl, text=a2, font=NORMAL_FONT)
            label8.place(x=950, y=90)

            e2=e+e1

            label10 = tk.Label(cstl, text=e2, font=NORMAL_FONT)
            label10.place(x=950, y=120)

            label16 = tk.Label(cstl, text="----", font=NORMAL_FONT)
            label16.place(x=950, y=150)

            ba2 = 264000

            label14 = tk.Label(cstl, text=ba2, font=NORMAL_FONT)
            label14.place(x=950, y=180)

            if (a2 > 1800000):
                ta2 = e2
            else:
                ta2 = ba2 + e2


            label15 = tk.Label(cstl, text=ta2, font=NORMAL_FONT)
            label15.place(x=950, y=210)

            if (a2-ta2>0):
                b2 = a2 - ta2
            elif(a2-ta2<0):
                b2=0


            label15 = tk.Label(cstl, text=b2, font=NORMAL_FONT)
            label15.place(x=950, y=240)

            if (b2 < 50000):
                c2 = b2 * 2 / 100
            elif (b2 == 50000):
                c2 = 1000
            elif (b2 > 50000 and b2 < 100000):
                c2 = ((b2 - 50000) * 6 / 100) + 1000
            elif (b2 == 100000):
                c2 = 4000
            elif (b2 > 100000 and b2 < 150000):
                c2 = ((b2 - 100000) * 10 / 100) + 4000
            elif (b2 == 150000):
                c2 = 9000
            elif (b2 > 150000 and b2 < 200000):
                c2 = ((b2 - 150000) * 14 / 100) + 9000
            elif (b2 == 200000):
                c2 = 16000
            else:
                c2 = ((b2 - 200000) * 17 / 100) + 16000

            cc2 = b2 * 15 / 100

            if (cc2 > c2):
                f2 = c2
            elif (c2 > cc2):
                f2 = cc2
            else:
                f2=c2

            label15 = tk.Label(cstl, text=f2, font=NORMAL_FONT)
            label15.place(x=950, y=270)

            label15 = tk.Label(cstl, text=f2, font=NORMAL_FONT)
            label15.place(x=950, y=300)

            if(f2 < f+f1):
                if ((f2*75/100)<20000):
                    d2 = round(f2 * 75 / 100)
                else:
                    d2 = 20000

                label15 = tk.Label(cstl, text=d2, font=NORMAL_FONT)
                label15.place(x=950, y=330)

                label15 = tk.Label(cstl, text=f2 - d2, font=NORMAL_FONT)
                label15.place(x=950, y=360)

            elif(f+f1 < f2):
                if ((f1*75/100)<20000):
                    d1 = round(f1 * 75 / 100)
                else:
                    d1 = 20000

                label15 = tk.Label(cstl, text=d1, font=NORMAL_FONT)
                label15.place(x=650, y=330)

                label15 = tk.Label(cstl, text=f1 - d1, font=NORMAL_FONT)
                label15.place(x=650, y=360)

                if ((f*75/100)<20000):
                    d = round(f * 75 / 100)
                else:
                    d = 20000

                label15 = tk.Label(cstl, text=d, font=NORMAL_FONT)
                label15.place(x=350, y=330)

                label15 = tk.Label(cstl, text=f - d, font=NORMAL_FONT)
                label15.place(x=350, y=360)

            else:
                if ((f2*75/100)<20000):
                    d2 = round(f2 * 75 / 100)
                else:
                    d2 = 20000

                label15 = tk.Label(cstl, text=d2, font=NORMAL_FONT)
                label15.place(x=950, y=330)

                label15 = tk.Label(cstl, text=f2 - d2, font=NORMAL_FONT)
                label15.place(x=950, y=360)

                if ((f1*75/100)<20000):
                    d1 = round(f1 * 75 / 100)
                else:
                    d1 = 20000

                label15 = tk.Label(cstl, text=d1, font=NORMAL_FONT)
                label15.place(x=650, y=330)

                label15 = tk.Label(cstl, text=f1 - d1, font=NORMAL_FONT)
                label15.place(x=650, y=360)

                if ((f*75/100)<20000):
                    d = round(f * 75 / 100)
                else:
                    d = 20000

                label15 = tk.Label(cstl, text=d, font=NORMAL_FONT)
                label15.place(x=350, y=330)

                label15 = tk.Label(cstl, text=f - d, font=NORMAL_FONT)
                label15.place(x=350, y=360)




            cstl.geometry("1280x720")
            cstl.mainloop()

        def cst1():
            cstl1 = Toplevel()
            cstl1.title("Computation of Estimated Salaries Tax Liabilities")

            label6 = tk.Label(cstl1, text="Year of assessment 2018/2019", font=LARGE_FONT)
            label6.pack(pady=10, padx=10)

            label7 = tk.Label(cstl1, text="Total Income:", font=NORMAL_FONT)
            label7.place(x=100, y=90)

            label11 = tk.Label(cstl1, text="Self", font=NORMAL_FONT)
            label11.place(x=350, y=60)

            label8 = tk.Label(cstl1, text=ics.get(), font=NORMAL_FONT)
            label8.place(x=350, y=91)

            a = int(str(ics.get()))

            label9 = tk.Label(cstl1, text="Mandatory:", font=NORMAL_FONT)
            label9.place(x=100, y=120)

            if(a*5/100<7100):
                e=0
            elif(a*5/100<18000):
                e=a*5/100
            else:
                e=18000

            label10 = tk.Label(cstl1, text=e, font=NORMAL_FONT)
            label10.place(x=350, y=121)

            label12 = tk.Label(cstl1, text="Allowances:", font=NORMAL_FONT)
            label12.place(x=100, y=150)

            label16 = tk.Label(cstl1, text="----", font=NORMAL_FONT)
            label16.place(x=350, y=150)

            label13 = tk.Label(cstl1, text="Basic:", font=NORMAL_FONT)
            label13.place(x=110, y=180)

            ba = 132000

            label14 = tk.Label(cstl1, text=ba, font=NORMAL_FONT)
            label14.place(x=350, y=180)

            label15 = tk.Label(cstl1, text="Total Allowances:", font=NORMAL_FONT)
            label15.place(x=100, y=210)

            if(a>900000):
                ta = e
            else:
                ta = ba + e

            label15 = tk.Label(cstl1, text=ta, font=NORMAL_FONT)
            label15.place(x=350, y=210)

            label15 = tk.Label(cstl1, text="Net Chargeable Income:", font=NORMAL_FONT)
            label15.place(x=100, y=240)


            if (a-ta>0):
                b = a - ta
            elif(a-ta<0):
                b=0

            label15 = tk.Label(cstl1, text=b, font=NORMAL_FONT)
            label15.place(x=350, y=240)

            label15 = tk.Label(cstl1, text="Tax before Reduction:", font=NORMAL_FONT)
            label15.place(x=100, y=270)

            if (b < 50000):
                c = b * 2 / 100
            elif (b == 50000):
                c = 1000
            elif (b > 50000 and b < 100000):
                c = ((b - 50000) * 6 / 100) + 1000
            elif (b == 100000):
                c = 4000
            elif (b > 100000 and b < 150000):
                c = ((b - 100000) * 10 / 100) + 4000
            elif (b == 150000):
                c = 9000
            elif (b > 150000 and b < 200000):
                c = ((b - 150000) * 14 / 100) + 9000
            elif (b == 200000):
                c = 16000
            else:
                c = ((b - 200000) * 17 / 100) + 16000

            cc=b*15/100

            if (cc>c):
                f=c
            elif(c>cc):
                f=cc
            else:
                f=c

            label15 = tk.Label(cstl1, text=f, font=NORMAL_FONT)
            label15.place(x=350, y=270)

            label15 = tk.Label(cstl1, text="Tax Reduction", font=NORMAL_FONT)
            label15.place(x=100, y=300)

            if ((f*75/100)<20000):
                d = round(f * 75 / 100)
            else:
                d = 20000

            label15 = tk.Label(cstl1, text=d, font=NORMAL_FONT)
            label15.place(x=350, y=300)

            label15 = tk.Label(cstl1, text="Tax Payable", font=NORMAL_FONT)
            label15.place(x=100, y=330)

            label15 = tk.Label(cstl1, text=f - d, font=NORMAL_FONT)
            label15.place(x=350, y=330)

            cstl1.geometry("960x720")
            cstl1.mainloop()

app = Tax()
app.geometry("1280x720")
app.mainloop()