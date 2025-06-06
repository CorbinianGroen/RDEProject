import tkinter as tk
from tkinter import filedialog
import customtkinter as ct

import os
import glob

import pandas as pd
import numpy as np
from scipy import interpolate

import matplotlib.lines as lines
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt

# imports of files
from scipy.stats import linregress

from importfilter import importwindow
import scanimport as scan

# testing values
loading = 3.847E-6
Temp = 273 + 20
# R = 32.7
global Ref
Ref = 0


# radius = 0.2

cm = 1 / 2.54

# end of testing values

# apperancesetting
ct.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


# end

def interpolation(curve1, curve2):
    upper1 = curve1['Potential/V'].loc[curve1['Potential/V'].nlargest(1).index[0]]
    lower1 = curve1['Potential/V'].loc[curve1['Potential/V'].nsmallest(1).index[0]]

    upper2 = curve2['Potential/V'].loc[curve2['Potential/V'].nlargest(1).index[0]]
    lower2 = curve2['Potential/V'].loc[curve2['Potential/V'].nsmallest(1).index[0]]

    if upper1 <= upper2:
        upper = upper1
    if upper1 > upper2:
        upper = upper2
    if lower1 >= lower2:
        lower = lower1
    if lower1 < lower2:
        lower = lower2
    points = curve1.shape[0]
    np_array = np.linspace(lower, upper, points)
    Volt = pd.DataFrame(np_array, columns=['Potential/V'])
    Amp1 = interpolate.interp1d(x=curve1['Potential/V'], y=curve1['Current/A'], kind='linear')
    Amp2 = interpolate.interp1d(x=curve2['Potential/V'], y=curve2['Current/A'], kind='linear')
    Amp_np1 = Amp1(Volt['Potential/V'])
    Amp_np2 = Amp2(Volt['Potential/V'])
    Amp_pd1 = pd.DataFrame(Amp_np1, columns=['Current/A_1'])
    Amp_pd2 = pd.DataFrame(Amp_np2, columns=['Current/A_2'])
    df = pd.merge(Volt, Amp_pd1, left_index=True, right_index=True)
    df = pd.merge(df, Amp_pd2, left_index=True, right_index=True)

    if 'RingCurrent/A' in curve1:
        Amp3 = interpolate.interp1d(x=curve1['Potential/V'], y=curve1['RingCurrent/A'], kind='linear')
        Amp_np3 = Amp3(Volt['Potential/V'])
        Amp_pd3 = pd.DataFrame(Amp_np3, columns=['RingCurrent/A_1'])
        df = pd.merge(df, Amp_pd3, left_index=True, right_index=True)

    if 'RingCurrent/A' in curve2:
        Amp4 = interpolate.interp1d(x=curve2['Potential/V'], y=curve2['RingCurrent/A'], kind='linear')
        Amp_np4 = Amp4(Volt['Potential/V'])
        Amp_pd4 = pd.DataFrame(Amp_np4, columns=['RingCurrent/A_2'])
        df = pd.merge(df, Amp_pd4, left_index=True, right_index=True)

    return df


def CO_plot(df1, df2):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('CO Strip Evaluation')
    window.geometry(
        str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(
            int(d_x + widthfactor * 8)) + '+' + str(int(d_y + heightfactor * 299)))
    # window.configure(background='white')
    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        window.configure(bg='grey90')
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    window.grid_columnconfigure(0, weight=3)
    window.grid_columnconfigure(1, weight=2, minsize=350)
    window.grid_rowconfigure(0, weight=1)

    co_info_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=("grey80", 'grey20'))
    co_info_frame.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)

    co_info_frame.grid_rowconfigure(0, weight=10)
    co_info_frame.grid_rowconfigure(1, weight=1)
    co_info_frame.grid_rowconfigure(2, weight=10)
    co_info_frame.grid_columnconfigure(0, weight=0)
    co_info_frame.grid_columnconfigure(1, weight=1)
    co_info_frame.grid_columnconfigure(2, weight=0)

    button_frame = ct.CTkFrame(master=co_info_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    button_frame.grid(row=2, column=1, sticky='nswe', pady=10, padx=10)
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=0)
    button_frame.grid_columnconfigure(2, weight=0)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)

    def on_closing():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    co_graph_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    co_graph_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)

    co_graph_frame.grid_rowconfigure(0, weight=0)
    co_graph_frame.grid_rowconfigure(1, weight=1)
    co_graph_frame.grid_columnconfigure(0, weight=0, minsize=10)
    co_graph_frame.grid_columnconfigure(1, weight=1)
    co_graph_frame.grid_columnconfigure(2, weight=0, minsize=10)

    co_f = Figure(figsize=(28 * cm, 18 * cm), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(co_f, master=co_graph_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, co_graph_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    df = interpolation(df1, df2)
    df['Diff'] = df['Current/A_1'] - df['Current/A_2']

    df['Potential/V'] = df['Potential/V'] - float(Ref)  # - (df1['Current/A'] * float(R))

    higher0 = df[df['Diff'] >= 0]
    higher0 = higher0[higher0['Potential/V'] >= 0.2]
    integration = np.trapezoid(x=higher0['Potential/V'], y=higher0['Diff'])
    global co_area
    co_area = ((integration / 0.01) / 420e-6)

    global co_rf
    area_geo = np.pi * (float(RadiusEntry.get()) ** 2)
    co_rf = co_area / area_geo
    firstvalue = higher0.head(1).index[0]

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
        global co_area_norm
        co_area_norm = co_area * 0.0001 / loading

    ax_co = co_f.add_subplot(1, 1, 1)
    ax_co.set_ylabel("Current [A]")
    ax_co.set_xlabel("Potential [V]")
    ax_co.set_facecolor(bgcolor)
    ax_co.xaxis.label.set_color(fgcolor)
    ax_co.yaxis.label.set_color(fgcolor)
    ax_co.tick_params(axis='x', colors=fgcolor)
    ax_co.tick_params(axis='y', colors=fgcolor)
    ax_co.spines['left'].set_color(fgcolor)
    ax_co.spines['top'].set_color(fgcolor)
    ax_co.spines['right'].set_color(fgcolor)
    ax_co.spines['bottom'].set_color(fgcolor)
    ax_co.plot(df['Potential/V'], df['Current/A_1'], label='first scan')
    ax_co.plot(df['Potential/V'], df['Current/A_2'], label='second scan')
    ax_co.plot(higher0['Potential/V'], higher0['Diff'], 'w--', label='integration')
    legend = ax_co.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)
    ax_co.fill_between(df['Potential/V'].loc[firstvalue:df.shape[0]],
                       df['Current/A_1'].loc[firstvalue:df.shape[0]],
                       df['Current/A_2'].loc[firstvalue:df.shape[0]], color=color)

    canvas.draw_idle()

    co_variable_frame = ct.CTkFrame(master=co_info_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
    co_variable_frame.grid(row=1, column=1, sticky='nswe', pady=10, padx=10)
    co_variable_frame.grid_columnconfigure(0, weight=1, minsize=300)
    co_variable_frame.grid_rowconfigure(0, weight=1)
    co_variable_frame.grid_rowconfigure(1, weight=1)
    co_variable_frame.grid_rowconfigure(2, weight=1)

    Area_norm_frame = ct.CTkFrame(master=co_variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    Area_norm_frame.grid(row=2, column=0, sticky='nswe', pady=5, padx=5)
    Area_norm_frame.grid_rowconfigure(0, weight=0)
    Area_norm_frame.grid_rowconfigure(1, weight=1)
    Area_norm_frame.grid_rowconfigure(2, weight=0)
    Area_norm_frame.grid_columnconfigure(0, weight=0, minsize=80)
    Area_norm_frame.grid_columnconfigure(1, weight=1, minsize=80)
    Area_norm_frame.grid_columnconfigure(2, weight=0, minsize=125)
    if LoadingEntry.get() != '':
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='{0:.3f}'.format(co_area_norm), font=("Calibri", -20),
                                      width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    else:
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='n.a.', font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_norm_frame, text='ECSA:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E,
                                                                                    padx=2)
    ct.CTkLabel(Area_norm_frame, text='m²ₚₜ/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E,
                                                                                       padx=2)

    rf_frame = ct.CTkFrame(master=co_variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    rf_frame.grid(row=1, column=0, sticky='nswe', pady=0, padx=5)
    rf_frame.grid_rowconfigure(0, weight=0)
    rf_frame.grid_rowconfigure(1, weight=1)
    rf_frame.grid_rowconfigure(2, weight=0)
    rf_frame.grid_columnconfigure(0, weight=0, minsize=80)
    rf_frame.grid_columnconfigure(1, weight=1, minsize=80)
    rf_frame.grid_columnconfigure(2, weight=0, minsize=125)
    rf_label = ct.CTkLabel(rf_frame, text='{0:.3f}'.format(co_rf), font=("Calibri", -20), width=1)
    rf_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(rf_frame, text='rf:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(rf_frame, text='cm²ₚₜ/cm²₉ₑₒ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E,
                                                                                    padx=2)

    Area_frame = ct.CTkFrame(master=co_variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    Area_frame.grid(row=0, column=0, sticky='nswe', pady=5, padx=5)
    Area_frame.grid_rowconfigure(0, weight=0)
    Area_frame.grid_rowconfigure(1, weight=1)
    Area_frame.grid_rowconfigure(2, weight=0)
    Area_frame.grid_columnconfigure(0, weight=0, minsize=80)
    Area_frame.grid_columnconfigure(1, weight=1, minsize=80)
    Area_frame.grid_columnconfigure(2, weight=0, minsize=125)
    Area_label = ct.CTkLabel(Area_frame, text='{0:.3f}'.format(co_area), font=("Calibri", -20), width=1)
    Area_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_frame, text='Area Pt:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(Area_frame, text='cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    def exit1(df):
        window.destroy()
        global z
        a = z
        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=160)
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=125)
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=20)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='CO Strip Determination - ', font=("Calibri", -20), width=140).grid(
            row=0, column=0, sticky=tk.W, padx=2, pady=5)

        d['v_n_{0}'.format(z)] = ct.CTkEntry(d['v_f_{0}'.format(z)], width=125, border_width=0,
                                             bg_color=("grey70", 'grey30'), fg_color=("grey70", 'grey30'),
                                             font=("Calibri", -19), text_color=('black', 'white'))
        d['v_n_{0}'.format(z)].insert(0, NameEntry.get())
        d['v_n_{0}'.format(z)].configure(state='disabled')
        d['v_n_{0}'.format(z)].grid(row=0, column=1, sticky='ws', pady=5)

        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x', width=8, height=8, command=lambda: remove(a),
                     font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=2, sticky=tk.E, pady=5,
                                                                                  padx=5)
        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['a_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                             fg_color=('grey80', 'grey20'))
        d['a_f_{0}'.format(z)].grid(row=1, column=0, sticky='nswe', pady=5, padx=5, ipadx=2, ipady=2, columnspan=3)
        d['a_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['a_l_{0}'.format(z)] = ct.CTkLabel(d['a_f_{0}'.format(z)], text='{0:.3f}'.format(co_area),
                                             font=("Calibri", -20), width=1)
        d['a_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='Area Pt:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                                  sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                               sticky=tk.E, padx=2)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                              fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2, columnspan=3)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(co_rf),
                                              font=("Calibri", -20), width=1)
        d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='rf:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                              sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='cm²ₚₜ/cm²₉ₑₒ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                       sticky=tk.E,
                                                                                                       padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                               fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2, columnspan=3)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(co_area_norm),
                                                   font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20),
                                                   width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='ECSA:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                                 sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='m²ₚₜ/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                    sticky=tk.E, padx=2)

        data_canvas.update_idletasks()
        data_canvas.config(scrollregion=data_frame.bbox())

        df.rename(columns={'Potential/V': 'Potential/V_' + 'COStrip_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df.rename(columns={'Current/A_1': 'Current/A-1_' + 'first_scan_' + str(z)}, inplace=True)
        df.rename(columns={'Current/A_2': 'Current/A-2_' + 'second_scan_' + str(z)}, inplace=True)
        df.rename(columns={'Diff': 'Diff-Current/A' + str(z)}, inplace=True)

        global savefile
        savefile = pd.concat([savefile, df], axis=1)

        if LoadingEntry.get() != '':
            ecsa = co_area_norm
        else:
            ecsa = 'n.a.'

        result = pd.DataFrame({'COStrip_Area_cm^2_Pt_' + NameEntry.get() + '_' + str(z): [co_area],
                               'COStrip_rf_cm^2_Pt/cm^2_geo_' + str(z): [co_rf],
                               'COStrip_ECSA_cm^2_Pt/g_Pt_' + str(z): [ecsa]})
        global results
        results = pd.concat([results, result], axis=1)

        save_enable()

        z += 1

    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=lambda: exit1(df), font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    window.mainloop()


def Ar_Plot(anodic, cathodic):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('HUPD ECSA Evaluation')
    window.geometry(
        str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(
            int(d_x + widthfactor * 8)) + '+' + str(int(d_y + heightfactor * 299)))
    # window.configure(background='white')
    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        window.configure(bg='grey90')
    window.overrideredirect(True)
    window.attributes("-topmost", True)
    window.grid_columnconfigure(0, weight=3)
    window.grid_columnconfigure(1, weight=2, minsize=350)
    window.grid_rowconfigure(0, weight=1)

    info_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    info_frame.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)

    info_frame.grid_rowconfigure(0, weight=10)
    info_frame.grid_rowconfigure(1, weight=1)
    info_frame.grid_rowconfigure(2, weight=10)
    info_frame.grid_columnconfigure(0, weight=0)
    info_frame.grid_columnconfigure(1, weight=1)
    info_frame.grid_columnconfigure(2, weight=0)

    button_frame = ct.CTkFrame(master=info_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    button_frame.grid(row=2, column=1, sticky='nswe', pady=10, padx=10)
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=0)
    button_frame.grid_columnconfigure(2, weight=0)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)

    def on_closing():
        window.destroy()
        # exit()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    ar_graph_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    ar_graph_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)

    ar_graph_frame.grid_rowconfigure(0, weight=0)
    ar_graph_frame.grid_rowconfigure(1, weight=1)
    ar_graph_frame.grid_columnconfigure(0, weight=0, minsize=10)
    ar_graph_frame.grid_columnconfigure(1, weight=1)
    ar_graph_frame.grid_columnconfigure(2, weight=0, minsize=10)

    f = Figure(figsize=(28 * cm, 18 * cm), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(f, master=ar_graph_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, ar_graph_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = f.add_subplot(1, 1, 1)
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

    anodic['Potential/V'] = anodic['Potential/V'] - float(Ref)  # - (df1['Current/A'] * float(R))
    cathodic['Potential/V'] = cathodic['Potential/V'] - float(Ref)  # - (df1['Current/A'] * float(R))

    max_current = anodic['Current/A'].loc[anodic['Current/A'].nlargest(1).index[0]]
    min_current = cathodic['Current/A'].loc[cathodic['Current/A'].nsmallest(1).index[0]]

    max_potential = anodic['Potential/V'].loc[anodic['Potential/V'].nlargest(1).index[0]]
    min_potential = cathodic['Potential/V'].loc[cathodic['Potential/V'].nsmallest(1).index[0]]

    init_anodic = anodic.loc[:, 'Current/A'][(anodic.loc[:, 'Current/A'].shift(2) > anodic.loc[:, 'Current/A']) & (
            anodic.loc[:, 'Current/A'].shift(-2) > anodic.loc[:, 'Current/A'])]
    init_anodic_V = anodic['Potential/V'].loc[init_anodic.nsmallest(1).index[0]]
    init_anodic_A = anodic['Current/A'].loc[init_anodic.nsmallest(1).index[0]]

    init_cathodic = cathodic.loc[:, 'Current/A'][
        (cathodic.loc[:, 'Current/A'].shift(2) < cathodic.loc[:, 'Current/A']) & (
                cathodic.loc[:, 'Current/A'].shift(-2) < cathodic.loc[:, 'Current/A'])]
    init_cathodic_V = cathodic['Potential/V'].loc[init_cathodic.nlargest(1).index[0]]
    init_cathodic_A = cathodic['Current/A'].loc[init_cathodic.nlargest(1).index[0]]

    ax.plot(anodic['Potential/V'], anodic['Current/A'], label='anodic')
    ax.plot(cathodic['Potential/V'], cathodic['Current/A'], label='cathodic')
    legend = ax.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

    index_low = anodic.iloc[(anodic['Potential/V'] - min_potential).abs().argsort()[:1]].index[0]
    index_high = anodic.iloc[(anodic['Potential/V'] - init_anodic_V).abs().argsort()[:1]].index[0]
    global shade_a
    shade_a = ax.fill_between(anodic['Potential/V'].loc[index_low:index_high],
                              anodic['Current/A'].loc[index_low:index_high], init_anodic_A, color=color)
    index_low_c = anodic.iloc[(cathodic['Potential/V'] - min_potential).abs().argsort()[:1]].index[0]
    index_high_c = anodic.iloc[(cathodic['Potential/V'] - init_anodic_V).abs().argsort()[:1]].index[0]
    global shade_c
    shade_c = ax.fill_between(cathodic['Potential/V'].loc[index_high_c:index_low_c],
                              cathodic['Current/A'].loc[index_high_c:index_low_c], init_cathodic_A, color=color)

    area_a = np.trapezoid(x=anodic['Potential/V'].loc[index_low:index_high],
                      y=anodic['Current/A'].loc[index_low:index_high] - init_anodic_A)
    area_c = np.trapezoid(x=cathodic['Potential/V'].loc[index_high_c:index_low_c],
                      y=cathodic['Current/A'].loc[index_high_c:index_low_c] - init_cathodic_A)
    global area
    area = (abs(area_a) + abs(area_c)) / 2
    area = (area / float(Ar_config[1])) / 210e-6

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
        global area_norm
        area_norm = area / loading * 0.0001

    global rf
    area_geo = np.pi * (float(RadiusEntry.get()) ** 2)
    rf = area / area_geo

    def dragged():
        upper_potential = Tline2.getvalue()
        lower_potential = Tline.getvalue()
        anodic_dl = Vline.getvalue()
        cathodic_dl = Vline2.getvalue()

        index_low = anodic.iloc[(anodic['Potential/V'] - lower_potential).abs().argsort()[:1]].index[0]
        index_high = anodic.iloc[(anodic['Potential/V'] - upper_potential).abs().argsort()[:1]].index[0]
        index_low_c = anodic.iloc[(cathodic['Potential/V'] - lower_potential).abs().argsort()[:1]].index[0]
        index_high_c = anodic.iloc[(cathodic['Potential/V'] - upper_potential).abs().argsort()[:1]].index[0]
        global shade_a
        shade_a.remove()
        shade_a = ax.fill_between(anodic['Potential/V'].loc[index_low:index_high],
                                  anodic['Current/A'].loc[index_low:index_high], anodic_dl, color=color)
        global shade_c
        shade_c.remove()
        shade_c = ax.fill_between(cathodic['Potential/V'].loc[index_high_c:index_low_c],
                                  cathodic['Current/A'].loc[index_high_c:index_low_c], cathodic_dl, color=color)

        area_a = np.trapezoid(x=anodic['Potential/V'].loc[index_low:index_high],
                          y=anodic['Current/A'].loc[index_low:index_high] - anodic_dl)
        area_c = np.trapezoid(x=cathodic['Potential/V'].loc[index_high_c:index_low_c],
                          y=cathodic['Current/A'].loc[index_high_c:index_low_c] - cathodic_dl)

        global area
        area = (abs(area_a) + abs(area_c)) / 2
        area = (area / float(Ar_config[1])) / 210e-6

        if LoadingEntry.get() != '':
            global loading
            loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
            global area_norm
            area_norm = area / loading * 0.0001

        global rf
        area_geo = np.pi * (float(RadiusEntry.get()) ** 2)
        rf = area / area_geo

        rf_label.configure(text='{0:.3f}'.format(rf))
        Area_label.configure(text='{0:.3f}'.format(area))
        if 'area_norm' in globals():
            Area_norm_label.configure(text='{0:.3f}'.format(area_norm))
        else:
            Area_norm_label.configure(text='n.a.')

    class draggable_lines:
        def __init__(self, canvas, ax, kind, XorY):
            self.ax = ax
            self.c = canvas
            self.o = kind
            self.XorY = XorY

            if kind == "h":
                x = [min_potential, max_potential]
                y = [XorY, XorY]

            elif kind == "v":
                x = [XorY, XorY]
                y = [min_current, max_current]
            self.line = lines.Line2D(x, y, picker=5, color=fgcolor, linestyle='dashed', linewidth=0.5)
            self.ax.add_line(self.line)
            self.c.draw_idle()
            self.c.mpl_connect('pick_event', self.clickonline)

        def clickonline(self, event):
            if event.artist == self.line:
                # print("line selected ", event.artist)
                self.follower = self.c.mpl_connect("motion_notify_event", self.followmouse)
                self.releaser = self.c.mpl_connect("button_press_event", self.releaseonclick)

        def followmouse(self, event):
            if self.o == "h":
                self.line.set_ydata([event.ydata, event.ydata])
            else:
                self.line.set_xdata([event.xdata, event.xdata])
            self.c.draw_idle()

        def releaseonclick(self, event):
            if self.o == "h":
                self.XorY = self.line.get_ydata()[0]
            else:
                self.XorY = self.line.get_xdata()[0]

            # print(self.XorY)
            dragged()
            self.c.draw_idle()
            self.c.mpl_disconnect(self.releaser)
            self.c.mpl_disconnect(self.follower)

        def getvalue(self):
            return self.XorY

    Vline = draggable_lines(canvas, ax, "h", init_anodic_A)
    Vline2 = draggable_lines(canvas, ax, "h", init_cathodic_A)
    Tline = draggable_lines(canvas, ax, "v", min_potential)
    Tline2 = draggable_lines(canvas, ax, "v", init_anodic_V)

    canvas.draw_idle()

    # info_frame.grid_columnconfigure(0, minsize=140)
    variable_frame = ct.CTkFrame(master=info_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
    variable_frame.grid(row=1, column=1, sticky='nswe', pady=10, padx=10)
    variable_frame.grid_columnconfigure(0, weight=1, minsize=280)
    variable_frame.grid_rowconfigure(0, weight=1)
    variable_frame.grid_rowconfigure(1, weight=1)
    variable_frame.grid_rowconfigure(2, weight=1)

    Area_norm_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    Area_norm_frame.grid(row=2, column=0, sticky='nswe', pady=5, padx=5)
    Area_norm_frame.grid_rowconfigure(0, weight=0)
    Area_norm_frame.grid_rowconfigure(1, weight=1)
    Area_norm_frame.grid_rowconfigure(2, weight=0)
    Area_norm_frame.grid_columnconfigure(0, weight=0, minsize=80)
    Area_norm_frame.grid_columnconfigure(1, weight=1, minsize=80)
    Area_norm_frame.grid_columnconfigure(2, weight=0, minsize=125)
    if LoadingEntry.get() != '':
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='{0:.3f}'.format(area_norm), font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    else:
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='n.a.', font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_norm_frame, text='ECSA:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E,
                                                                                    padx=2)
    ct.CTkLabel(Area_norm_frame, text='m²ₚₜ/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E,
                                                                                       padx=2)

    rf_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    rf_frame.grid(row=1, column=0, sticky='nswe', pady=0, padx=5)
    rf_frame.grid_rowconfigure(0, weight=0)
    rf_frame.grid_rowconfigure(1, weight=1)
    rf_frame.grid_rowconfigure(2, weight=0)
    rf_frame.grid_columnconfigure(0, weight=0, minsize=80)
    rf_frame.grid_columnconfigure(1, weight=1, minsize=80)
    rf_frame.grid_columnconfigure(2, weight=0, minsize=125)
    rf_label = ct.CTkLabel(rf_frame, text='{0:.3f}'.format(rf), font=("Calibri", -20), width=1)
    rf_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(rf_frame, text='rf:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(rf_frame, text='cm²ₚₜ/cm²₉ₑₒ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E,
                                                                                    padx=2)

    Area_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    Area_frame.grid(row=0, column=0, sticky='nswe', pady=5, padx=5)
    Area_frame.grid_rowconfigure(0, weight=0)
    Area_frame.grid_rowconfigure(1, weight=1)
    Area_frame.grid_rowconfigure(2, weight=0)
    Area_frame.grid_columnconfigure(0, weight=0, minsize=80)
    Area_frame.grid_columnconfigure(1, weight=1, minsize=80)
    Area_frame.grid_columnconfigure(2, weight=0, minsize=125)
    Area_label = ct.CTkLabel(Area_frame, text='{0:.3f}'.format(area), font=("Calibri", -20), width=1)
    Area_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_frame, text='Area Pt:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(Area_frame, text='cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    def exit1():
        window.destroy()
        global z

        a = z

        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=160)
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=140)
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=20)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='HUPD Determination - ', font=("Calibri", -20), width=140).grid(row=0,
                                                                                                                 column=0,
                                                                                                                 sticky=tk.W,
                                                                                                                 padx=2,
                                                                                                                 pady=5)
        d['v_n_{0}'.format(z)] = ct.CTkEntry(d['v_f_{0}'.format(z)], width=140, border_width=0,
                                             bg_color=("grey70", 'grey30'), fg_color=("grey70", 'grey30'),
                                             font=("Calibri", -19), text_color=('black', 'white'))
        d['v_n_{0}'.format(z)].insert(0, NameEntry.get())
        d['v_n_{0}'.format(z)].configure(state='disabled')
        d['v_n_{0}'.format(z)].grid(row=0, column=1, sticky='ws', pady=5)
        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x', width=8, height=8, command=lambda: remove(a),
                     font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=2, sticky=tk.E, pady=5,
                                                                                  padx=5)

        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['a_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                             fg_color=('grey80', 'grey20'))
        d['a_f_{0}'.format(z)].grid(row=1, column=0, columnspan=3, sticky='nswe', pady=5, padx=5, ipadx=2, ipady=2)
        d['a_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['a_l_{0}'.format(z)] = ct.CTkLabel(d['a_f_{0}'.format(z)], text='{0:.3f}'.format(area), font=("Calibri", -20),
                                             width=1)
        d['a_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='Area Pt:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                                  sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                               sticky=tk.E, padx=2)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                              fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, columnspan=3, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(rf), font=("Calibri", -20),
                                              width=1)
        d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='rf:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                              sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='cm²ₚₜ/cm²₉ₑₒ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                       sticky=tk.E,
                                                                                                       padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                               fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0, columnspan=3, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(area_norm),
                                                   font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20),
                                                   width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='ECSA:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                                 sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='m²ₚₜ/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                    sticky=tk.E, padx=2)

        data_canvas.update_idletasks()
        data_canvas.configure(scrollregion=data_frame.bbox())

        df = pd.concat([anodic, cathodic], ignore_index=True).reset_index()
        df.rename(columns={'Potential/V': 'Potential/V_' + 'HUPD_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df.rename(columns={'Current/A': 'Current/A_' + 'HUPD_' + str(z)}, inplace=True)
        del df['index']
        global savefile
        savefile = pd.concat([savefile, df], axis=1)

        if LoadingEntry.get() != '':
            ecsa = area_norm
        else:
            ecsa = 'n.a.'

        result = pd.DataFrame(
            {'HUPD_Area_cm^2_Pt_' + NameEntry.get() + '_' + str(z): [area], 'HUPD_rf_cm^2_Pt/cm^2_geo_' + str(z): [rf],
             'HUPD_ECSA_cm^2_Pt/g_Pt_' + str(z): [ecsa]})
        global results
        results = pd.concat([results, result], axis=1)

        save_enable()

        z += 1

    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=exit1, font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    window.mainloop()


def O2_plot(O2, Ar):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('ORR Evaluation')
    window.geometry(
        str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(
            int(d_x + widthfactor * 8)) + '+' + str(int(d_y + heightfactor * 299)))
    # window.configure(background='white')
    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        window.configure(bg='grey90')
    window.overrideredirect(True)
    window.attributes("-topmost", True)
    window.grid_columnconfigure(0, weight=3)
    window.grid_columnconfigure(1, weight=2, minsize=350)
    window.grid_rowconfigure(0, weight=1)
    o2_graph_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    o2_graph_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)

    o2_graph_frame.grid_rowconfigure(0, weight=0)
    o2_graph_frame.grid_rowconfigure(1, weight=1)
    o2_graph_frame.grid_columnconfigure(0, weight=0, minsize=10)
    o2_graph_frame.grid_columnconfigure(1, weight=1)
    o2_graph_frame.grid_columnconfigure(2, weight=0, minsize=10)

    o2_f = Figure(figsize=(28 * cm, 18 * cm), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(o2_f, master=o2_graph_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, o2_graph_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax_o2 = o2_f.add_subplot(1, 1, 1)
    ax_o2.set_ylabel("Current [A]")
    ax_o2.set_xlabel("Potential [V]")
    ax_o2.set_facecolor(bgcolor)
    ax_o2.xaxis.label.set_color(fgcolor)
    ax_o2.yaxis.label.set_color(fgcolor)
    ax_o2.tick_params(axis='x', colors=fgcolor)
    ax_o2.tick_params(axis='y', colors=fgcolor)
    ax_o2.spines['left'].set_color(fgcolor)
    ax_o2.spines['top'].set_color(fgcolor)
    ax_o2.spines['right'].set_color(fgcolor)
    ax_o2.spines['bottom'].set_color(fgcolor)

    O2['Potential/V'] = O2['Potential/V'] - (O2['Current/A'] * float(R)) - float(Ref)
    Ar['Potential/V'] = Ar['Potential/V'] - (Ar['Current/A'] * float(R)) - float(Ref)

    df = interpolation(O2, Ar)

    df['Diff/A'] = df['Current/A_1'] - df['Current/A_2']

    df = df.rename(columns={'Potential/V': 'E-iR/V'})

    max_current = df['Diff/A'].loc[df['Diff/A'].nlargest(1).index[0]]
    min_current = df['Diff/A'].loc[df['Diff/A'].nsmallest(1).index[0]]

    index_low = df.iloc[(df['E-iR/V'] - 0.3).abs().argsort()[:1]].index[0]
    index_high = df.iloc[(df['E-iR/V'] - 0.5).abs().argsort()[:1]].index[0]

    global i_limiting
    i_limiting = df['Diff/A'].loc[index_low:index_high].mean()

    global dflim
    dflim = df[(df['Diff/A'] >= (i_limiting * 0.5)) & (df['Diff/A'] <= (i_limiting * 0.01))].reset_index()
    dflim = dflim.rename(columns={'E-iR/V': 'E-iR(lim)/V', 'Diff/A': 'Diff(lim)/A'})

    dflim['E-iR-etadiff(lim)/V'] = dflim['E-iR(lim)/V'] - (
                (8.31446 * Temp) / (4 * 96485) * np.log(1 - (dflim['Diff(lim)/A'] / i_limiting)))

    dflim.drop(columns={'index', 'Current/A_1', 'Current/A_2'}, inplace=True)

    dflim['ik/A'] = (i_limiting * dflim['Diff(lim)/A']) / (i_limiting - dflim['Diff(lim)/A'])

    index_0pt9 = df.iloc[(dflim['E-iR(lim)/V'] - 0.9).abs().argsort()[:1]].index[0]

    tafel = dflim[['E-iR(lim)/V', 'E-iR-etadiff(lim)/V', 'ik/A']].dropna()
    tafel = tafel.iloc[::-1].reset_index()
    del tafel['index']
    tafel['ik/A'] = abs(tafel['ik/A'])
    c = 0
    e = 0

    if int(tafel.shape[0] * 0.01) >= 5:
        start = int(tafel.shape[0] * 0.01)
    else:
        start = 5

    for i in range(tafel.shape[0] - start):

        df1 = tafel.head(start + i)
        linear = linregress(np.log10(df1['ik/A']), df1['E-iR(lim)/V'])
        linear1 = linregress(np.log10(df1['ik/A']), df1['E-iR-etadiff(lim)/V'])

        if (-1 * linear[2]) >= c:
            c = (-1 * linear[2])
            coefficents = linear
        if (-1 * linear1[2]) >= e:
            e = (-1 * linear1[2])
            coefficents1 = linear1

    ik_expol = 10 ** ((0.9 - coefficents[1]) / (coefficents[0]))
    ik_expol_etadiff = 10 ** ((0.9 - coefficents1[1]) / (coefficents1[0]))

    global i_surface_0pt9
    global i_s_expol
    global i_s_expol_etadiff

    if 'co_area' in globals():
        dflim['is/A'] = abs(dflim['ik/A']) / co_area * 1000 * 1000
        i_surface_0pt9 = dflim['is/A'].loc[index_0pt9]
        i_s_expol = ik_expol / co_area * 1000 * 1000
        i_s_expol_etadiff = ik_expol_etadiff / co_area * 1000 * 1000

    if 'co_area' not in globals() and 'area' in globals():
        dflim['is/A'] = abs(dflim['ik/A']) / area * 1000 * 1000
        i_surface_0pt9 = dflim['is/A'].loc[index_0pt9]
        i_s_expol = ik_expol / area * 1000 * 1000
        i_s_expol_etadiff = ik_expol_etadiff / area * 1000 * 1000

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
        dflim['im/A'] = abs(dflim['ik/A']) / loading
        global i_mass_0pt9
        i_mass_0pt9 = dflim['im/A'].loc[index_0pt9]
        global i_m_expol
        global i_m_expol_etadiff
        i_m_expol = ik_expol / loading
        i_m_expol_etadiff = ik_expol_etadiff / loading

    if 'RingCurrent/A_1' in df:
        #ax_o2_r = ax_o2.twinx()
        ax_o2.plot(df['E-iR/V'], df['RingCurrent/A_1'], label='Ring1', zorder=1)
        #ax_o2_r.set_ylabel("Ring Current [A]")
    if 'RingCurrent/A_2' in df:
        #ax_o2_r2 = ax_o2.twinx()
        ax_o2.plot(df['E-iR/V'], df['RingCurrent/A_2'], label='Ring2', zorder=1)
        #ax_o2.set_ylabel("Ring Current [A]")


    ax_o2.plot(df['E-iR/V'], df['Diff/A'], label='ORR_corrected', zorder=3)
    ax_o2.plot(df['E-iR/V'], df['Current/A_1'], 'w--', label='O2', zorder=3)
    ax_o2.plot(df['E-iR/V'], df['Current/A_2'], 'k--', label='Ar', zorder=3)



    legend = ax_o2.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

    def dragged():
        lower_potential = Tline.getvalue()
        upper_potential = Tline2.getvalue()

        index_low = df.iloc[(df['E-iR/V'] - lower_potential).abs().argsort()[:1]].index[0]
        index_high = df.iloc[(df['E-iR/V'] - upper_potential).abs().argsort()[:1]].index[0]
        global i_limiting
        i_limiting = df['Diff/A'].loc[index_low:index_high].mean()

        global dflim
        dflim = df[(df['Diff/A'] >= (i_limiting * 0.5)) & (df['Diff/A'] <= (i_limiting * 0.01))].reset_index()
        dflim = dflim.rename(columns={'E-iR/V': 'E-iR(lim)/V', 'Diff/A': 'Diff(lim)/A'})
        dflim['E-iR-etadiff(lim)/V'] = dflim['E-iR(lim)/V'] - (
                    (8.31446 * Temp) / (4 * 96485) * np.log(1 - (dflim['Diff(lim)/A'] / i_limiting)))
        dflim.drop(columns={'index', 'Current/A_1', 'Current/A_2'}, inplace=True)
        dflim['ik/A'] = (i_limiting * dflim['Diff(lim)/A']) / (i_limiting - dflim['Diff(lim)/A'])

        index_0pt9 = df.iloc[(dflim['E-iR(lim)/V'] - 0.9).abs().argsort()[:1]].index[0]

        il_label.configure(text='{0:.3e}'.format(i_limiting))

        tafel = dflim[['E-iR(lim)/V', 'E-iR-etadiff(lim)/V', 'ik/A']].dropna()
        tafel = tafel.iloc[::-1].reset_index()
        del tafel['index']
        tafel['ik/A'] = abs(tafel['ik/A'])
        c = 0
        e = 0

        if int(tafel.shape[0] * 0.01) >= 5:
            start = int(tafel.shape[0] * 0.01)
        else:
            start = 5

        for i in range(tafel.shape[0] - start):

            df1 = tafel.head(start + i)
            linear = linregress(np.log10(df1['ik/A']), df1['E-iR(lim)/V'])
            linear1 = linregress(np.log10(df1['ik/A']), df1['E-iR-etadiff(lim)/V'])

            if (-1 * linear[2]) >= c:
                c = (-1 * linear[2])
                coefficents = linear
            if (-1 * linear1[2]) >= e:
                e = (-1 * linear1[2])
                coefficents1 = linear1

        ik_expol = 10 ** ((0.9 - coefficents[1]) / (coefficents[0]))
        ik_expol_etadiff = 10 ** ((0.9 - coefficents1[1]) / (coefficents1[0]))

        global i_surface_0pt9
        global i_s_expol
        global i_s_expol_etadiff

        if 'co_area' in globals():
            dflim['is/A'] = abs(dflim['ik/A']) / co_area * 1000 * 1000
            i_surface_0pt9 = dflim['is/A'].loc[index_0pt9]
            i_s_expol = ik_expol / co_area * 1000 * 1000
            i_s_expol_etadiff = ik_expol_etadiff / co_area * 1000 * 1000
            is_label.configure(text='{0:.3f}'.format(i_surface_0pt9))
            is_label_ex.configure(text='{0:.3f}'.format(i_s_expol))


        elif 'co_area' not in globals() and 'area' in globals():
            dflim['is/A'] = abs(dflim['ik/A']) / area * 1000 * 1000
            i_surface_0pt9 = dflim['is/A'].loc[index_0pt9]
            i_s_expol = ik_expol / area * 1000 * 1000
            i_s_expol_etadiff = ik_expol_etadiff / area * 1000 * 1000
            is_label.configure(text='{0:.3f}'.format(i_surface_0pt9))
            is_label_ex.configure(text='{0:.3f}'.format(i_s_expol))

        else:
            is_label.configure(text='n.a.')
            is_label_ex.configure(text='n.a.')

        if LoadingEntry.get() != '':
            global loading
            loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
            dflim['im/A'] = abs(dflim['ik/A']) / loading
            global i_mass_0pt9
            i_mass_0pt9 = dflim['im/A'].loc[index_0pt9]
            im_label.configure(text='{0:.3f}'.format(i_mass_0pt9))
            global i_m_expol
            global i_m_expol_etadiff
            i_m_expol = ik_expol / loading
            i_m_expol_etadiff = ik_expol_etadiff / loading
            im_label_ex.configure(text='{0:.3f}'.format(i_m_expol))

        else:
            im_label.configure(text='n.a.')
            im_label_ex.configure(text='n.a.')

    class draggable_line:
        def __init__(self, canvas, ax, kind, XorY):
            self.ax = ax
            self.c = canvas
            self.o = kind
            self.XorY = XorY

            if kind == "h":
                x = [-1, 1]
                y = [XorY, XorY]

            elif kind == "v":
                x = [XorY, XorY]
                y = [min_current, max_current]
            self.line = lines.Line2D(x, y, picker=5, color=fgcolor, linestyle='dashed', linewidth=0.5)
            self.ax.add_line(self.line)
            self.c.draw_idle()
            self.c.mpl_connect('pick_event', self.clickonline)

        def clickonline(self, event):
            if event.artist == self.line:
                # print("line selected ", event.artist)
                self.follower = self.c.mpl_connect("motion_notify_event", self.followmouse)
                self.releaser = self.c.mpl_connect("button_press_event", self.releaseonclick)

        def followmouse(self, event):
            if self.o == "h":
                self.line.set_ydata([event.ydata, event.ydata])
            else:
                self.line.set_xdata([event.xdata, event.xdata])
            self.c.draw_idle()

        def releaseonclick(self, event):
            if self.o == "h":
                self.XorY = self.line.get_ydata()[0]
            else:
                self.XorY = self.line.get_xdata()[0]

            # print(self.XorY)
            dragged()
            self.c.mpl_disconnect(self.releaser)
            self.c.mpl_disconnect(self.follower)

        def getvalue(self):
            return self.XorY

    Tline = draggable_line(canvas, ax_o2, "v", 0.3)
    Tline2 = draggable_line(canvas, ax_o2, "v", 0.5)

    canvas.draw_idle()

    info_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    info_frame.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)

    info_frame.grid_rowconfigure(0, weight=10)
    info_frame.grid_rowconfigure(1, weight=1)
    info_frame.grid_rowconfigure(2, weight=10)
    info_frame.grid_columnconfigure(0, weight=0)
    info_frame.grid_columnconfigure(1, weight=1)
    info_frame.grid_columnconfigure(2, weight=0)
    # info_frame.grid_columnconfigure(0, minsize=140)
    variable_frame = ct.CTkFrame(master=info_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
    variable_frame.grid(row=1, column=1, sticky='nswe', pady=10, padx=10)
    variable_frame.grid_columnconfigure(0, weight=1, minsize=300)
    variable_frame.grid_rowconfigure(0, weight=1)
    variable_frame.grid_rowconfigure(1, weight=1)
    variable_frame.grid_rowconfigure(2, weight=1)

    is_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    is_frame.grid(row=1, column=0, sticky='nswe', pady=0, padx=5)
    is_frame.grid_rowconfigure(0, weight=0)
    is_frame.grid_rowconfigure(1, weight=1)
    is_frame.grid_rowconfigure(2, weight=0)
    is_frame.grid_rowconfigure(3, weight=1)
    is_frame.grid_rowconfigure(4, weight=0)
    is_frame.grid_columnconfigure(0, weight=0, minsize=80)
    is_frame.grid_columnconfigure(1, weight=1, minsize=115)
    is_frame.grid_columnconfigure(2, weight=0, minsize=90)
    if any(var in globals() for var in ['co_area', 'area']):
        is_label = ct.CTkLabel(is_frame, text='{0:.3f}'.format(i_surface_0pt9), font=("Calibri", -20), width=1)
        is_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        is_label_ex = ct.CTkLabel(is_frame, text='{0:.3f}'.format(i_s_expol), font=("Calibri", -20), width=1)
        is_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    else:
        is_label = ct.CTkLabel(is_frame, text='n.a.', font=("Calibri", -20), width=1)
        is_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        is_label_ex = ct.CTkLabel(is_frame, text='n.a.', font=("Calibri", -20), width=1)
        is_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(is_frame, text='iₛ:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='iₛ ex:', font=("Calibri", -20), width=1).grid(row=3, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2, sticky=tk.E, padx=2)

    im_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    im_frame.grid(row=2, column=0, sticky='nswe', pady=5, padx=5)
    im_frame.grid_rowconfigure(0, weight=0)
    im_frame.grid_rowconfigure(1, weight=1)
    im_frame.grid_rowconfigure(2, weight=0)
    im_frame.grid_rowconfigure(3, weight=1)
    im_frame.grid_rowconfigure(4, weight=0)
    im_frame.grid_columnconfigure(0, weight=0, minsize=80)
    im_frame.grid_columnconfigure(1, weight=1, minsize=115)
    im_frame.grid_columnconfigure(2, weight=0, minsize=90)
    if LoadingEntry.get() != '':
        im_label = ct.CTkLabel(im_frame, text='{0:.3f}'.format(i_mass_0pt9), font=("Calibri", -20), width=1)
        im_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        im_label_ex = ct.CTkLabel(im_frame, text='{0:.3f}'.format(i_m_expol), font=("Calibri", -20), width=1)
        im_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    else:
        im_label = ct.CTkLabel(im_frame, text='n.a.', font=("Calibri", -20), width=1)
        im_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        im_label_ex = ct.CTkLabel(im_frame, text='n.a.', font=("Calibri", -20), width=1)
        im_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(im_frame, text='iₘ:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='iₘ ex:', font=("Calibri", -20), width=1).grid(row=3, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2, sticky=tk.E, padx=2)

    il_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    il_frame.grid(row=0, column=0, sticky='nswe', pady=5, padx=5)
    il_frame.grid_rowconfigure(0, weight=0)
    il_frame.grid_rowconfigure(1, weight=1)
    il_frame.grid_rowconfigure(2, weight=0)
    il_frame.grid_columnconfigure(0, weight=0, minsize=80)
    il_frame.grid_columnconfigure(1, weight=1, minsize=115)
    il_frame.grid_columnconfigure(2, weight=0, minsize=90)
    il_label = ct.CTkLabel(il_frame, text='{0:.3e}'.format(i_limiting), font=("Calibri", -20), width=1)
    il_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(il_frame, text='iₗᵢₘ:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(il_frame, text='A', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    def exit1(df):
        window.destroy()
        global z
        a = z
        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=140)
        d['v_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=160)
        d['v_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=20)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='ORR Determination - ', font=("Calibri", -20), width=140).grid(row=0,
                                                                                                                column=0,
                                                                                                                sticky=tk.W,
                                                                                                                padx=2,
                                                                                                                pady=5)
        d['v_n_{0}'.format(z)] = ct.CTkEntry(d['v_f_{0}'.format(z)], width=160, border_width=0,
                                             bg_color=("grey70", 'grey30'), fg_color=("grey70", 'grey30'),
                                             font=("Calibri", -19), text_color=('black', 'white'))
        d['v_n_{0}'.format(z)].insert(0, NameEntry.get())
        d['v_n_{0}'.format(z)].configure(state='disabled')
        d['v_n_{0}'.format(z)].grid(row=0, column=1, sticky='ws', pady=5)
        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x', width=8, height=8, command=lambda: remove(a),
                     font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=2, sticky=tk.E, pady=5,
                                                                                  padx=5)

        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['a_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                             fg_color=('grey80', 'grey20'))
        d['a_f_{0}'.format(z)].grid(row=1, column=0, sticky='nswe', pady=5, padx=5, ipadx=2, ipady=2, columnspan=3)
        d['a_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['a_l_{0}'.format(z)] = ct.CTkLabel(d['a_f_{0}'.format(z)], text='{0:.3e}'.format(i_limiting),
                                             font=("Calibri", -20), width=1)
        d['a_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='iₗᵢₘ:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                               sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='A', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E,
                                                                                           padx=2)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                              fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2, columnspan=3)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(4, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if any(var in globals() for var in ['co_area', 'area']):
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(i_surface_0pt9),
                                                  font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(i_s_expol),
                                                  font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        else:
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='iₛ:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                              sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                   sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='iₛ ex:', font=("Calibri", -20), width=1).grid(row=3, column=0,
                                                                                                 sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2,
                                                                                                   sticky=tk.E, padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                               fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2, columnspan=3)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(i_mass_0pt9),
                                                   font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(i_m_expol),
                                                   font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20),
                                                   width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20),
                                                   width=1)
            d['a_n_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='iₘ:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                               sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                 sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='iₘ ex:', font=("Calibri", -20), width=1).grid(row=3, column=0,
                                                                                                  sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2,
                                                                                                 sticky=tk.E, padx=2)

        data_canvas.update_idletasks()
        data_canvas.configure(scrollregion=data_frame.bbox())

        df.rename(columns={'E-iR/V': 'E-iR/V_' + 'ORR_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df.rename(columns={'Diff/A': 'Current/A_' + 'ORR_' + str(z)}, inplace=True)
        if 'RingCurrent/A_1' in df.columns:
            df.rename(columns={'RingCurrent/A_1': 'RingCurrent/A1_' + 'ORR_' + str(z)}, inplace=True)
        if 'RingCurrent/A_2' in df.columns:
            df.rename(columns={'RingCurrent/A_2': 'RingCurrent/A2_' + 'ORR_' + str(z)}, inplace=True)

        del df['Current/A_1']
        del df['Current/A_2']
        # del df['Potential/V']

        global dflim
        dflim.rename(columns={'E-iR(lim)/V': 'E-iR(lim)/V_' + 'ORR_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        dflim.rename(columns={'E-iR-etadiff(lim)/V': 'E-iR-etadiff(lim)/V_' + 'ORR_' + str(z)}, inplace=True)
        dflim.rename(columns={'Diff(lim)/A': 'Current(lim)/A_' + 'ORR_' + str(z)}, inplace=True)
        dflim.rename(columns={'ik/A': 'ik/A_' + 'ORR_' + str(z)}, inplace=True)

        tafel = dflim[
            ['E-iR(lim)/V_' + 'ORR_' + NameEntry.get() + '_' + str(z), 'E-iR-etadiff(lim)/V_' + 'ORR_' + str(z),
             'ik/A_' + 'ORR_' + str(z)]].dropna()
        tafel = tafel.iloc[::-1].reset_index()
        del tafel['index']
        tafel['ik/A_' + 'ORR_' + str(z)] = abs(tafel['ik/A_' + 'ORR_' + str(z)])
        c = 0
        e = 0

        if int(tafel.shape[0] * 0.01) >= 5:
            start = int(tafel.shape[0] * 0.01)
        else:
            start = 5

        for i in range(tafel.shape[0] - start):

            df1 = tafel.head(start + i)
            linear = linregress(np.log10(df1['ik/A_' + 'ORR_' + str(z)]),
                                df1['E-iR(lim)/V_' + 'ORR_' + NameEntry.get() + '_' + str(z)])
            linear1 = linregress(np.log10(df1['ik/A_' + 'ORR_' + str(z)]),
                                 df1['E-iR-etadiff(lim)/V_' + 'ORR_' + str(z)])

            if (-1 * linear[2]) >= c:
                c = (-1 * linear[2])
                coefficents = linear
            if (-1 * linear1[2]) >= e:
                e = (-1 * linear1[2])
                coefficents1 = linear1

        plt.plot(tafel['ik/A_' + 'ORR_' + str(z)], tafel['E-iR(lim)/V_' + 'ORR_' + NameEntry.get() + '_' + str(z)],
                 label='iR-free')
        plt.plot(tafel['ik/A_' + 'ORR_' + str(z)], tafel['E-iR-etadiff(lim)/V_' + 'ORR_' + str(z)],
                 label='etadiff-free')
        plt.plot(tafel['ik/A_' + 'ORR_' + str(z)],
                 coefficents[0] * np.log10(tafel['ik/A_' + 'ORR_' + str(z)]) + coefficents[1])
        plt.plot(tafel['ik/A_' + 'ORR_' + str(z)],
                 coefficents1[0] * np.log10(tafel['ik/A_' + 'ORR_' + str(z)]) + coefficents1[1])
        plt.plot(tafel['ik/A_' + 'ORR_' + str(z)], np.linspace(0.9, 0.9, tafel['ik/A_' + 'ORR_' + str(z)].shape[0]))
        plt.xscale('log')
        plt.legend()
        plt.show()

        ik_expol = 10 ** ((0.9 - coefficents[1]) / (coefficents[0]))
        ik_expol_etadiff = 10 ** ((0.9 - coefficents1[1]) / (coefficents1[0]))

        # ik_expol = interpolate.interp1d(x=(coefficents[0] * np.log10(tafel['ik/A_' + 'ORR_' + str(z)]) + coefficents[1]), y=tafel['ik/A_' + 'ORR_' + str(z)], kind='linear')(0.9)
        # ik_expol_etadiff = interpolate.interp1d(x=(coefficents1[0] * np.log10(tafel['ik/A_' + 'ORR_' + str(z)]) + coefficents1[1]), y=tafel['ik/A_' + 'ORR_' + str(z)], kind='linear')(0.9)

        if 'is/A' in dflim:
            dflim.rename(columns={'is/A': 'is/A_' + 'ORR_' + str(z)}, inplace=True)
        if 'im/A' in dflim:
            dflim.rename(columns={'im/A': 'im/A_' + 'ORR_' + str(z)}, inplace=True)

        dflim['ik/A_tafel_' + 'ORR_' + str(z)] = tafel['ik/A_' + 'ORR_' + str(z)]
        dflim['im/A_tafel_' + 'ORR_' + str(z)] = tafel['ik/A_' + 'ORR_' + str(z)] / (float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6)))
        dflim['is/A_tafel_' + 'ORR_' + str(z)] = tafel['ik/A_' + 'ORR_' + str(z)] / area * 1000 * 1000
        dflim['E-iR/V_tafel_' + 'ORR_' + str(z)] = coefficents[0] * np.log10(tafel['ik/A_' + 'ORR_' + str(z)]) + \
                                                   coefficents[1]
        dflim['E-iR-etadiff/V_tafel_' + 'ORR_' + str(z)] = coefficents1[0] * np.log10(
            tafel['ik/A_' + 'ORR_' + str(z)]) + coefficents1[1]

        global savefile
        savefile = pd.concat([savefile, df], axis=1)
        savefile = pd.concat([savefile, dflim], axis=1)

        if LoadingEntry.get() != '':
            i_m = i_mass_0pt9
            global loading
            loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
            i_m_ex = ik_expol / loading
            i_m_ex_eta = ik_expol_etadiff / loading


        else:
            i_m = 'n.a.'
            i_m_ex = 'n.a.'
            i_m_ex_eta = 'n.a.'

        if 'co_area' in globals():
            i_s = i_surface_0pt9
            i_s_ex = ik_expol / co_area * 1000 * 1000
            i_s_ex_eta = ik_expol_etadiff / co_area * 1000 * 1000


        elif 'co_area' not in globals() and 'area' in globals():
            i_s = i_surface_0pt9
            i_s_ex = ik_expol / area * 1000 * 1000
            i_s_ex_eta = ik_expol_etadiff / area * 1000 * 1000

        else:
            i_s = 'n.a.'
            i_s_ex = 'n.a.'
            i_s_ex_eta = 'n.a.'

        result = pd.DataFrame(
            {'ORR_i_lim_A_' + NameEntry.get() + '_' + str(z): [i_limiting], 'ORR_i_s_A/cm^2_Pt_' + str(z): [i_s],
             'ORR_i_m_A/g_Pt_' + str(z): [i_m],
             'ORR_i_k_ex_A_' + str(z): [ik_expol], 'ORR_i_s_ex_A/cm^2_Pt_' + str(z): [i_s_ex],
             'ORR_i_m_ex_A/g_Pt_' + str(z): [i_m_ex],
             'ORR_i_k_ex_eta_A_' + str(z): [ik_expol_etadiff], 'ORR_i_s_ex_eta_A/cm^2_Pt_' + str(z): [i_s_ex_eta],
             'ORR_i_m_ex_eta_A/g_Pt_' + str(z): [i_m_ex_eta],
             'ORR_Tafel_slope_mV/dec_' + str(z): [coefficents[0]], 'ORR_Tafel_intercept_' + str(z): [coefficents[1]],
             'ORR_Tafel_R_' + str(z): [coefficents[2]],
             'ORR_Tafel_slope_eta_mV/dec_' + str(z): [coefficents1[0]], 'ORR_Tafel_intercept_eta_' + str(z): [coefficents1[1]],
             'ORR_Tafel_R_eta' + str(z): [coefficents1[2]]})
        global results
        results = pd.concat([results, result], axis=1)

        save_enable()

        z += 1

    button_frame = ct.CTkFrame(master=info_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    button_frame.grid(row=2, column=1, sticky='nswe', pady=10, padx=10)
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=0)
    button_frame.grid_columnconfigure(2, weight=0)
    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=lambda: exit1(df), font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)

    def on_closing():
        window.destroy()
        # exit()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()


def HOR_plot(df1, df2):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('HOR Evaluation')
    window.geometry(
        str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(
            int(d_x + widthfactor * 8)) + '+' + str(int(d_y + heightfactor * 299)))
    # window.configure(background='white')
    if ct.get_appearance_mode() == 'Dark':
        color = '#4D4D4D'
        fgcolor = 'white'
        bgcolor = '#333333'
        window.configure(bg='grey10')
    else:
        color = '#B3B3B3'
        fgcolor = 'black'
        bgcolor = '#CDCDCD'
        window.configure(bg='grey90')
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    window.grid_columnconfigure(0, weight=3)
    window.grid_columnconfigure(1, weight=2, minsize=350)
    window.grid_rowconfigure(0, weight=1)

    hor_info_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=("grey80", 'grey20'))
    hor_info_frame.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)

    hor_info_frame.grid_rowconfigure(0, weight=10)
    hor_info_frame.grid_rowconfigure(1, weight=1)
    hor_info_frame.grid_rowconfigure(2, weight=10)
    hor_info_frame.grid_columnconfigure(0, weight=0)
    hor_info_frame.grid_columnconfigure(1, weight=1)
    hor_info_frame.grid_columnconfigure(2, weight=0)

    button_frame = ct.CTkFrame(master=hor_info_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    button_frame.grid(row=2, column=1, sticky='nswe', pady=10, padx=10)
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=0)
    button_frame.grid_columnconfigure(2, weight=0)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)

    def on_closing():
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    hor_graph_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    hor_graph_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)

    hor_graph_frame.grid_rowconfigure(0, weight=0)
    hor_graph_frame.grid_rowconfigure(1, weight=1)
    hor_graph_frame.grid_columnconfigure(0, weight=0, minsize=10)
    hor_graph_frame.grid_columnconfigure(1, weight=1)
    hor_graph_frame.grid_columnconfigure(2, weight=0, minsize=10)

    hor_f = Figure(figsize=(28 * cm, 18 * cm), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(hor_f, master=hor_graph_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, hor_graph_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    df2 = df2.iloc[::-1].reset_index()

    df1['Potential/V'] = df1['Potential/V'] - (df1['Current/A'] * float(R)) - float(Ref)
    df2['Potential/V'] = df2['Potential/V'] - (df2['Current/A'] * float(R)) - float(Ref)

    df1.rename(columns={'Potential/V': 'E-iR/V'}, inplace=True)
    df2.rename(columns={'Potential/V': 'E-iR/V'}, inplace=True)

    max_current = df2['Current/A'].loc[df2['Current/A'].nlargest(1).index[0]] * 1.1
    min_current = df2['Current/A'].loc[df2['Current/A'].nsmallest(1).index[0]]

    index_low = df2.iloc[(df2['E-iR/V'] - 0.3).abs().argsort()[:1]].index[0]
    index_high = df2.iloc[(df2['E-iR/V'] - 0.5).abs().argsort()[:1]].index[0]

    index_low_1 = df1.iloc[(df1['E-iR/V'] - 0.3).abs().argsort()[:1]].index[0]
    index_high_1 = df1.iloc[(df1['E-iR/V'] - 0.5).abs().argsort()[:1]].index[0]

    global i_limiting_h
    i_limiting_h = df2['Current/A'].loc[index_low:index_high].mean()

    global i_limiting_h_1
    i_limiting_h_1 = df1['Current/A'].loc[index_low_1:index_high_1].mean()

    min_lim = df2[df2['Current/A'] > 0].iloc[0].name

    upper_limit = 0.95 * i_limiting_h
    upper_limit_1 = 0.95 * i_limiting_h_1

    max_lim = df2[(df2['Current/A'] >= upper_limit) & (df2['Current/A'] <= i_limiting_h)].iloc[0].name
    max_lim_1 = df1[(df1['Current/A'] >= upper_limit_1) & (df1['Current/A'] <= i_limiting_h_1)].iloc[0].name

    df_diff = df2.iloc[0:max_lim].reset_index()
    del df_diff['index']

    df_diff['etadiff/V'] = ((-8.314 * Temp) / (2 * 96485)) * (np.log(1 - (df_diff['Current/A'] / i_limiting_h)))

    df1_red = df1.iloc[0:max_lim_1].reset_index()
    df2_red = df2.iloc[0:max_lim].reset_index()

    df2_filtered_HOR = df2_red[(df2_red['E-iR/V'] >= 0)]
    df2_filtered_HER = df2_red[(df2_red['E-iR/V'] >= -0.01) & (df2_red['E-iR/V'] <= 0)]

    df2_filtered_HOR = df2_filtered_HOR.copy()
    df2_filtered_HER = df2_filtered_HER.copy()

    df2_filtered_HOR.loc[:, 'E-iR-eta/V'] = df2_filtered_HOR['E-iR/V'] + (((8.31446 * Temp) / (2 * 96485)) * (np.log(1 - (df2_filtered_HOR['Current/A'] / i_limiting_h))))
    df2_filtered_HER.loc[:, 'E-iR-eta/V'] = df2_filtered_HER['E-iR/V']

    df2_filtered_HER = df2_filtered_HER.copy()

    df2_filtered_HER.loc[:, 'Current_kin/A'] = df2_filtered_HER['Current/A']

    df2_filtered_HOR_iR = df2_filtered_HOR[(df2_filtered_HOR['E-iR/V'] <= 0.01)]
    df2_filtered_HOR_eta = df2_filtered_HOR[(df2_filtered_HOR['E-iR-eta/V'] <= 0.01)]

    df2_filtered_HOR_iR = df2_filtered_HOR_iR.copy()
    df2_filtered_HOR_eta = df2_filtered_HOR_eta.copy()

    df2_filtered_HOR_iR.loc[:, 'Current_kin/A'] = (i_limiting_h * df2_filtered_HOR_iR['Current/A']) / (i_limiting_h - df2_filtered_HOR_iR['Current/A'])
    df2_filtered_HOR_eta.loc[:, 'Current_kin/A'] = (i_limiting_h * df2_filtered_HOR_eta['Current/A']) / (i_limiting_h - df2_filtered_HOR_eta['Current/A'])


    df2_filtered = pd.concat([df2_filtered_HER, df2_filtered_HOR_iR], ignore_index=True)
    df2_filtered_eta = pd.concat([df2_filtered_HER, df2_filtered_HOR_eta], ignore_index=True)

    df2_filtered = df2_filtered.drop(columns=['level_0', 'index'])
    df2_filtered_eta = df2_filtered_eta.drop(columns=['level_0', 'index'])



    df1_red['E-iR-eta/V'] = df1_red['E-iR/V'] - ((-8.314 * Temp) / (2 * 96485)) * (np.log(1 - (df1_red['Current/A'] / i_limiting_h)))

    df2_red['E-iR-eta/V'] = df2_red['E-iR/V'] - ((-8.314 * Temp) / (2 * 96485)) * (
        np.log(1 - (df2_red['Current/A'] / i_limiting_h)))

    df1_filtered = df1_red[(df1_red['E-iR/V'] >= -0.01) & (df1_red['E-iR/V'] <= 0.01)]
    df1_filtered_eta = df1_red[(df1_red['E-iR-eta/V'] >= -0.01) & (df1_red['E-iR-eta/V'] <= 0.01)]

    linear_df1 = np.polyfit(df1_filtered['E-iR/V'], df1_filtered['Current/A'], 1)
    linear_df1_eta = np.polyfit(df1_filtered_eta['E-iR-eta/V'], df1_filtered_eta['Current/A'], 1)

    #df2_filtered = df2_red[(df2_red['E-iR/V'] >= -0.01) & (df2_red['E-iR/V'] <= 0.01)]
    #df2_filtered_eta = df2_red[(df2_red['E-iR-eta/V'] >= -0.01) & (df2_red['E-iR-eta/V'] <= 0.01)]

    #df2_filtered_eta.plot(x='E-iR-eta/V', y='Current_kin/A', kind='line', marker='o')


    linear_df2 = np.polyfit(df2_filtered['E-iR/V'], df2_filtered['Current_kin/A'], 1)
    linear_df2_eta = np.polyfit(df2_filtered_eta['E-iR-eta/V'], df2_filtered_eta['Current_kin/A'], 1)

    #df2_filtered_eta['Current_kin_linear/A'] = linear_df2_eta[0] * df2_filtered_eta['E-iR-eta/V'] + linear_df2_eta[1]

    #df2_filtered_eta.plot(x='E-iR-eta/V', y='Current_kin_linear/A', kind='line', marker='o')

    #plt.show()

    global df2_f
    global df2_f_eta
    df2_f = df2_filtered.copy()
    df2_f_eta = df2_filtered_eta.copy()

    #plt.show()

    global i_0_k_1
    global i_0_k_eta_1
    global i_0_k_2
    global i_0_k_eta_1

    i_0_k_1 = ((8.31446 * Temp) / 96485) * linear_df1[0]
    i_0_k_eta_1 = ((8.31446 * Temp) / 96485) * linear_df1_eta[0]
    i_0_k_2 = ((8.31446 * Temp) / 96485) * linear_df2[0]
    i_0_k_eta_2 = ((8.31446 * Temp) / 96485) * linear_df2_eta[0]

    global i_0_s_1
    global i_0_s_eta_1
    global i_0_s_2
    global i_0_s_eta_2

    if 'co_area' in globals():
        i_0_s_1 = i_0_k_1 / co_area * 1000000
        i_0_s_eta_1 = i_0_k_eta_1 / co_area * 1000000
        i_0_s_2 = i_0_k_2 / co_area * 1000000
        i_0_s_eta_2 = i_0_k_eta_2 / co_area * 1000000

    if 'co_area' not in globals() and 'area' in globals():
        i_0_s_1 = i_0_k_1 / area * 1000000
        i_0_s_eta_1 = i_0_k_eta_1 / area * 1000000
        i_0_s_2 = i_0_k_2 / area * 1000000
        i_0_s_eta_2 = i_0_k_eta_2 / area * 1000000

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
        global i_0_m_1
        global i_0_m_eta_1
        global i_0_m_2
        global i_0_m_eta_2

        i_0_m_1 = i_0_k_1 / loading
        i_0_m_eta_1 = i_0_k_eta_1 / loading
        i_0_m_2 = i_0_k_2 / loading
        i_0_m_eta_2 = i_0_k_eta_2 / loading

    ax_hor = hor_f.add_subplot(1, 1, 1)
    ax_hor.set_ylabel("Current [A]")
    ax_hor.set_xlabel("Potential [V]")
    ax_hor.set_facecolor(bgcolor)
    ax_hor.xaxis.label.set_color(fgcolor)
    ax_hor.yaxis.label.set_color(fgcolor)
    ax_hor.tick_params(axis='x', colors=fgcolor)
    ax_hor.tick_params(axis='y', colors=fgcolor)
    ax_hor.spines['left'].set_color(fgcolor)
    ax_hor.spines['top'].set_color(fgcolor)
    ax_hor.spines['right'].set_color(fgcolor)
    ax_hor.spines['bottom'].set_color(fgcolor)
    ax_hor.plot(df1['E-iR/V'], df1['Current/A'], label='anodic HOR')
    ax_hor.plot(df2['E-iR/V'], df2['Current/A'], label='cathodic HOR')
    ax_hor.axhline(y=0, color='0.4', xmin=df1['E-iR/V'].nsmallest(1), xmax=df1['E-iR/V'].nlargest(1),
                   linestyle='dashed')
    diff_lim_plt = ax_hor.plot(df_diff['etadiff/V'], df_diff['Current/A'], label='DiffusionLimitation')
    legend = ax_hor.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)


    def dragged():
        lower_potential = Tline.getvalue()
        upper_potential = Tline2.getvalue()

        index_low = df2.iloc[(df2['E-iR/V'] - lower_potential).abs().argsort()[:1]].index[0]
        index_high = df2.iloc[(df2['E-iR/V'] - upper_potential).abs().argsort()[:1]].index[0]

        index_low_1 = df1.iloc[(df1['E-iR/V'] - lower_potential).abs().argsort()[:1]].index[0]
        index_high_1 = df1.iloc[(df1['E-iR/V'] - upper_potential).abs().argsort()[:1]].index[0]

        global i_limiting_h
        i_limiting_h = df2['Current/A'].loc[index_low:index_high].mean()

        global i_limiting_h_1
        i_limiting_h_1 = df1['Current/A'].loc[index_low_1:index_high_1].mean()

        upper_limit = 0.95 * i_limiting_h
        upper_limit_1 = 0.95 * i_limiting_h_1

        max_lim = df2[(df2['Current/A'] >= upper_limit) & (df2['Current/A'] <= i_limiting_h)].iloc[0].name
        max_lim_1 = df1[(df1['Current/A'] >= upper_limit_1) & (df1['Current/A'] <= i_limiting_h_1)].iloc[0].name

        #df_diff = df2.iloc[0:max_lim].reset_index()
        #del df_diff['index']

        #df_diff['etadiff/V'] = ((-8.314 * Temp) / (2 * 96485)) * (np.log(1 - (df_diff['Current/A'] / i_limiting_h)))

        df1_red = df1.iloc[0:max_lim_1].reset_index()
        df2_red = df2.iloc[0:max_lim].reset_index()

        df2_filtered_HOR = df2_red[(df2_red['E-iR/V'] >= 0)]
        df2_filtered_HER = df2_red[(df2_red['E-iR/V'] >= -0.01) & (df2_red['E-iR/V'] <= 0)]

        df2_filtered_HOR = df2_filtered_HOR.copy()
        df2_filtered_HER = df2_filtered_HER.copy()

        df2_filtered_HOR.loc[:, 'E-iR-eta/V'] = df2_filtered_HOR['E-iR/V'] + (
                    ((8.31446 * Temp) / (2 * 96485)) * (np.log(1 - (df2_filtered_HOR['Current/A'] / i_limiting_h))))
        df2_filtered_HER.loc[:, 'E-iR-eta/V'] = df2_filtered_HER['E-iR/V']

        df2_filtered_HER = df2_filtered_HER.copy()

        df2_filtered_HER.loc[:, 'Current_kin/A'] = df2_filtered_HER['Current/A']

        df2_filtered_HOR_iR = df2_filtered_HOR[(df2_filtered_HOR['E-iR/V'] <= 0.01)]
        df2_filtered_HOR_eta = df2_filtered_HOR[(df2_filtered_HOR['E-iR-eta/V'] <= 0.01)]

        df2_filtered_HOR_iR = df2_filtered_HOR_iR.copy()
        df2_filtered_HOR_eta = df2_filtered_HOR_eta.copy()

        df2_filtered_HOR_iR.loc[:, 'Current_kin/A'] = (i_limiting_h * df2_filtered_HOR_iR['Current/A']) / (
                    i_limiting_h - df2_filtered_HOR_iR['Current/A'])
        df2_filtered_HOR_eta.loc[:, 'Current_kin/A'] = (i_limiting_h * df2_filtered_HOR_eta['Current/A']) / (
                    i_limiting_h - df2_filtered_HOR_eta['Current/A'])

        df2_filtered = pd.concat([df2_filtered_HER, df2_filtered_HOR_iR], ignore_index=True)
        df2_filtered_eta = pd.concat([df2_filtered_HER, df2_filtered_HOR_eta], ignore_index=True)

        df2_filtered = df2_filtered.drop(columns=['level_0', 'index'])
        df2_filtered_eta = df2_filtered_eta.drop(columns=['level_0', 'index'])


        df1_red['E-iR-eta/V'] = df1_red['E-iR/V'] - ((-8.314 * Temp) / (2 * 96485)) * (
            np.log(1 - (df1_red['Current/A'] / i_limiting_h_1)))

        df2_red['E-iR-eta/V'] = df2_red['E-iR/V'] - ((-8.314 * Temp) / (2 * 96485)) * (
            np.log(1 - (df2_red['Current/A'] / i_limiting_h)))

        df1_filtered = df1_red[(df1_red['E-iR/V'] >= -0.01) & (df1_red['E-iR/V'] <= 0.01)]
        df1_filtered_eta = df1_red[(df1_red['E-iR-eta/V'] >= -0.01) & (df1_red['E-iR-eta/V'] <= 0.01)]

        linear_df1 = np.polyfit(df1_filtered['E-iR/V'], df1_filtered['Current/A'], 1)

        linear_df1_eta = np.polyfit(df1_filtered_eta['E-iR-eta/V'], df1_filtered_eta['Current/A'], 1)

        #df2_filtered = df2_red[(df2_red['E-iR/V'] >= -0.01) & (df2_red['E-iR/V'] <= 0.01)]
        #df2_filtered_eta = df2_red[(df2_red['E-iR-eta/V'] >= -0.01) & (df2_red['E-iR-eta/V'] <= 0.01)]

        linear_df2 = np.polyfit(df2_filtered['E-iR/V'], df2_filtered['Current_kin/A'], 1)
        linear_df2_eta = np.polyfit(df2_filtered_eta['E-iR-eta/V'], df2_filtered_eta['Current_kin/A'], 1)

        global df2_f
        global df2_f_eta
        df2_f = df2_filtered.copy()
        df2_f_eta = df2_filtered_eta.copy()

        global i_0_k_1
        global i_0_k_eta_1
        global i_0_k_2
        global i_0_k_eta_1

        i_0_k_1 = ((8.31446 * Temp) / 96485) * linear_df1[0]
        i_0_k_eta_1 = ((8.31446 * Temp) / 96485) * linear_df1_eta[0]
        i_0_k_2 = ((8.31446 * Temp) / 96485) * linear_df2[0]
        i_0_k_eta_2 = ((8.31446 * Temp) / 96485) * linear_df2_eta[0]

        global i_0_s_1
        global i_0_s_eta_1
        global i_0_s_2
        global i_0_s_eta_2

        if 'co_area' in globals():

            i_0_s_1 = i_0_k_1 / co_area * 1000000
            i_0_s_eta_1 = i_0_k_eta_1 / co_area * 1000000
            i_0_s_2 = i_0_k_2 / co_area * 1000000
            i_0_s_eta_2 = i_0_k_eta_2 / co_area * 1000000

            is_label.configure(text='{0:.3f}'.format(i_0_s_2))
            is_label_ex.configure(text='{0:.3f}'.format(i_0_s_eta_2))


        elif 'co_area' not in globals() and 'area' in globals():

            i_0_s_1 = i_0_k_1 / area * 1000000
            i_0_s_eta_1 = i_0_k_eta_1 / area * 1000000
            i_0_s_2 = i_0_k_2 / area * 1000000
            i_0_s_eta_2 = i_0_k_eta_2 / area * 1000000

            is_label.configure(text='{0:.3f}'.format(i_0_s_2))
            is_label_ex.configure(text='{0:.3f}'.format(i_0_s_eta_2))


        else:
            is_label.configure(text='n.a.')
            is_label_ex.configure(text='n.a.')

        if LoadingEntry.get() != '':
            global loading
            loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))
            global i_0_m_1
            global i_0_m_eta_1
            global i_0_m_2
            global i_0_m_eta_2

            i_0_m_1 = i_0_k_1 / loading
            i_0_m_eta_1 = i_0_k_eta_1 / loading
            i_0_m_2 = i_0_k_2 / loading
            i_0_m_eta_2 = i_0_k_eta_2 / loading

            im_label.configure(text='{0:.3f}'.format(i_0_m_2))
            im_label_ex.configure(text='{0:.3f}'.format(i_0_m_eta_2))


        else:
            im_label.configure(text='n.a.')
            im_label_ex.configure(text='n.a.')

        '''
        
        for line in diff_lim_plt:
            if line.get_label() == 'DiffusionLimitaion':
                line_update = line

                line_update.set_data(df_diff['etadiff/V'], df_diff['Current/A'])
                line_update.set_label('DiffusionLimitation')
                ax_hor.draw()
        '''

    class draggable_line_h:
        def __init__(self, canvas, ax, kind, XorY):
            self.ax = ax
            self.c = canvas
            self.o = kind
            self.XorY = XorY

            if kind == "h":
                x = [-1, 1]
                y = [XorY, XorY]

            elif kind == "v":
                x = [XorY, XorY]
                y = [min_current, max_current]
            self.line = lines.Line2D(x, y, picker=5, color=fgcolor, linestyle='dashed', linewidth=0.5)
            self.ax.add_line(self.line)
            self.c.draw_idle()
            self.c.mpl_connect('pick_event', self.clickonline)

        def clickonline(self, event):
            if event.artist == self.line:
                # print("line selected ", event.artist)
                self.follower = self.c.mpl_connect("motion_notify_event", self.followmouse)
                self.releaser = self.c.mpl_connect("button_press_event", self.releaseonclick)

        def followmouse(self, event):
            if self.o == "h":
                self.line.set_ydata([event.ydata, event.ydata])
            else:
                self.line.set_xdata([event.xdata, event.xdata])
            self.c.draw_idle()

        def releaseonclick(self, event):
            if self.o == "h":
                self.XorY = self.line.get_ydata()[0]
            else:
                self.XorY = self.line.get_xdata()[0]

            # print(self.XorY)
            dragged()
            self.c.mpl_disconnect(self.releaser)
            self.c.mpl_disconnect(self.follower)

        def getvalue(self):
            return self.XorY

    Tline = draggable_line_h(canvas, ax_hor, "v", 0.3)
    Tline2 = draggable_line_h(canvas, ax_hor, "v", 0.5)

    canvas.draw_idle()

    hor_variable_frame = ct.CTkFrame(master=hor_info_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
    hor_variable_frame.grid(row=1, column=1, sticky='nswe', pady=10, padx=10)
    hor_variable_frame.grid_columnconfigure(0, weight=1, minsize=300)
    hor_variable_frame.grid_rowconfigure(0, weight=1)
    hor_variable_frame.grid_rowconfigure(1, weight=1)
    hor_variable_frame.grid_rowconfigure(2, weight=1)

    is_frame = ct.CTkFrame(master=hor_variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    is_frame.grid(row=1, column=0, sticky='nswe', pady=0, padx=5)
    is_frame.grid_rowconfigure(0, weight=0)
    is_frame.grid_rowconfigure(1, weight=1)
    is_frame.grid_rowconfigure(2, weight=0)
    is_frame.grid_rowconfigure(3, weight=1)
    is_frame.grid_rowconfigure(4, weight=0)
    is_frame.grid_columnconfigure(0, weight=0, minsize=80)
    is_frame.grid_columnconfigure(1, weight=1, minsize=115)
    is_frame.grid_columnconfigure(2, weight=0, minsize=90)
    if any(var in globals() for var in ['co_area', 'area']):
        is_label = ct.CTkLabel(is_frame, text='{0:.3f}'.format(i_0_s_2), font=("Calibri", -20), width=1)
        is_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        is_label_ex = ct.CTkLabel(is_frame, text='{0:.3f}'.format(i_0_s_eta_2), font=("Calibri", -20), width=1)
        is_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    else:
        is_label = ct.CTkLabel(is_frame, text='n.a.', font=("Calibri", -20), width=1)
        is_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        is_label_ex = ct.CTkLabel(is_frame, text='n.a.', font=("Calibri", -20), width=1)
        is_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(is_frame, text='iₛ:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='iₛ eta:', font=("Calibri", -20), width=1).grid(row=3, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2, sticky=tk.E, padx=2)

    im_frame = ct.CTkFrame(master=hor_variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    im_frame.grid(row=2, column=0, sticky='nswe', pady=5, padx=5)
    im_frame.grid_rowconfigure(0, weight=0)
    im_frame.grid_rowconfigure(1, weight=1)
    im_frame.grid_rowconfigure(2, weight=0)
    im_frame.grid_rowconfigure(3, weight=1)
    im_frame.grid_rowconfigure(4, weight=0)
    im_frame.grid_columnconfigure(0, weight=0, minsize=80)
    im_frame.grid_columnconfigure(1, weight=1, minsize=115)
    im_frame.grid_columnconfigure(2, weight=0, minsize=90)
    if LoadingEntry.get() != '':
        im_label = ct.CTkLabel(im_frame, text='{0:.3f}'.format(i_0_m_2), font=("Calibri", -20), width=1)
        im_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        im_label_ex = ct.CTkLabel(im_frame, text='{0:.3f}'.format(i_0_m_eta_2), font=("Calibri", -20), width=1)
        im_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    else:
        im_label = ct.CTkLabel(im_frame, text='n.a.', font=("Calibri", -20), width=1)
        im_label.grid(row=1, column=1, sticky=tk.E, padx=0)
        im_label_ex = ct.CTkLabel(im_frame, text='n.a.', font=("Calibri", -20), width=1)
        im_label_ex.grid(row=3, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(im_frame, text='iₘ:', font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='iₘ eta:', font=("Calibri", -20), width=1).grid(row=3, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2, sticky=tk.E, padx=2)

    def exit1(df1, df2, df2_f, df2_f_eta):
        window.destroy()
        global z
        a = z
        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=160)
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=125)
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=20)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='HOR Scan - ', font=("Calibri", -20), width=140).grid(row=0, column=0,
                                                                                                       sticky=tk.W,
                                                                                                       padx=2, pady=5)

        d['v_n_{0}'.format(z)] = ct.CTkEntry(d['v_f_{0}'.format(z)], width=125, border_width=0,
                                             bg_color=("grey70", 'grey30'), fg_color=("grey70", 'grey30'),
                                             font=("Calibri", -19), text_color=('black', 'white'))
        d['v_n_{0}'.format(z)].insert(0, NameEntry.get())
        d['v_n_{0}'.format(z)].configure(state='disabled')
        d['v_n_{0}'.format(z)].grid(row=0, column=1, sticky='ws', pady=5)

        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x', width=8, height=8, command=lambda: remove(a),
                     font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=2, sticky=tk.E, pady=5,
                                                                                  padx=5)
        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                              fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2, columnspan=3)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(4, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if any(var in globals() for var in ['co_area', 'area']):
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(i_0_s_2),
                                                  font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(i_0_s_eta_2),
                                                  font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        else:
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='iₛ:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                              sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                   sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='iₛ eta:', font=("Calibri", -20), width=1).grid(row=3, column=0,
                                                                                                  sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='µA/cm²ₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2,
                                                                                                   sticky=tk.E, padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10,
                                               fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2, columnspan=3)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(i_0_m_2),
                                                   font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(i_0_m_eta_2),
                                                   font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20),
                                                   width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', font=("Calibri", -20),
                                                   width=1)
            d['a_n_l_{0}'.format(z)].grid(row=3, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='iₘ:', font=("Calibri", -20), width=1).grid(row=1, column=0,
                                                                                               sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=1, column=2,
                                                                                                 sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='iₘ eta:', font=("Calibri", -20), width=1).grid(row=3, column=0,
                                                                                                   sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='A/gₚₜ', font=("Calibri", -20), width=1).grid(row=3, column=2,
                                                                                                 sticky=tk.E, padx=2)
        data_canvas.update_idletasks()
        data_canvas.configure(scrollregion=data_frame.bbox())

        df1.rename(columns={'E-iR/V': 'E-iR/V_' + 'HOR_an_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df2.rename(columns={'E-iR/V': 'E-iR/V_' + 'HOR_ca_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df1.rename(columns={'Current/A': 'Current_anodic/A_' + str(z)}, inplace=True)
        df2.rename(columns={'Current/A': 'Current_cathodic/A_' + str(z)}, inplace=True)
        df2.drop('index', axis=1, inplace=True)

        df2_f.drop('E-iR-eta/V', axis=1, inplace=True)
        #df2_f.drop('level_0', axis=1, inplace=True)
        #df2_f.drop('index', axis=1, inplace=True)
        df2_f['Current_linear/A_' + str(z)] = linear_df2[0] * df2_f['E-iR/V'] + linear_df2[1]
        df2_f.rename(columns={'E-iR/V': 'E-iR(lim)_ca/V_' + 'HOR_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df2_f.rename(columns={'Current/A': 'Current_cathodic(lim)/A_' + str(z)}, inplace=True)
        df2_f.rename(columns={'Current_kin/A': 'Current_cathodic_kin(lim)/A_' + str(z)}, inplace=True)

        df2_f_eta['Current_linear_eta/A_' + str(z)] = linear_df2_eta[0] * df2_f_eta['E-iR-eta/V'] + linear_df2_eta[1]
        df2_f_eta.drop('E-iR/V', axis=1, inplace=True)
        #df2_f_eta.drop('level_0', axis=1, inplace=True)
        #df2_f_eta.drop('index', axis=1, inplace=True)
        df_pop = df2_f_eta.pop('E-iR-eta/V')
        df2_f_eta.insert(0, 'E-iR-eta/V', df_pop)
        df2_f_eta.rename(columns={'E-iR-eta/V': 'E-iR-eta(lim)/V_' + 'HOR_' + NameEntry.get() + '_' + str(z)},
                         inplace=True)
        df2_f_eta.rename(columns={'Current/A': 'Current_cathodic(lim)_eta/A_' + str(z)}, inplace=True)
        df2_f_eta.rename(columns={'Current_kin/A': 'Current_cathodic_kin(lim)_eta/A_' + str(z)}, inplace=True)

        global savefile
        savefile = pd.concat([savefile, df1], axis=1)
        savefile = pd.concat([savefile, df2], axis=1)
        savefile = pd.concat([savefile, df2_f], axis=1)
        savefile = pd.concat([savefile, df2_f_eta], axis=1)

        # linear coefficients

        slope_cat = linear_df2[0]
        slope_cat_eta = linear_df2_eta[0]
        y_inter = linear_df2[1]
        y_inter_eta = linear_df2_eta[1]

        if LoadingEntry.get() != '':
            i_0_m = i_0_m_2
            i_0_m_eta = i_0_m_eta_2
        else:
            i_0_m = 'n.a.'
            i_0_m_eta = 'n.a.'

        if 'co_area' in globals():
            i_0_s = i_0_s_2
            i_0_s_eta = i_0_s_eta_2
        elif 'co_area' not in globals() and 'area' in globals():
            i_0_s = i_0_s_2
            i_0_s_eta = i_0_s_eta_2

        else:
            i_0_s = 'n.a.'
            i_0_s_eta = 'n.a.'

        result = pd.DataFrame({'HOR_cathodic_i_0_k_A_' + NameEntry.get() + '_' + str(z): [i_0_k_2],
                               'HOR_cathodic_i_0_k_eta_A_' + str(z): [i_0_k_eta_2],
                               'HOR_cathodic_i_0_s_µA_cm^2geo_' + str(z): [i_0_s],
                               'HOR_cathodic_i_0_s_eta_µA_cm^2geo_' + str(z): [i_0_s_eta],
                               'HOR_cathodic_i_0_m_A_gPt' + str(z): [i_0_m],
                               'HOR_cathodic_i_0_m_eta_A_gPt' + str(z): [i_0_m_eta],
                               'HOR_cathodic_slope_' + str(z): [slope_cat],
                               'HOR_cathodic_slope_eta_' + str(z): [slope_cat_eta],
                               'HOR_cathodic_y_inter_' + str(z): [y_inter],
                               'HOR_cathodic_y_inter_eta_' + str(z): [y_inter_eta]})
        global results
        results = pd.concat([results, result], axis=1)

        save_enable()

        z += 1

    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=lambda: exit1(df1, df2, df2_f, df2_f_eta),
                 font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    window.mainloop()


if __name__ == '__main__':
    root = ct.CTk()
    root.title('RDE Evaluation')

    root.iconbitmap('iconRDE.ico')

    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    widthfactor = 1920 / 1920
    heightfactor = 1080 / 1080
    root.geometry(str(int(width - (widthfactor * 20))) + 'x' + str(int(height - (heightfactor * 90))) + '+0+10')
    root.configure(bg='grey90')
    root.resizable(False, False)

    root.grid_columnconfigure(0, weight=3, minsize=int(widthfactor * (width * 0.753) - 25))
    root.grid_columnconfigure(1, weight=1, minsize=int(widthfactor * (width * (1 - 0.753)) - 25))
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

    d = {}
    global z
    z = 0
    global savefile
    global results
    savefile = np.linspace(0, 1000, 1001)
    savefile = pd.DataFrame(savefile, columns=['ignore'])
    results = pd.DataFrame({'ignore': [1]})

    # open importfilter
    config = open('Importconfig.txt')
    config_txt = config.readlines()
    config.close()

    global Ar_config
    global CO_config
    global ORR_config
    global ORRa_config

    Ar_config = config_txt[2].replace('\n', '').split()
    CO_config = config_txt[4].replace('\n', '').split()
    ORR_config = config_txt[6].replace('\n', '').split()
    ORRa_config = config_txt[8].replace('\n', '').split()
    HOR_config = config_txt[10].replace('\n', '').split()

    # open Savpath:
    pathfile = open('Pathfile.txt')
    path_txt = pathfile.readlines()
    pathfile.close()

    global path
    path = path_txt[1].replace('\n', '')

    # layout of frames for the main window
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

    graph_frame = ct.CTkFrame(master=root, corner_radius=10, fg_color=('grey80', 'grey20'))
    graph_frame.grid(row=1, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)

    data_over_frame = ct.CTkFrame(master=root, corner_radius=10, fg_color=('grey80', 'grey20'))
    data_over_frame.grid(row=0, column=1, rowspan=2, sticky='nswe', pady=10, padx=10)
    data_over_frame.grid_columnconfigure(0, weight=0, minsize=10)
    data_over_frame.grid_columnconfigure(1, weight=1)
    data_over_frame.grid_columnconfigure(2, weight=0)
    data_over_frame.grid_columnconfigure(3, weight=0, minsize=5)
    data_over_frame.grid_rowconfigure(0, weight=0, minsize=10)
    data_over_frame.grid_rowconfigure(1, weight=1)
    data_over_frame.grid_rowconfigure(2, weight=0, minsize=10)

    data_canvas = ct.CTkCanvas(master=data_over_frame, bg=fg_color, highlightthickness=0)
    data_canvas.grid(row=1, column=1, sticky='nswe')
    data_canvas.grid_columnconfigure(0, weight=1)
    data_canvas.grid_columnconfigure(1, weight=0, minsize=5)

    yscrollbar = tk.Scrollbar(data_over_frame, orient='vertical')
    yscrollbar.grid(row=1, column=2, sticky='nse')

    data_canvas.configure(yscrollcommand=yscrollbar.set)
    yscrollbar.configure(command=data_canvas.yview)

    data_frame = ct.CTkFrame(master=data_canvas, fg_color=fg_color, bg_color=fg_color)
    data_frame.grid(row=0, column=0, sticky='nswe')
    data_frame.grid_rowconfigure(0, weight=0, minsize=0)
    data_frame.grid_columnconfigure(0, weight=0, minsize=0)
    data_frame.grid_columnconfigure(1, weight=1)

    data_canvas.create_window((0, 0), window=data_frame, anchor='nw')

    bottom_frame = ct.CTkFrame(master=root, corner_radius=10, fg_color=('grey80', 'grey20'))
    bottom_frame.grid(row=2, column=0, columnspan=2, sticky='nswe', padx=10, ipadx=10, ipady=10)
    bottom_frame.grid_rowconfigure(0, weight=0)
    bottom_frame.grid_rowconfigure(1, weight=1)
    bottom_frame.grid_rowconfigure(2, weight=0)
    bottom_frame.grid_columnconfigure(1, weight=1)


    def remove(value):
        for widgets in d['v_f_{0}'.format(value)].winfo_children():
            widgets.destroy()
        d['v_f_{0}'.format(value)].grid_forget()
        d['v_f_{0}'.format(value)].destroy()
        data_frame.grid_rowconfigure(value * 2 + 2, minsize=0)
        global savefile
        savefile.drop(list(savefile.filter(regex='_' + str(value))), axis=1, inplace=True)
        global results
        results.drop(list(results.filter(regex='_' + str(value))), axis=1, inplace=True)
        save_enable()


    # input frame
    NameLabel = ct.CTkLabel(master=input_frame, text='Name:', font=("Calibri", -18))
    NameLabel.grid(row=1, column=1, sticky=tk.W)
    NameEntry = ct.CTkEntry(master=input_frame, width=200, font=("Calibri", -14))
    NameEntry.grid(row=1, column=2, sticky=tk.W, columnspan=2)

    LoadingLabel = ct.CTkLabel(master=input_frame, text='Loading [µg/cm²]:', font=("Calibri", -18))
    LoadingLabel.grid(row=3, column=1, sticky=tk.W)
    LoadingEntry = ct.CTkEntry(master=input_frame, width=200, font=("Calibri", -14))
    LoadingEntry.grid(row=3, column=2, sticky=tk.W, columnspan=2)

    RLabel = ct.CTkLabel(master=input_frame, text=u'HFR [\u03A9]:', font=("Calibri", -18))
    RLabel.grid(row=5, column=1, sticky=tk.W)
    REntry = ct.CTkEntry(master=input_frame, width=150, font=("Calibri", -14))
    REntry.grid(row=5, column=2, sticky=tk.W)


    def HFR():
        global path
        file = filedialog.askopenfilename(title='Open HFR file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'
            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()

            HFR = scan.HFRscan(file, sepvalue='\t', headervalue=None, decimalvalue='.', skip=1, R=3, u_R=1)

            REntry.delete(0, 'end')
            REntry.insert(0, HFR)


    ct.CTkButton(master=input_frame, text='HFR', command=HFR, font=("Calibri", -16), width=40, height=20).grid(row=5,
                                                                                                               column=3,
                                                                                                               sticky=tk.W,
                                                                                                               padx=5)

    RefLabel = ct.CTkLabel(master=input_frame, text='Ref [V]:', font=("Calibri", -18))
    RefLabel.grid(row=7, column=1, sticky=tk.W)
    RefEntry = ct.CTkEntry(master=input_frame, width=150, font=("Calibri", -14))
    RefEntry.grid(row=7, column=2, sticky=tk.W)


    def Reference():
        global path
        file = filedialog.askopenfilename(title='Open HOR H2 file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'
            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()

            Ref_cathodic, Ref_anodic = scan.multiplescan(file, 2, sepvalue='\t', headervalue=0, decimalvalue='.',
                                                         skip=0, pot=2, u_V=1, cur=3, u_A=1)

            pot_cat = Ref_cathodic['Potential/V'].iloc[abs(Ref_cathodic['Current/A']).nsmallest(1).index[0]]
            pot_an = Ref_anodic['Potential/V'].iloc[abs(Ref_anodic['Current/A']).nsmallest(1).index[0]]

            global Ref
            Ref = (pot_cat + pot_an) / 2

            RefEntry.delete(0, 'end')
            RefEntry.insert(0, Ref)


    ct.CTkButton(master=input_frame, text='Ref', command=Reference, font=("Calibri", -16), width=40, height=20).grid(row=7,
                                                                                                               column=3,
                                                                                                               sticky=tk.W,
                                                                                                               padx=5)

    RadiusLabel = ct.CTkLabel(master=input_frame, text='Radius [cm]:', font=("Calibri", -18))
    RadiusLabel.grid(row=9, column=1, sticky=tk.W)
    RadiusEntry = ct.CTkEntry(master=input_frame, width=200, font=("Calibri", -14))
    RadiusEntry.grid(row=9, column=2, sticky=tk.W, columnspan=2)
    RadiusEntry.insert(0, '0.25')

    HUPDLabel = ct.CTkLabel(master=input_frame, text='Ar CV:', font=("Calibri", -18))
    HUPDLabel.grid(row=1, column=4, sticky=tk.W)
    HUPDEntry = ct.CTkEntry(master=input_frame, width=400, font=("Calibri", -14))
    HUPDEntry.grid(row=1, column=5, sticky=tk.W)


    def HUPD():
        global path
        file = filedialog.askopenfilename(title='Open HUPD file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            HUPDEntry.delete(0, 'end')
            HUPDEntry.insert(0, file)
            HUPDEval.configure(state=tk.NORMAL)

            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'
            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()


    ct.CTkButton(master=input_frame, text='Open', command=HUPD, font=("Calibri", -18), width=80).grid(row=1, column=6,
                                                                                                      sticky=tk.W,
                                                                                                      padx=20)


    def Ar_graph():
        Ar = HUPDEntry.get()

        if Ar_config[4] == 'None':
            Ar_header = None
        else:
            Ar_header = int(Ar_config[4])

        Ar_sep_dic = {';': ';', 'spaces': r'\s+', 'tabs': '\t'}
        Ar_unit_dic = {'V': 1, 'mV': 1000, 'µV': 1000000}
        Ar_unit_1_dic = {'A': 1, 'mA': 1000, 'µA': 1000000}
        Ar_dic = {'Single': scan.singlescan(Ar, sepvalue=Ar_sep_dic[Ar_config[3]], headervalue=Ar_header,
                                            decimalvalue=Ar_config[5], skip=int(Ar_config[6]), pot=int(Ar_config[7]),
                                            u_V=Ar_unit_dic[Ar_config[8]], cur=int(Ar_config[9]),
                                            u_A=Ar_unit_1_dic[Ar_config[10]]),
                  'Multiple': scan.multiplescan(Ar, int(Ar_config[2]), sepvalue=Ar_sep_dic[Ar_config[3]],
                                                headervalue=Ar_header, decimalvalue=Ar_config[5],
                                                skip=int(Ar_config[6]), pot=int(Ar_config[7]),
                                                u_V=Ar_unit_dic[Ar_config[8]], cur=int(Ar_config[9]),
                                                u_A=Ar_unit_1_dic[Ar_config[10]])}
        Ar_cathodic, Ar_anodic = Ar_dic[Ar_config[0]]

        Ar_Plot(Ar_anodic, Ar_cathodic)


    HUPDEval = ct.CTkButton(master=input_frame, text='Eval', command=Ar_graph, font=("Calibri", -18), width=80)
    HUPDEval.grid(row=1, column=7, sticky=tk.W, padx=20)
    HUPDEval.configure(state=tk.DISABLED)

    COStripLabel = ct.CTkLabel(master=input_frame, text='CO Strip:', font=("Calibri", -18))
    COStripLabel.grid(row=3, column=4, sticky=tk.W)
    COStripEntry = ct.CTkEntry(master=input_frame, width=400, font=("Calibri", -14))
    COStripEntry.grid(row=3, column=5, sticky=tk.W)


    # COStripEntry.insert(0, CO_Strip)

    def COStrip():
        global path
        file = filedialog.askopenfilename(title='Open COStrip file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file.strip():
            COStripEntry.delete(0, 'end')
            COStripEntry.insert(0, file)
            COStripEval.configure(state=tk.NORMAL)

            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'

            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()


    ct.CTkButton(master=input_frame, text='Open', command=COStrip, font=("Calibri", -18), width=80).grid(row=3,
                                                                                                         column=6,
                                                                                                         sticky=tk.W,
                                                                                                         padx=20)


    def CO_Strip_graph():
        CO_Strip = COStripEntry.get()
        if CO_config[1] == 'None':
            CO_header = None
        else:
            CO_header = int(CO_config[1])

        CO_sep_dic = {';': ';', 'spaces': r'\s+', 'tabs': '\t'}

        CO_cathodic_1, CO_anodic_1 = scan.multiplescan(CO_Strip, 1, sepvalue=CO_sep_dic[CO_config[0]],
                                                       headervalue=CO_header, decimalvalue=CO_config[2],
                                                       skip=int(CO_config[3]), pot=int(CO_config[4]),
                                                       cur=int(CO_config[5]))
        CO_cathodic_2, CO_anodic_2 = scan.multiplescan(CO_Strip, 2, sepvalue=CO_sep_dic[CO_config[0]],
                                                       headervalue=CO_header, decimalvalue=CO_config[2],
                                                       skip=int(CO_config[3]), pot=int(CO_config[4]),
                                                       cur=int(CO_config[5]))
        CO_plot(CO_anodic_1, CO_anodic_2)


    COStripEval = ct.CTkButton(master=input_frame, text='Eval', command=CO_Strip_graph, font=("Calibri", -18), width=80)
    COStripEval.grid(row=3, column=7, sticky=tk.W, padx=20)
    # COStripEval.configure(state=tk.DISABLED)

    ORRLabel = ct.CTkLabel(master=input_frame, text='ORR O2:', font=("Calibri", -18))
    ORRLabel.grid(row=5, column=4, sticky=tk.W)
    ORREntry = ct.CTkEntry(master=input_frame, width=400, font=("Calibri", -14))
    ORREntry.grid(row=5, column=5, sticky=tk.W)


    def ORR():
        global path
        file = filedialog.askopenfilename(title='Open ORR O2 file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file is not None:
            ORREntry.delete(0, 'end')
            ORREntry.insert(0, file)

            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'

            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()

            if ORRArEntry.get() != '':
                ORREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=ORR, font=("Calibri", -18), width=80).grid(row=5, column=6,
                                                                                                     sticky=tk.W,
                                                                                                     padx=20)

    ORRArLabel = ct.CTkLabel(master=input_frame, text='ORR Ar:', font=("Calibri", -18))
    ORRArLabel.grid(row=7, column=4, sticky=tk.W)
    ORRArEntry = ct.CTkEntry(master=input_frame, width=400, font=("Calibri", -14))
    ORRArEntry.grid(row=7, column=5, sticky=tk.W)


    def ORR_Ar():
        global path
        file = filedialog.askopenfilename(title='Open ORR Ar file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file is not None:
            ORRArEntry.delete(0, 'end')
            ORRArEntry.insert(0, file)

            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'

            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()

            if ORREntry.get() != '':
                ORREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=ORR_Ar, font=("Calibri", -18), width=80).grid(row=7, column=6,
                                                                                                        sticky=tk.W,
                                                                                                        padx=20)


    def ORR_graph():
        ORR = ORREntry.get()
        Ar_orr = ORRArEntry.get()
        global R
        R = None
        global Ref
        Ref = None
        if REntry.get() != '':
            R = REntry.get()
            REntry.configure(fg_color=('white', 'grey25'))
        else:
            REntry.configure(fg_color=('red'))
        if RefEntry.get() != '':
            Ref = RefEntry.get()
            RefEntry.configure(fg_color=('white', 'grey25'))
        else:
            RefEntry.configure(fg_color=('red'))
        if R is not None and Ref is not None:

            if ORR_config[4] == 'None':
                ORR_header = None
            else:
                ORR_header = int(ORR_config[4])

            if ORRa_config[4] == 'None':
                ORRa_header = None
            else:
                ORRa_header = int(ORRa_config[4])

            ORR_sep_dic = {';': ';', 'spaces': r'\s+', 'tabs': '\t'}

            ORR_dic = {'LSV': scan.lsvscan(ORR, sepvalue=ORR_sep_dic[ORR_config[3]], headervalue=ORR_header,
                                           decimalvalue=ORR_config[5], skip=int(ORR_config[6]), pot=int(ORR_config[7]),
                                           cur=int(ORR_config[8])),
                       'Single': scan.singlescan(ORR, sepvalue=ORR_sep_dic[ORR_config[3]], headervalue=ORR_header,
                                                 decimalvalue=ORR_config[5], skip=int(ORR_config[6]),
                                                 pot=int(ORR_config[7]), cur=int(ORR_config[8])),
                       'Multiple': scan.multiplescan(ORR, int(ORR_config[2]), sepvalue=ORR_sep_dic[ORR_config[3]],
                                                     headervalue=ORR_header, decimalvalue=ORR_config[5],
                                                     skip=int(ORR_config[6]), pot=int(ORR_config[7]),
                                                     cur=int(ORR_config[8]))}

            ORRa_dic = {'LSV': scan.lsvscan(Ar_orr, sepvalue=ORR_sep_dic[ORRa_config[3]], headervalue=ORRa_header,
                                            decimalvalue=ORRa_config[5], skip=int(ORRa_config[6]),
                                            pot=int(ORRa_config[7]), cur=int(ORRa_config[8])),
                        'Single': scan.singlescan(Ar_orr, sepvalue=ORR_sep_dic[ORRa_config[3]], headervalue=ORRa_header,
                                                  decimalvalue=ORRa_config[5], skip=int(ORRa_config[6]),
                                                  pot=int(ORRa_config[7]), cur=int(ORRa_config[8])),
                        'Multiple': scan.multiplescan(Ar_orr, int(ORRa_config[2]), sepvalue=ORR_sep_dic[ORRa_config[3]],
                                                      headervalue=ORRa_header, decimalvalue=ORRa_config[5],
                                                      skip=int(ORRa_config[6]), pot=int(ORRa_config[7]),
                                                      cur=int(ORRa_config[8]))}

            ORR_cathodic, ORR_anodic = ORR_dic[ORR_config[0]]
            ORRa_cathodic, ORRa_anodic = ORRa_dic[ORRa_config[0]]

            O2_plot(ORR_anodic, ORRa_anodic)


    ORREval = ct.CTkButton(master=input_frame, text='Eval', command=ORR_graph, font=("Calibri", -18), width=80)
    ORREval.grid(row=5, column=7, rowspan=3, sticky=tk.W, padx=20)
    ORREval.configure(state=tk.DISABLED)

    HORLabel = ct.CTkLabel(master=input_frame, text='HOR H2:', font=("Calibri", -18))
    HORLabel.grid(row=9, column=4, sticky=tk.W)
    HOREntry = ct.CTkEntry(master=input_frame, width=400, font=("Calibri", -14))
    HOREntry.grid(row=9, column=5, sticky=tk.W)


    def HOR():
        global path
        file = filedialog.askopenfilename(title='Open HOR H2 file', initialdir=path, filetypes=[('Textfile', '*.txt')])
        if file is not None:
            HOREntry.delete(0, 'end')
            HOREntry.insert(0, file)

            file_path = file.split('/')
            del file_path[-1]
            file_path = '/'.join(file_path) + '/'

            path = f'PathFile\n'f'{file_path}\n'

            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()

            # if HORArEntry.get() != '':
            HOREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=HOR, font=("Calibri", -18), width=80).grid(row=9, column=6,
                                                                                                     sticky=tk.W,
                                                                                                     padx=20)

    HORArLabel = ct.CTkLabel(master=input_frame, text='Folder:', font=("Calibri", -18))
    HORArLabel.grid(row=11, column=4, sticky=tk.W)
    HORArEntry = ct.CTkEntry(master=input_frame, width=400, font=("Calibri", -14))
    HORArEntry.grid(row=11, column=5, sticky=tk.W)


    def get_latest_file(pattern):
        files = glob.glob(pattern)
        if not files:
            return None
        latest_file = max(files, key=os.path.getmtime)
        return latest_file


    def find_measurement_files(folder_path):
        # Define patterns for each measurement type
        patterns = {
            "Ar_cv_slow": os.path.join(folder_path, "*CV-*0,01Vs-0rpm*cycles.txt"),
            "CO_strip": os.path.join(folder_path, "*-CO-Strip-*.txt"),
            "O2_measurement": os.path.join(folder_path, "*-O2-CV-*1600*.txt"),
            "H2_measurement": os.path.join(folder_path, "*-H2-CV-*1600*.txt"),
            "Impedance": os.path.join(folder_path, "*-Impedance.txt")
        }

        # Find the latest file for each pattern
        files = {}
        for key, pattern in patterns.items():
            files[key] = get_latest_file(pattern)

        return files

    def SelectFolder():
        global path
        file_path = filedialog.askdirectory(title='Open HOR Ar file', initialdir=path)
        if file_path is not None:
            HORArEntry.delete(0, 'end')
            HORArEntry.insert(0, file_path)

            file_path = os.path.dirname(file_path)

            path = f'PathFile\n'f'{file_path}\n'

            pathfile = open('Pathfile.txt', 'w')
            pathfile.write(path)
            pathfile.close()

            folder_path = HORArEntry.get()

            # Find and print the latest files based on the criteria
            latest_files = find_measurement_files(folder_path)

            HUPDEntry.delete(0, 'end')
            COStripEntry.delete(0, 'end')
            ORREntry.delete(0, 'end')
            ORRArEntry.delete(0, 'end')
            HOREntry.delete(0, 'end')
            RefEntry.delete(0, 'end')
            REntry.delete(0, 'end')

            if latest_files.get('Ar_cv_slow'):
                HUPDEntry.delete(0, 'end')
                HUPDEntry.insert(0, latest_files['Ar_cv_slow'].replace('\\', '/'))
                HUPDEval.configure(state=tk.NORMAL)
            if latest_files.get('CO_strip'):
                COStripEntry.delete(0, 'end')
                COStripEntry.insert(0, latest_files['CO_strip'].replace('\\', '/'))
                COStripEval.configure(state=tk.NORMAL)
            if latest_files.get('O2_measurement'):
                ORREntry.delete(0, 'end')
                ORREntry.insert(0, latest_files['O2_measurement'].replace('\\', '/'))
                ORREval.configure(state=tk.NORMAL)
            if latest_files.get('Ar_cv_slow'):
                ORRArEntry.delete(0, 'end')
                ORRArEntry.insert(0, latest_files['Ar_cv_slow'].replace('\\', '/'))
            if latest_files.get('H2_measurement'):
                HOREntry.delete(0, 'end')
                HOREntry.insert(0, latest_files['H2_measurement'].replace('\\', '/'))
                HOREval.configure(state=tk.NORMAL)

            if latest_files.get('H2_measurement'):
                Ref_cathodic, Ref_anodic = scan.multiplescan(latest_files['H2_measurement'].replace('\\', '/'), 2, sepvalue='\t', headervalue=0, decimalvalue='.',
                                                         skip=0, pot=2, u_V=1, cur=3, u_A=1)

                pot_cat = Ref_cathodic['Potential/V'].iloc[abs(Ref_cathodic['Current/A']).nsmallest(1).index[0]]
                pot_an = Ref_anodic['Potential/V'].iloc[abs(Ref_anodic['Current/A']).nsmallest(1).index[0]]

                global Ref
                Ref = (pot_cat + pot_an) / 2

                RefEntry.delete(0, 'end')
                RefEntry.insert(0, Ref)

            if latest_files.get('Impedance'):
                HFR = scan.HFRscan(latest_files['Impedance'].replace('\\', '/'), sepvalue='\t', headervalue=None, decimalvalue='.', skip=1, R=3, u_R=1)

                REntry.delete(0, 'end')
                REntry.insert(0, HFR)




    HORButton = ct.CTkButton(master=input_frame, text='Open', command=SelectFolder, font=("Calibri", -18), width=80)
    HORButton.grid(row=11, column=6, sticky=tk.W, padx=20)
    #HORButton.configure(state=tk.DISABLED)


    def HOR_graph():
        HOR = HOREntry.get()
        global R
        R = None
        global Ref
        Ref = None
        if REntry.get() != '':
            R = REntry.get()
            REntry.configure(fg_color=('white', 'grey25'))
        else:
            REntry.configure(fg_color=('red'))
        if RefEntry.get() != '':
            Ref = RefEntry.get()
            RefEntry.configure(fg_color=('white', 'grey25'))
        else:
            RefEntry.configure(fg_color=('red'))
        if R is not None and Ref is not None:

            if HOR_config[4] == 'None':
                HOR_header = None
            else:
                HOR_header = int(Ar_config[4])

            HOR_sep_dic = {';': ';', 'spaces': r'\s+', 'tabs': '\t'}
            HOR_unit_dic = {'V': 1, 'mV': 1000, 'µV': 1000000}
            HOR_unit_1_dic = {'A': 1, 'mA': 1000, 'µA': 1000000}
            HOR_dic = {'Single': scan.singlescan(HOR, sepvalue=HOR_sep_dic[Ar_config[3]], headervalue=HOR_header,
                                                 decimalvalue=HOR_config[5], skip=int(HOR_config[6]),
                                                 pot=int(HOR_config[7]), u_V=HOR_unit_dic[HOR_config[8]],
                                                 cur=int(HOR_config[9]), u_A=HOR_unit_1_dic[HOR_config[10]]),
                       'Multiple': scan.multiplescan(HOR, int(HOR_config[2]), sepvalue=HOR_sep_dic[Ar_config[3]],
                                                     headervalue=HOR_header, decimalvalue=HOR_config[5],
                                                     skip=int(HOR_config[6]), pot=int(HOR_config[7]),
                                                     u_V=HOR_unit_dic[HOR_config[8]], cur=int(HOR_config[9]),
                                                     u_A=HOR_unit_1_dic[HOR_config[10]])}
            HOR_cathodic, HOR_anodic = HOR_dic[HOR_config[0]]

            HOR_plot(HOR_anodic, HOR_cathodic)


    HOREval = ct.CTkButton(master=input_frame, text='Eval', command=HOR_graph, font=("Calibri", -18), width=80)
    HOREval.grid(row=9, column=7, sticky=tk.W, padx=20)
    HOREval.configure(state=tk.DISABLED)


    def save_enable():
        amount = len(list(data_frame.winfo_children()))
        if amount > 0:
            SaveButton.configure(state=tk.NORMAL)
        else:
            SaveButton.configure(state=tk.DISABLED)


    def save():
        global savefile
        global results
        global path

        file = filedialog.asksaveasfilename(title='Save As', initialdir=path, filetypes=[('Textfile', '*.txt')],
                                            initialfile=NameEntry.get())
        if file.strip():
            del savefile['ignore']

            if LoadingEntry.get() != '':
                global loading
                loading = float(LoadingEntry.get())*(np.pi * (float(RadiusEntry.get()) ** 2))*(10**(-6))

                result = pd.DataFrame({'loading_' + NameEntry.get(): [loading]})
                global results
                results = pd.concat([results, result], axis=1)

            del results['ignore']
            file1 = file + '.txt'
            file2 = file + '_results.txt'

            savefile.to_csv(file1, sep='\t', index=False, header=True)
            results.to_csv(file2, sep='\t', index=False, header=True)

            # reinitialize the savefiles
            savefile = np.linspace(0, 1000, 1001)
            savefile = pd.DataFrame(savefile, columns=['ignore'])
            results = pd.DataFrame({'ignore': [1]})

            w_list = list(data_frame.winfo_children())
            for element in w_list:
                element.destroy()
            global z
            z = 0

            if 'area' in globals():
                global area
                del area
            if 'area_norm' in globals():
                global area_norm
                del area_norm
            if 'rf' in globals():
                global rf
                del rf
            if 'co_area' in globals():
                global co_area
                del co_area
            if 'co_area_norm' in globals():
                global co_area_norm
                del co_area_norm
            if 'co_rf' in globals():
                global co_rf
                del co_rf
            if 'i_limiting' in globals():
                global i_limiting
                del i_limiting
            if 'R' in globals():
                global R
                del R
            if 'dflim' in globals():
                global dflim
                del dflim
            if 'i_surface_0pt9' in globals():
                global i_surface_0pt9
                del i_surface_0pt9
            if 'i_s_expol' in globals():
                global i_s_expol
                del i_s_expol
            if 'i_s_expol_etadiff' in globals():
                global i_s_expol_etadiff
                del i_s_expol_etadiff
            if 'i_mass_0pt9' in globals():
                global i_mass_0pt9
                del i_mass_0pt9
            if 'i_m_expol' in globals():
                global i_m_expol
                del i_m_expol
            if 'i_m_expol_etadiff' in globals():
                global i_m_expol_etadiff
                del i_m_expol_etadiff
            if 'i_limiting_h' in globals():
                global i_limiting_h
                del i_limiting_h
            if 'i_0_k_1' in globals():
                global i_0_k_1
                del i_0_k_1
            if 'i_0_k_eta_1' in globals():
                global i_0_k_eta_1
                del i_0_k_eta_1
            if 'i_0_k_2' in globals():
                global i_0_k_2
                del i_0_k_2
            if 'i_0_k_eta_2' in globals():
                global i_0_k_eta_2
                del i_0_k_eta_2
            if 'i_0_s_1' in globals():
                global i_0_s_1
                del i_0_s_1
            if 'i_0_s_eta_1' in globals():
                global i_0_s_eta_1
                del i_0_s_eta_1
            if 'i_0_s_2' in globals():
                global i_0_s_2
                del i_0_s_2
            if 'i_0_s_eta_2' in globals():
                global i_0_s_eta_2
                del i_0_s_eta_2
            if 'i_0_m_1' in globals():
                global i_0_m_1
                del i_0_m_1
            if 'i_0_m_eta_1' in globals():
                global i_0_m_eta_1
                del i_0_m_eta_1
            if 'i_0_m_2' in globals():
                global i_0_m_2
                del i_0_m_2
            if 'i_0_m_eta_2' in globals():
                global i_0_m_eta_2
                del i_0_m_eta_2






        else:
            pass


    SaveButton = ct.CTkButton(master=bottom_frame, text="Save", command=save, font=("Calibri", -18), width=80,
                              height=10)
    SaveButton.grid(row=1, column=2, sticky=tk.E, padx=10)
    SaveButton.configure(state=tk.DISABLED)


    def options():
        window = ct.CTkToplevel(root)
        importwindow(window, widthfactor, heightfactor)

        root.wait_window(window)

        config = open('Importconfig.txt')
        config_txt = config.readlines()
        config.close()

        global Ar_config
        global CO_config
        global ORR_config
        global ORRa_config

        Ar_config = config_txt[2].replace('\n', '').split()
        CO_config = config_txt[4].replace('\n', '').split()
        ORR_config = config_txt[6].replace('\n', '').split()
        ORRa_config = config_txt[8].replace('\n', '').split()


    OptionsButton = ct.CTkButton(master=bottom_frame, text="Import Options", command=options, font=("Calibri", -18),
                                 width=160, height=10)
    OptionsButton.grid(row=1, column=1, sticky=tk.W, padx=10)


    def change_mode():
        if switch_2.get() == 1:
            ct.set_appearance_mode("Dark")
            root.configure(bg='grey10')
            data_canvas.configure(bg='grey20')
            data_frame.configure(fg_color='grey20')
            data_frame.configure(bg_color='grey20')
        else:
            ct.set_appearance_mode("Light")
            root.configure(bg='grey90')
            data_canvas.configure(bg='grey80')
            data_frame.configure(fg_color='grey80')
            data_frame.configure(bg_color='grey80')


    switch_2 = ct.CTkSwitch(master=bottom_frame, text="Dark Mode", command=change_mode)
    switch_2.grid(row=1, column=0, sticky=tk.W, padx=10)


    def on_closing():
        root.destroy()
        exit()


    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()
