import tkinter as tk
from tkinter import filedialog
import customtkinter as ct

import pandas as pd
import numpy as np
from scipy import interpolate

import matplotlib.lines as lines
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt

cm = 1 / 2.54

def import_data(data, results):

    if 'Current/A-1_first_scan_1' in data.columns:
        data['Current/A_diff_1'] = data['Current/A-1_first_scan_1'] - data['Current/A-2_second_scan_1']

    if 'ik/A_tafel_ORR_2' in data.columns:
        data['im/A_tafel_ORR_2'] = data['ik/A_tafel_ORR_2'] / float(LoadingEntry.get())

        if 'ORR_Tafel_slope_2' in results.columns:
            coefficient0 = results['ORR_Tafel_slope_2'].iloc[0]
            coefficient1 = results['ORR_Tafel_intercept_2'].iloc[0]

            data['E-iR/V_tafel_ORR_2'] = coefficient0 * np.log10(data['ik/A_tafel_ORR_2']) + coefficient1

        if 'ORR_Tafel_slope_eta_2' in results.columns:
            coefficient0 = results['ORR_Tafel_slope_eta_2'].iloc[0]
            coefficient1 = results['ORR_Tafel_intercept_eta_2'].iloc[0]

            data['E-iR-etadiff/V_tafel_ORR_2'] = coefficient0 * np.log10(data['ik/A_tafel_ORR_2']) + coefficient1

    return (data)


def HUPD(data, data2, data3):

    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        #window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        #window.configure(bg='grey90')

    HUPD_f = Figure(figsize=(5,3),facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(HUPD_f, master=HUPD_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, HUPD_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = HUPD_f.add_subplot(1, 1, 1)
    ax.set_ylabel("Current [A]")
    ax.set_xlabel("Potential [V]")
    ax.set_facecolor(bgcolor)
    ax.xaxis.label.set_color(fgcolor)
    ax.yaxis.label.set_color(fgcolor)
    ax.tick_params(axis='x', colors=fgcolor)
    ax.tick_params(axis='y', colors=fgcolor)
    ax.spines['left'].set_color(fgcolor)
    ax.spines['top'].set_color(fgcolor)
    ax.spines['right'].set_color(fgcolor)
    ax.spines['bottom'].set_color(fgcolor)

    formatter = ticker.ScalarFormatter()
    formatter.set_powerlimits((-3, 3))  # Set the power limits for scientific notation

    # Set the y-axis tick label format
    ax.yaxis.set_major_formatter(formatter)

    partial_name = 'Potential/V_HUPD'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:

        Pot = data.loc[:, matching_columns[0]]
        name = matching_columns[0].replace(partial_name, '').replace("_", "").rstrip("0")

    partial_name = 'Current/A_HUPD'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():

        ax.plot(Pot, Cur, label=name)


    partial_name2 = 'Potential/V_HUPD'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[0]]
        name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("0")


    partial_name2 = 'Current/A_HUPD'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2, label=name2)


    partial_name3 = 'Potential/V_HUPD'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[0]]
        name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("0")


    partial_name3 = 'Current/A_HUPD'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3, label=name3)

    legend = ax.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

def COStrip(data, data2, data3):

    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        #window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        #window.configure(bg='grey90')

    COStrip_f = Figure(figsize=(5, 3) , facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(COStrip_f, master=COStrip_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, COStrip_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = COStrip_f.add_subplot(1, 1, 1)
    ax.set_ylabel("Current [A]")
    ax.set_xlabel("Potential [V]")
    ax.set_facecolor(bgcolor)
    ax.xaxis.label.set_color(fgcolor)
    ax.yaxis.label.set_color(fgcolor)
    ax.tick_params(axis='x', colors=fgcolor)
    ax.tick_params(axis='y', colors=fgcolor)
    ax.spines['left'].set_color(fgcolor)
    ax.spines['top'].set_color(fgcolor)
    ax.spines['right'].set_color(fgcolor)
    ax.spines['bottom'].set_color(fgcolor)
    formatter = ticker.ScalarFormatter()
    formatter.set_powerlimits((-3, 3))  # Set the power limits for scientific notation

    # Set the y-axis tick label format
    ax.yaxis.set_major_formatter(formatter)

    partial_name = 'Potential/V_COStrip'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:

        Pot = data.loc[:, matching_columns[0]]
        name = matching_columns[0].replace(partial_name, '').replace("_", "").rstrip("1")

    partial_name = 'Current/A_diff'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():

        ax.plot(Pot, Cur, label=name)

    partial_name2 = 'Potential/V_COStrip'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[0]]
        name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("1")

    partial_name2 = 'Current/A_diff'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2, label=name2)

    partial_name3 = 'Potential/V_COStrip'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[0]]
        name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("1")

    partial_name3 = 'Current/A_diff'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3, label=name3)

    legend = ax.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

def ORR(data, data2, data3):

    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        # window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        # window.configure(bg='grey90')

    ORR_f = Figure(figsize=(5, 3), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(ORR_f, master=ORR_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, ORR_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = ORR_f.add_subplot(1, 1, 1)
    ax.set_ylabel("Current [A]")
    ax.set_xlabel("Potential [V]")
    ax.set_facecolor(bgcolor)
    ax.xaxis.label.set_color(fgcolor)
    ax.yaxis.label.set_color(fgcolor)
    ax.tick_params(axis='x', colors=fgcolor)
    ax.tick_params(axis='y', colors=fgcolor)
    ax.spines['left'].set_color(fgcolor)
    ax.spines['top'].set_color(fgcolor)
    ax.spines['right'].set_color(fgcolor)
    ax.spines['bottom'].set_color(fgcolor)

    formatter = ticker.ScalarFormatter()
    formatter.set_powerlimits((-3, 3))  # Set the power limits for scientific notation

    # Set the y-axis tick label format
    ax.yaxis.set_major_formatter(formatter)

    partial_name = 'E-iR/V_ORR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Pot = data.loc[:, matching_columns[0]]
        name = matching_columns[0].replace(partial_name, '').replace("_", "").rstrip("2")

    partial_name = 'Current/A_ORR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
            Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():
            ax.plot(Pot, Cur, label=name)


    partial_name2 = 'E-iR/V_ORR'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[0]]
        name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("2")


    partial_name2 = 'Current/A_ORR'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2, label=name2)


    partial_name3 = 'E-iR/V_ORR'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[0]]
        name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("2")


    partial_name3 = 'Current/A_ORR'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3, label=name3)

    legend = ax.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

def im(data, data2, data3):

    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        # window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        # window.configure(bg='grey90')

    im_f = Figure(figsize=(5, 3), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(im_f, master=im_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, im_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = im_f.add_subplot(1, 1, 1)
    ax.set_ylabel("Potential [V]")
    ax.set_xlabel("i_mass [A/gPt]")
    ax.set_facecolor(bgcolor)
    ax.xaxis.label.set_color(fgcolor)
    ax.yaxis.label.set_color(fgcolor)
    ax.tick_params(axis='x', colors=fgcolor)
    ax.tick_params(axis='y', colors=fgcolor)
    ax.spines['left'].set_color(fgcolor)
    ax.spines['top'].set_color(fgcolor)
    ax.spines['right'].set_color(fgcolor)
    ax.spines['bottom'].set_color(fgcolor)
    ax.set_xscale('log')

    formatter = ticker.ScalarFormatter()
    formatter.set_powerlimits((-3, 3))  # Set the power limits for scientific notation

    # Set the y-axis tick label format
    ax.yaxis.set_major_formatter(formatter)

    partial_name = 'im/A_tafel_ORR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Pot = data.loc[:, matching_columns[0]]
        name = matching_columns[0].replace(partial_name, '').replace("_", "").rstrip("2")

    partial_name = 'E/V_tafel_ORR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
            Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():
            ax.plot(Pot, Cur, label=name)


    partial_name2 = 'im/A_tafel_ORR'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[0]]
        name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("2")


    partial_name2 = 'E/V_tafel_ORR'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2, label=name2)


    partial_name3 = 'im/A_tafel_ORR'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[0]]
        name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("2")


    partial_name3 = 'E/V_tafel_ORR'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3, label=name3)

    #real data
    partial_name = 'im/A_ORR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Pot = data.loc[:, matching_columns[0]]
        name = matching_columns[0].replace(partial_name, '').replace("_", "").rstrip("2")

    partial_name = 'E-iR(lim)/V_ORR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():
        ax.plot(Pot, Cur, label=name)

    partial_name2 = 'im/A_ORR'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[0]]
        name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("2")

    partial_name2 = 'E-iR(lim)/V_ORR'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2, label=name2)

    partial_name3 = 'im/A_ORR'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[0]]
        name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("2")

    partial_name3 = 'E-iR(lim)/V_ORR'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3, label=name3)

    legend = ax.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

def HOR(data, data2, data3):

    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        # window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        # window.configure(bg='grey90')

    HOR_f = Figure(figsize=(5, 3), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(HOR_f, master=HOR_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, HOR_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = HOR_f.add_subplot(1, 1, 1)
    ax.set_ylabel("Potential [V]")
    ax.set_xlabel("i_mass [A/gPt]")
    ax.set_facecolor(bgcolor)
    ax.xaxis.label.set_color(fgcolor)
    ax.yaxis.label.set_color(fgcolor)
    ax.tick_params(axis='x', colors=fgcolor)
    ax.tick_params(axis='y', colors=fgcolor)
    ax.spines['left'].set_color(fgcolor)
    ax.spines['top'].set_color(fgcolor)
    ax.spines['right'].set_color(fgcolor)
    ax.spines['bottom'].set_color(fgcolor)

    formatter = ticker.ScalarFormatter()
    formatter.set_powerlimits((-3, 3))  # Set the power limits for scientific notation

    # Set the y-axis tick label format
    ax.yaxis.set_major_formatter(formatter)

    partial_name = 'E-iR/V_HOR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Pot = data.loc[:, matching_columns[0]]
        name = matching_columns[0].replace(partial_name, '').replace("_", "").rstrip("3")

    partial_name = 'Current_anodic'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
            Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():
            ax.plot(Pot, Cur, label=name)


    partial_name2 = 'E-iR/V_HOR'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[0]]
        name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("3")


    partial_name2 = 'Current_anodic'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2, label=name2)


    partial_name3 = 'E-iR/V_HOR'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[0]]
        name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("3")


    partial_name3 = 'Current_anodic'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3, label=name3)

    #cathodic
    partial_name = 'E-iR/V_HOR'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Pot = data.loc[:, matching_columns[1]]
        #name = matching_columns[1].replace(partial_name, '').replace("_", "").rstrip("2")

    partial_name = 'Current_cathodic'
    matching_columns = [col for col in data.columns if partial_name in col]

    if matching_columns:
        Cur = data.loc[:, matching_columns[0]]

    if 'Pot' in locals():
        ax.plot(Pot, Cur)

    partial_name2 = 'E-iR/V_HOR'  # Name for the second dataframe
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Pot2 = data2.loc[:, matching_columns2[1]]
        #name2 = matching_columns2[0].replace(partial_name2, '').replace("_", "").rstrip("2")

    partial_name2 = 'Current_cathodic'
    matching_columns2 = [col for col in data2.columns if partial_name2 in col]

    if matching_columns2:
        Cur2 = data2.loc[:, matching_columns2[0]]

        ax.plot(Pot2, Cur2)

    partial_name3 = 'E-iR/V_HOR'  # Name for the third dataframe
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Pot3 = data3.loc[:, matching_columns3[1]]
        #name3 = matching_columns3[0].replace(partial_name3, '').replace("_", "").rstrip("2")

    partial_name3 = 'Current_cathodic'
    matching_columns3 = [col for col in data3.columns if partial_name3 in col]

    if matching_columns3:
        Cur3 = data3.loc[:, matching_columns3[0]]
        ax.plot(Pot3, Cur3)

    legend = ax.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

if __name__ == '__main__':

    root = ct.CTk()
    root.title('RDE Treatment')
    root.iconphoto(True, tk.PhotoImage(file='iconRDE.png'))
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    widthfactor = width / 1920
    heightfactor = height / 1080
    root.geometry(str(int(width - (widthfactor * 20))) + 'x' + str(int(height - (heightfactor * 90))) + '+0+10')
    root.configure(bg='grey90')
    root.resizable(False, False)

    root.grid_columnconfigure(0, weight=3, minsize=int(widthfactor * (width * 0.753) - 25))
    #root.grid_columnconfigure(1, weight=1, minsize=int(widthfactor * (width * (1 - 0.753)) - 25))
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1, minsize=int(heightfactor * (height * 0.615)))
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0, minsize=10)

    if ct.get_appearance_mode() == 'Dark':
        bg_color = 'grey10'
        fg_color = 'grey20'
    else:
        bg_color = 'grey90'
        fg_color = 'grey80'

    # open Savpath:
    pathfile = open('Pathfile.txt')
    path_txt = pathfile.readlines()
    pathfile.close()

    global path
    path = path_txt[1].replace('\n', '')



    bottom_frame = ct.CTkFrame(master=root, corner_radius=10, fg_color=('grey80', 'grey20'))
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nswe', padx=10, ipadx=10, ipady=10)
    bottom_frame.grid_rowconfigure(0, weight=0)
    bottom_frame.grid_rowconfigure(1, weight=1)
    bottom_frame.grid_rowconfigure(2, weight=0)
    bottom_frame.grid_columnconfigure(1, weight=1)


    def change_mode():
        if switch_2.get() == 1:
            ct.set_appearance_mode("Dark")
            root.configure(bg='grey10')



        else:
            ct.set_appearance_mode("Light")
            root.configure(bg='grey90')



    switch_2 = ct.CTkSwitch(master=bottom_frame, text="Dark Mode", command=change_mode)
    switch_2.grid(row=1, column=0, sticky=tk.W, padx=10)

    input_frame = ct.CTkFrame(master=root, corner_radius=10, fg_color=('grey80', 'grey20'))
    input_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)
    input_frame.grid_rowconfigure(0, weight=0, minsize=10)
    input_frame.grid_columnconfigure(0, weight=0, minsize=10)
    input_frame.grid_columnconfigure(3, weight=0, minsize=10)
    input_frame.grid_rowconfigure(2, weight=0, minsize=10)
    input_frame.grid_rowconfigure(4, weight=0, minsize=10)
    input_frame.grid_rowconfigure(6, weight=0, minsize=10)
    input_frame.grid_rowconfigure(8, weight=0, minsize=10)
    input_frame.grid_rowconfigure(10, weight=0, minsize=10)

    graph_frame = ct.CTkFrame(master=root, corner_radius=10, fg_color=('grey80', 'grey20'), width=1880, height=690)
    graph_frame.grid(row=1, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)
    graph_frame.grid_rowconfigure(0, weight=0, minsize=10)
    graph_frame.grid_columnconfigure(0, weight=0, minsize=10)
    graph_frame.grid_columnconfigure(2, weight=0, minsize=10)
    graph_frame.grid_columnconfigure(4, weight=0, minsize=10)
    graph_frame.grid_columnconfigure(6, weight=0, minsize=10)
    graph_frame.grid_rowconfigure(2, weight=0, minsize=10)
    graph_frame.grid_rowconfigure(4, weight=0, minsize=10)







    LoadingLabel = ct.CTkLabel(master=input_frame, text='Loading [g]:', text_font=("Calibri", -18))
    LoadingLabel.grid(row=3, column=1, sticky=tk.W)
    LoadingEntry = ct.CTkEntry(master=input_frame, width=200, text_font=("Calibri", -14))
    LoadingEntry.grid(row=3, column=2, sticky=tk.W, columnspan=2)
    LoadingEntry.insert(0, '2.74889357189107E-06')



    E1L = ct.CTkLabel(master=input_frame, text='E1:', text_font=("Calibri", -18))
    E1L.grid(row=1, column=4, sticky=tk.W)
    E1entry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    E1entry.grid(row=1, column=5, sticky=tk.W)
    #E1entry.insert(0,'W:/RRDE/Corbi/CG2_PtC_10mVs/CG2-PtC-16507.txt')


    def E1():
        global path
        file = filedialog.askopenfilename(title='Open Electrode file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            E1entry.delete(0, 'end')
            E1entry.insert(0, file)
            Eval.configure(state=tk.NORMAL)

            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'
            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()


    ct.CTkButton(master=input_frame, text='Open', command=E1, text_font=("Calibri", -18), width=80).grid(row=1, column=6, sticky=tk.W, padx=20)

    E2L = ct.CTkLabel(master=input_frame, text='E2:', text_font=("Calibri", -18))
    E2L.grid(row=3, column=4, sticky=tk.W)
    E2entry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    E2entry.grid(row=3, column=5, sticky=tk.W)


    def E2():
        global path
        file = filedialog.askopenfilename(title='Open Electrode file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            E2entry.delete(0, 'end')
            E2entry.insert(0, file)


            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'
            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()


    ct.CTkButton(master=input_frame, text='Open', command=E2, text_font=("Calibri", -18), width=80).grid(row=3, column=6, sticky=tk.W, padx=20)

    E3L = ct.CTkLabel(master=input_frame, text='E3:', text_font=("Calibri", -18))
    E3L.grid(row=5, column=4, sticky=tk.W)
    E3entry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    E3entry.grid(row=5, column=5, sticky=tk.W)


    def E3():
        global path
        file = filedialog.askopenfilename(title='Open Electrode file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            E3entry.delete(0, 'end')
            E3entry.insert(0, file)


            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'
            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()


    ct.CTkButton(master=input_frame, text='Open', command=E3, text_font=("Calibri", -18), width=80).grid(row=5, column=6, sticky=tk.W, padx=20)

    # graphs in the graphs frame
    HUPD_frame = ct.CTkFrame(master=graph_frame, corner_radius=10, fg_color=('grey90', 'grey10'))#, width=int((graph_frame.winfo_width() - 50) / 3), height=int((graph_frame.winfo_height() - 30) / 2))
    HUPD_frame.grid(row=1, column=1, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)
    COStrip_frame = ct.CTkFrame(master=graph_frame, corner_radius=10, fg_color=('grey90', 'grey10'))#, width=int((graph_frame.winfo_width() - 50) / 3), height=int((graph_frame.winfo_height() - 30) / 2))
    COStrip_frame.grid(row=1, column=3, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)
    ORR_frame = ct.CTkFrame(master=graph_frame, corner_radius=10, fg_color=('grey90', 'grey10'))#, width=int((graph_frame.winfo_width() - 50) / 3), height=int((graph_frame.winfo_height() - 30) / 2))
    ORR_frame.grid(row=1, column=5, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)
    im_frame = ct.CTkFrame(master=graph_frame, corner_radius=10, fg_color=('grey90', 'grey10'))#, width=int((graph_frame.winfo_width() - 50) / 3), height=int((graph_frame.winfo_height() - 30) / 2))
    im_frame.grid(row=3, column=1, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)
    HOR_frame = ct.CTkFrame(master=graph_frame, corner_radius=10, fg_color=('grey90', 'grey10'))#, width=int((graph_frame.winfo_width() - 50) / 3), height=int((graph_frame.winfo_height() - 30) / 2))
    HOR_frame.grid(row=3, column=3, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)


    def Evaluate():

        global E1_data
        global E2_data
        global E3_data

        Electrode1 = E1entry.get()
        Electrode1_results = E1entry.get().replace(".txt", "_results.txt")

        E1pd = pd.read_csv(Electrode1, sep='\t', header=0, decimal='.')
        E1rpd = pd.read_csv(Electrode1_results, sep='\t', header=0, decimal='.')

        E1_data = import_data(E1pd, E1rpd)

        Electrode2 = E2entry.get()

        if Electrode2:
            Electrode2_results = E2entry.get().replace(".txt", "_results.txt")
            E2pd = pd.read_csv(Electrode2, sep='\t', header=0, decimal='.')
            E2rpd = pd.read_csv(Electrode2_results, sep='\t', header=0, decimal='.')

            E2_data = import_data(E2pd, E2rpd)

        else:
            E2_data = pd.DataFrame()

        Electrode3 = E3entry.get()

        if Electrode3:
            Electrode3_results = E3entry.get().replace(".txt", "_results.txt")
            E3pd = pd.read_csv(Electrode3, sep='\t', header=0, decimal='.')
            E3rpd = pd.read_csv(Electrode3_results, sep='\t', header=0, decimal='.')

            E3_data = import_data(E3pd, E3rpd)


        else:
            E3_data = pd.DataFrame()


        HUPD(E1_data, E2_data, E3_data)
        COStrip(E1_data, E2_data, E3_data)
        ORR(E1_data, E2_data, E3_data)
        im(E1_data, E2_data, E3_data)
        HOR(E1_data, E2_data, E3_data)

        SaveButton.config(state=tk.NORMAL)



    Eval = ct.CTkButton(master=input_frame, text='Eval', command=Evaluate, text_font=("Calibri", -18), width=80)
    Eval.grid(row=1, column=7, sticky=tk.W, padx=20)
    Eval.configure(state=tk.DISABLED)

    def save():
        global E1_data
        global E2_data
        global E3_data

        file = filedialog.askdirectory(title='Save As', initialdir=path)

        if file.strip():

            if not E1_data.empty:

                name1 = E1_data.columns[0].split('_')[2]

                file1 = file + '/' + name1 + '_treated.txt'

                E1_data.to_csv(file1, sep='\t', index=False, header=True)

            if not E2_data.empty:

                name2 = E2_data.columns[0].split('_')[2]

                file2 = file + '/' + name2 + '_treated.txt'
                E2_data.to_csv(file2, sep='\t', index=False, header=True)


            if not E3_data.empty:

                name3 = E3_data.columns[0].split('_')[2]

                file3 = file + '/' + name3 + '_treated.txt'
                E3_data.to_csv(file3, sep='\t', index=False, header=True)

            #reinitialize the dataframes

            E1_data = pd.DataFrame()
            E2_data = pd.DataFrame()
            E3_data = pd.DataFrame()


        else:
            pass


    SaveButton = ct.CTkButton(master=bottom_frame, text="Save", command=save, text_font=("Calibri", -18), width=80, height=10)
    SaveButton.grid(row=1, column=2, sticky=tk.E, padx=10)
    SaveButton.config(state=tk.DISABLED)

    def on_closing():
        root.destroy()
        exit()


    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
