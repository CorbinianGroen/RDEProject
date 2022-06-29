import tkinter as tk
import customtkinter as ct
from tkinter import ttk

def importwindow(master, widthfactor, heightfactor):

    config = open('Importconfig.txt')
    config_txt = config.readlines()
    config.close()

    Ar_config = config_txt[2].replace('\n', '').split()
    CO_config = config_txt[4].replace('\n', '').split()


    window = ct.CTkToplevel(master)
    #window.grab_set()
    window.title('Import Options')
    window.geometry(str(int(widthfactor*1200)) + 'x' + str(int(heightfactor*600)))
    window.resizable(False, False)

    window.grid_rowconfigure(0, minsize=10)
    window.grid_rowconfigure(1, weight=5)
    window.grid_rowconfigure(2, minsize=10)
    window.grid_rowconfigure(3, weight=0)
    window.grid_rowconfigure(4, minsize=10)

    window.grid_columnconfigure(0, minsize=10)
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, minsize=10)

    InputFrame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    InputFrame.grid(row=1, column=1, sticky='nswe')

    InputFrame.grid_rowconfigure(0, weight=1, minsize=100)
    InputFrame.grid_columnconfigure(0, weight=1)
    InputFrame.grid_rowconfigure(1, weight=1, minsize=100)
    InputFrame.grid_rowconfigure(2, weight=1, minsize=150)
    InputFrame.grid_rowconfigure(3, weight=1, minsize=150)
    InputFrame.grid_rowconfigure(4, minsize=10)

    ArFrame = ct.CTkFrame(master=InputFrame, corner_radius=10, fg_color=('grey90', 'grey10'))
    ArFrame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10)
    COFrame = ct.CTkFrame(master=InputFrame, corner_radius=10, fg_color=('grey90', 'grey10'))
    COFrame.grid(row=1, column=0, sticky='nswe', padx=10)
    ORRFrame = ct.CTkFrame(master=InputFrame, corner_radius=10, fg_color=('grey90', 'grey10'))
    ORRFrame.grid(row=2, column=0, sticky='nswe', padx=10, pady=10)
    HORFrame = ct.CTkFrame(master=InputFrame, corner_radius=10, fg_color=('grey90', 'grey10'))
    HORFrame.grid(row=3, column=0, sticky='nswe', padx=10)

    #ArFrame Inputs
    ArFrame.grid_rowconfigure(0, minsize=10, weight=0)
    ArFrame.grid_rowconfigure(1, minsize=30, weight=0)
    ArFrame.grid_rowconfigure(2, minsize=30, weight=1)
    ArFrame.grid_rowconfigure(3, minsize=10, weight=0)
    ArFrame.grid_columnconfigure(0, minsize=10)
    ArFrame.grid_columnconfigure(17, minsize=10)
    ct.CTkLabel(master=ArFrame, text='Ar CV:', text_font=("Calibri", -18), width=1).grid(row=1, column=1, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Scantype:', text_font=("Calibri", -18), width=1).grid(row=2, column=1, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Scan Rate:', text_font=("Calibri", -18), width=1).grid(row=2, column=3, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Scan:', text_font=("Calibri", -18), width=1).grid(row=2, column=5, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Sep:', text_font=("Calibri", -18), width=1).grid(row=2, column=7, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Header:', text_font=("Calibri", -18), width=1).grid(row=2, column=9, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Decimal:', text_font=("Calibri", -18), width=1).grid(row=2, column=11, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Skip:', text_font=("Calibri", -18), width=1).grid(row=2, column=13, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Pot Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=15, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Cur Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=17, sticky=tk.W)

    Scans = ("Single", "Multiple")
    ArScan_var = ct.StringVar()
    ArScan = ct.CTkOptionMenu(master=ArFrame, variable=ArScan_var, values=Scans)
    ArScan.config(width=80, fg_color=('grey70', 'grey30'), button_color=('grey70', 'grey30'),button_hover_color=('grey70', 'grey30'))
    ArScan.set(Ar_config[0])
    ArScan.grid(row=2, column=2, sticky=tk.W)

    ArScanRate= ct.CTkEntry(master=ArFrame, width=50)
    ArScanRate.grid(row=2, column=4, sticky=tk.W)
    ArScanRate.insert(0, Ar_config[1])

    ArScanNumber = ct.CTkEntry(master=ArFrame, width=30)
    ArScanNumber.grid(row=2, column=6, sticky=tk.W)
    ArScanNumber.insert(0, Ar_config[2])

    Seperators = (";", "spaces", "tabs")
    ArSep_var = ct.StringVar()
    ArSep = ct.CTkOptionMenu(master=ArFrame, variable=ArSep_var, values=Seperators)
    ArSep.config(width=50, fg_color=('grey70', 'grey30'), button_color=('grey70', 'grey30'),button_hover_color=('grey70', 'grey30'))
    ArSep.set(Ar_config[3])
    ArSep.grid(row=2, column=8, sticky=tk.W)

    Options = ('None', '0', '1', '2', '3', '4', '5', '6')
    ArOption_var = ct.StringVar()
    ArHead = ct.CTkComboBox(master=ArFrame, variable=ArOption_var, values=Options)
    ArHead.config(width=70, fg_color=('grey70', 'grey30'), button_color=('grey70', 'grey30'), button_hover_color=('grey70', 'grey30'))
    ArHead.set(Ar_config[4])
    ArHead.grid(row=2, column=10, sticky=tk.W)

    Decimals = ('.', ',')
    ArDecimal_var = ct.StringVar()
    ArDecimal = ct.CTkOptionMenu(master=ArFrame, variable=ArDecimal_var, values=Decimals)
    ArDecimal.config(width=50, fg_color=('grey70', 'grey30'), button_color=('grey70', 'grey30'), button_hover_color=('grey70', 'grey30'))
    ArDecimal.set(Ar_config[5])
    ArDecimal.grid(row=2, column=12, sticky=tk.W)

    ArSkip = ct.CTkEntry(master=ArFrame, width=10)
    ArSkip.grid(row=2, column=14, sticky=tk.W)
    ArSkip.insert(0, Ar_config[6])

    ArPot = ct.CTkEntry(master=ArFrame, width=30)
    ArPot.grid(row=2, column=16, sticky=tk.W)
    ArPot.insert(0, Ar_config[7])

    ArCur = ct.CTkEntry(master=ArFrame, width=30)
    ArCur.grid(row=2, column=18, sticky=tk.W)
    ArCur.insert(0, Ar_config[8])

    # COFrame Inputs
    COFrame.grid_rowconfigure(0, minsize=10)
    COFrame.grid_columnconfigure(0, minsize=10)
    COFrame.grid_columnconfigure(11, minsize=10)
    ct.CTkLabel(master=COFrame, text='CO CV:', text_font=("Calibri", -18), width=1).grid(row=1, column=1, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Sep:', text_font=("Calibri", -18), width=1).grid(row=2, column=1, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Header:', text_font=("Calibri", -18), width=1).grid(row=2, column=3, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Decimal:', text_font=("Calibri", -18), width=1).grid(row=2, column=5, sticky=tk.W)

    Seperators = (";", "spaces", "tabs")
    COSep_var = ct.StringVar()
    COSep = ttk.Combobox(COFrame, textvariable=COSep_var)
    COSep['values'] = Seperators
    COSep['state'] = 'readonly'
    COSep.config(width=5)
    COSep_var.set(CO_config[0])
    COSep.grid(row=2, column=2, sticky=tk.W)

    Options = ('None', '0', '1', '2', '3', '4', '5', '6')
    COOption_var = ct.StringVar()
    COHead = ttk.Combobox(COFrame, textvariable=COOption_var)
    COHead['values'] = Options
    COOption_var.set(CO_config[1])
    COHead.config(width=8)
    # COHead = ct.CTkComboBox(master=COFrame, variable=COOption_var, values=Options)
    # COHead.config(width=80, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey70', 'grey30'))
    COHead.grid(row=2, column=4, sticky=tk.W)

    Decimals = ('.', ',')
    CODecimal_var = ct.StringVar()
    CODecimal = ttk.Combobox(COFrame, textvariable=ArDecimal_var)
    CODecimal['values'] = Decimals
    CODecimal['state'] = 'readonly'
    CODecimal.config(width=5)
    CODecimal.grid(row=2, column=6, sticky=tk.W)
    CODecimal_var.set(CO_config[2])


    SaveFrame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    SaveFrame.grid(row=3, column=1, sticky='nswe')
    SaveFrame.grid_columnconfigure(0, weight=1)

    def save():

        SaveText = f'Import Configure File\n' \
                   f'Ar\n' \
                   f'{ArScan.get()}\t{ArScanRate.get()}\t{ArScanNumber.get()}\t{ArSep.get()}\t{ArHead.get()}\t{ArDecimal.get()}\t{ArSkip.get()}\t{ArPot.get()}\t{ArCur.get()}\n' \
                   f'CO\n' \
                   f'{COSep.get()}\t{COHead.get()}\t{CODecimal.get()}\n'


        config = open('Importconfig.txt', 'w')
        config.write(SaveText)
        config.close()


    SaveButton = ct.CTkButton(master=SaveFrame,text="Save", command=save, text_font=("Calibri", -18), width= 160, height= 10)
    SaveButton.grid(row=0, column=0, sticky=tk.E, pady=10, padx=10)

    window.mainloop()


#root = 1
#importwindow(root, 1, 1)