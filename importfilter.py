import tkinter as tk
import customtkinter as ct

def importwindow(master, widthfactor, heightfactor):

    config = open('Importconfig.txt')
    config_txt = config.readlines()
    config.close()

    Ar_config = config_txt[2].replace('\n', '').split()
    CO_config = config_txt[4].replace('\n', '').split()
    ORR_config = config_txt[6].replace('\n', '').split()
    ORRa_config = config_txt[8].replace('\n', '').split()

    #window = ct.CTkToplevel(master)
    window = master
    #window.grab_set()
    window.title('Import Options')
    window.geometry(str(int(widthfactor*1400)) + 'x' + str(int(heightfactor*600)))
    #window.resizable(False, False)

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

    InputFrame.grid_columnconfigure(0, weight=1)
    InputFrame.grid_rowconfigure(0, weight=1, minsize=100)
    InputFrame.grid_rowconfigure(1, weight=1, minsize=80)
    InputFrame.grid_rowconfigure(2, weight=1, minsize=160)
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
    ArFrame.grid_columnconfigure(19, minsize=10)
    ct.CTkLabel(master=ArFrame, text='Ar CV:', text_font=("Calibri", -18), width=1).grid(row=1, column=1, sticky=tk.W, columnspan=3)
    ct.CTkLabel(master=ArFrame, text='Scantype:', text_font=("Calibri", -18), width=1).grid(row=2, column=1, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Scan Rate:', text_font=("Calibri", -18), width=1).grid(row=2, column=3, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Scan:', text_font=("Calibri", -18), width=1).grid(row=2, column=5, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Sep:', text_font=("Calibri", -18), width=1).grid(row=2, column=7, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Header:', text_font=("Calibri", -18), width=1).grid(row=2, column=9, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Decimal:', text_font=("Calibri", -18), width=1).grid(row=2, column=11, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Skip:', text_font=("Calibri", -18), width=1).grid(row=2, column=13, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Pot Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=15, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='', text_font=("Calibri", -18), width=1).grid(row=2, column=17, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='Cur Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=19, sticky=tk.W)
    ct.CTkLabel(master=ArFrame, text='', text_font=("Calibri", -18), width=1).grid(row=2, column=21, sticky=tk.W)

    Scans = ("Single", "Multiple")
    ArScan_var = ct.StringVar()
    ArScan = ct.CTkOptionMenu(master=ArFrame, variable=ArScan_var, values=Scans)
    ArScan.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'),button_hover_color=('grey80', 'grey20'))
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
    ArSep.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ArSep.set(Ar_config[3])
    ArSep.grid(row=2, column=8, sticky=tk.W)

    Options = ('None', '0', '1', '2', '3', '4', '5', '6')
    ArOption_var = ct.StringVar()
    ArHead = ct.CTkComboBox(master=ArFrame, variable=ArOption_var, values=Options)
    ArHead.configure(width=70, fg_color=('grey90', 'grey10'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'), border_color=('grey80', 'grey20'))
    ArHead.set(Ar_config[4])
    ArHead.grid(row=2, column=10, sticky=tk.W)

    Decimals = ('.', ',')
    ArDecimal_var = ct.StringVar()
    ArDecimal = ct.CTkOptionMenu(master=ArFrame, variable=ArDecimal_var, values=Decimals)
    ArDecimal.config(width=50, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ArDecimal.set(Ar_config[5])
    ArDecimal.grid(row=2, column=12, sticky=tk.W)

    ArSkip = ct.CTkEntry(master=ArFrame, width=30)
    ArSkip.grid(row=2, column=14, sticky=tk.W)
    ArSkip.insert(0, Ar_config[6])

    ArPot = ct.CTkEntry(master=ArFrame, width=30)
    ArPot.grid(row=2, column=16, sticky=tk.W)
    ArPot.insert(0, Ar_config[7])

    Unit = ("V", "mV", "µV")
    ArV_var = ct.StringVar()
    ArV = ct.CTkOptionMenu(master=ArFrame, variable=ArV_var, values=Unit)
    ArV.config(width=30, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ArV.set(Ar_config[8])
    ArV.grid(row=2, column=18, sticky=tk.W)

    ArCur = ct.CTkEntry(master=ArFrame, width=30)
    ArCur.grid(row=2, column=20, sticky=tk.W)
    ArCur.insert(0, Ar_config[9])

    Unit_1 = ("A", "mA", "µA")
    ArA_var = ct.StringVar()
    ArA = ct.CTkOptionMenu(master=ArFrame, variable=ArA_var, values=Unit_1)
    ArA.config(width=30, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ArA.set(Ar_config[10])
    ArA.grid(row=2, column=22, sticky=tk.W)




    # COFrame Inputs
    COFrame.grid_rowconfigure(0, minsize=10)
    COFrame.grid_rowconfigure(3, minsize=10)
    COFrame.grid_columnconfigure(0, minsize=10)
    COFrame.grid_columnconfigure(11, minsize=10)
    ct.CTkLabel(master=COFrame, text='CO CV:', text_font=("Calibri", -18), width=1).grid(row=1, column=1, sticky=tk.W, columnspan=3)
    ct.CTkLabel(master=COFrame, text='Sep:', text_font=("Calibri", -18), width=1).grid(row=2, column=1, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Header:', text_font=("Calibri", -18), width=1).grid(row=2, column=3, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Decimal:', text_font=("Calibri", -18), width=1).grid(row=2, column=5, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Skip:', text_font=("Calibri", -18), width=1).grid(row=2, column=7, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Pot Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=9, sticky=tk.W)
    ct.CTkLabel(master=COFrame, text='Cur Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=11, sticky=tk.W)

    Seperators = (";", "spaces", "tabs")
    COSep_var = ct.StringVar()
    COSep = ct.CTkOptionMenu(master=COFrame, variable=COSep_var, values=Seperators)
    COSep.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    COSep.set(CO_config[0])
    COSep.grid(row=2, column=2, sticky=tk.W)

    Options = ('None', '0', '1', '2', '3', '4', '5', '6')
    COOption_var = ct.StringVar()
    COHead = ct.CTkComboBox(master=COFrame, variable=COOption_var, values=Options)
    COHead.configure(width=70, fg_color=('grey90', 'grey10'), button_color=('grey80', 'grey20'),button_hover_color=('grey80', 'grey20'), border_color=('grey80', 'grey20'))
    COHead.set(CO_config[1])
    COHead.grid(row=2, column=4, sticky=tk.W)

    Decimals = ('.', ',')
    CODecimal_var = ct.StringVar()
    CODecimal = ct.CTkOptionMenu(master=COFrame, variable=CODecimal_var, values=Decimals)
    CODecimal.config(width=50, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    CODecimal.set(CO_config[2])
    CODecimal.grid(row=2, column=6, sticky=tk.W)

    COSkip = ct.CTkEntry(master=COFrame, width=30)
    COSkip.grid(row=2, column=8, sticky=tk.W)
    COSkip.insert(0, CO_config[3])

    COPot = ct.CTkEntry(master=COFrame, width=30)
    COPot.grid(row=2, column=10, sticky=tk.W)
    COPot.insert(0, CO_config[4])

    COCur = ct.CTkEntry(master=COFrame, width=30)
    COCur.grid(row=2, column=12, sticky=tk.W)
    COCur.insert(0, CO_config[5])

    #ORR inputs
    ORRFrame.grid_rowconfigure(0, minsize=10, weight=0)
    ORRFrame.grid_rowconfigure(1, minsize=30, weight=0)
    ORRFrame.grid_rowconfigure(2, minsize=30, weight=1)
    ORRFrame.grid_rowconfigure(3, minsize=30, weight=0)
    ORRFrame.grid_rowconfigure(4, minsize=30, weight=1)
    ORRFrame.grid_rowconfigure(5, minsize=10, weight=0)
    ORRFrame.grid_columnconfigure(0, minsize=10)
    ORRFrame.grid_columnconfigure(19, minsize=10)
    ct.CTkLabel(master=ORRFrame, text='ORR O2 Scan:', text_font=("Calibri", -18), width=1).grid(row=1, column=1, sticky=tk.W, columnspan=3)
    ct.CTkLabel(master=ORRFrame, text='Scantype:', text_font=("Calibri", -18), width=1).grid(row=2, column=1, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Scan Rate:', text_font=("Calibri", -18), width=1).grid(row=2, column=3, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Scan:', text_font=("Calibri", -18), width=1).grid(row=2, column=5, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Sep:', text_font=("Calibri", -18), width=1).grid(row=2, column=7, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Header:', text_font=("Calibri", -18), width=1).grid(row=2, column=9, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Decimal:', text_font=("Calibri", -18), width=1).grid(row=2, column=11, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Skip:', text_font=("Calibri", -18), width=1).grid(row=2, column=13, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Pot Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=15, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Cur Column:', text_font=("Calibri", -18), width=1).grid(row=2, column=17, sticky=tk.W)

    Scans = ("LSV","Single", "Multiple")
    ORRScan_var = ct.StringVar()
    ORRScan = ct.CTkOptionMenu(master=ORRFrame, variable=ORRScan_var, values=Scans)
    ORRScan.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ORRScan.set(ORR_config[0])
    ORRScan.grid(row=2, column=2, sticky=tk.W)

    ORRScanRate = ct.CTkEntry(master=ORRFrame, width=50)
    ORRScanRate.grid(row=2, column=4, sticky=tk.W)
    ORRScanRate.insert(0, ORR_config[1])

    ORRScanNumber = ct.CTkEntry(master=ORRFrame, width=30)
    ORRScanNumber.grid(row=2, column=6, sticky=tk.W)
    ORRScanNumber.insert(0, ORR_config[2])

    Seperators = (";", "spaces", "tabs")
    ORRSep_var = ct.StringVar()
    ORRSep = ct.CTkOptionMenu(master=ORRFrame, variable=ORRSep_var, values=Seperators)
    ORRSep.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ORRSep.set(ORR_config[3])
    ORRSep.grid(row=2, column=8, sticky=tk.W)

    Options = ('None', '0', '1', '2', '3', '4', '5', '6')
    ORROption_var = ct.StringVar()
    ORRHead = ct.CTkComboBox(master=ORRFrame, variable=ORROption_var, values=Options)
    ORRHead.configure(width=70, fg_color=('grey90', 'grey10'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'), border_color=('grey80', 'grey20'))
    ORRHead.set(ORR_config[4])
    ORRHead.grid(row=2, column=10, sticky=tk.W)

    Decimals = ('.', ',')
    ORRDecimal_var = ct.StringVar()
    ORRDecimal = ct.CTkOptionMenu(master=ORRFrame, variable=ORRDecimal_var, values=Decimals)
    ORRDecimal.config(width=50, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ORRDecimal.set(ORR_config[5])
    ORRDecimal.grid(row=2, column=12, sticky=tk.W)

    ORRSkip = ct.CTkEntry(master=ORRFrame, width=30)
    ORRSkip.grid(row=2, column=14, sticky=tk.W)
    ORRSkip.insert(0, ORR_config[6])

    ORRPot = ct.CTkEntry(master=ORRFrame, width=30)
    ORRPot.grid(row=2, column=16, sticky=tk.W)
    ORRPot.insert(0, ORR_config[7])

    ORRCur = ct.CTkEntry(master=ORRFrame, width=30)
    ORRCur.grid(row=2, column=18, sticky=tk.W)
    ORRCur.insert(0, ORR_config[8])

    # ORR_Ar inputs
    ct.CTkLabel(master=ORRFrame, text='ORR Ar Scan:', text_font=("Calibri", -18), width=1).grid(row=3, column=1, sticky=tk.W, columnspan=3)
    ct.CTkLabel(master=ORRFrame, text='Scantype:', text_font=("Calibri", -18), width=1).grid(row=4, column=1, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Scan Rate:', text_font=("Calibri", -18), width=1).grid(row=4, column=3, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Scan:', text_font=("Calibri", -18), width=1).grid(row=4, column=5, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Sep:', text_font=("Calibri", -18), width=1).grid(row=4, column=7, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Header:', text_font=("Calibri", -18), width=1).grid(row=4, column=9, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Decimal:', text_font=("Calibri", -18), width=1).grid(row=4, column=11, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Skip:', text_font=("Calibri", -18), width=1).grid(row=4, column=13, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Pot Column:', text_font=("Calibri", -18), width=1).grid(row=4, column=15, sticky=tk.W)
    ct.CTkLabel(master=ORRFrame, text='Cur Column:', text_font=("Calibri", -18), width=1).grid(row=4, column=17, sticky=tk.W)

    Scans = ("LSV", "Single", "Multiple")
    ORRaScan_var = ct.StringVar()
    ORRaScan = ct.CTkOptionMenu(master=ORRFrame, variable=ORRaScan_var, values=Scans)
    ORRaScan.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ORRaScan.set(ORRa_config[0])
    ORRaScan.grid(row=4, column=2, sticky=tk.W)

    ORRaScanRate = ct.CTkEntry(master=ORRFrame, width=50)
    ORRaScanRate.grid(row=4, column=4, sticky=tk.W)
    ORRaScanRate.insert(0, ORRa_config[1])

    ORRaScanNumber = ct.CTkEntry(master=ORRFrame, width=30)
    ORRaScanNumber.grid(row=4, column=6, sticky=tk.W)
    ORRaScanNumber.insert(0, ORRa_config[2])

    Seperators = (";", "spaces", "tabs")
    ORRaSep_var = ct.StringVar()
    ORRaSep = ct.CTkOptionMenu(master=ORRFrame, variable=ORRaSep_var, values=Seperators)
    ORRaSep.config(width=90, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ORRaSep.set(ORRa_config[3])
    ORRaSep.grid(row=4, column=8, sticky=tk.W)

    Options = ('None', '0', '1', '2', '3', '4', '5', '6')
    ORRaOption_var = ct.StringVar()
    ORRaHead = ct.CTkComboBox(master=ORRFrame, variable=ORRaOption_var, values=Options)
    ORRaHead.configure(width=70, fg_color=('grey90', 'grey10'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'), border_color=('grey80', 'grey20'))
    ORRaHead.set(ORR_config[4])
    ORRaHead.grid(row=4, column=10, sticky=tk.W)

    Decimals = ('.', ',')
    ORRaDecimal_var = ct.StringVar()
    ORRaDecimal = ct.CTkOptionMenu(master=ORRFrame, variable=ORRaDecimal_var, values=Decimals)
    ORRaDecimal.config(width=50, fg_color=('grey80', 'grey20'), button_color=('grey80', 'grey20'), button_hover_color=('grey80', 'grey20'))
    ORRaDecimal.set(ORRa_config[5])
    ORRaDecimal.grid(row=4, column=12, sticky=tk.W)

    ORRaSkip = ct.CTkEntry(master=ORRFrame, width=30)
    ORRaSkip.grid(row=4, column=14, sticky=tk.W)
    ORRaSkip.insert(0, ORRa_config[6])

    ORRaPot = ct.CTkEntry(master=ORRFrame, width=30)
    ORRaPot.grid(row=4, column=16, sticky=tk.W)
    ORRaPot.insert(0, ORRa_config[7])

    ORRaCur = ct.CTkEntry(master=ORRFrame, width=30)
    ORRaCur.grid(row=4, column=18, sticky=tk.W)
    ORRaCur.insert(0, ORRa_config[8])


    SaveFrame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    SaveFrame.grid(row=3, column=1, sticky='nswe')
    SaveFrame.grid_columnconfigure(0, weight=1)

    def save():

        SaveText = f'Import Configure File\n' \
                   f'Ar\n' \
                   f'{ArScan.get()}\t{ArScanRate.get()}\t{ArScanNumber.get()}\t{ArSep.get()}\t{ArHead.get()}\t{ArDecimal.get()}\t{ArSkip.get()}\t{ArPot.get()}\t{ArV.get()}\t{ArCur.get()}\t{ArA.get()}\n' \
                   f'CO\n' \
                   f'{COSep.get()}\t{COHead.get()}\t{CODecimal.get()}\t{COSkip.get()}\t{COPot.get()}\t{COCur.get()}\n' \
                   f'ORR\n'\
                   f'{ORRScan.get()}\t{ORRScanRate.get()}\t{ORRScanNumber.get()}\t{ORRSep.get()}\t{ORRHead.get()}\t{ORRDecimal.get()}\t{ORRSkip.get()}\t{ORRPot.get()}\t{ORRCur.get()}\n'\
                   f'ORRa\n' \
                   f'{ORRaScan.get()}\t{ORRaScanRate.get()}\t{ORRaScanNumber.get()}\t{ORRaSep.get()}\t{ORRaHead.get()}\t{ORRaDecimal.get()}\t{ORRaSkip.get()}\t{ORRaPot.get()}\t{ORRaCur.get()}\n'
        config = open('Importconfig.txt', 'w')
        config.write(SaveText)
        config.close()


    SaveButton = ct.CTkButton(master=SaveFrame,text="Save", command=save, text_font=("Calibri", -18), width= 160, height= 10)
    SaveButton.grid(row=0, column=0, sticky=tk.E, pady=10, padx=10)


    #window.mainloop()


#root = 1
#importwindow(root, 1, 1)