import tkinter as tk
from tkinter import filedialog
import customtkinter as ct

import pandas as pd
import numpy as np
from scipy import interpolate

import matplotlib.lines as lines
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

#imports of files
from importfilter import importwindow
import scanimport as scan

#testing values
loading = 3.847E-6
R = 32.7
Ref = 0.0035
Ar = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-Ar-0.02mVs-CV-0.05-0.925mV-2.txt'
O2 = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-O2-1(1).txt'
Ar_orr = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-Ar-1(1).txt'
CO_Strip = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3_20210414-RRDE3_COstrip-0.05V_1Vs-1_0.01rpm_Ar_0_GC-19936-afterORRC_all cylcles.txt'
Kr_test = 'C:/CloudStation/Master/Forschungspraktikum Krischer/Data/nSi-Pt_20220225/5_ar_cv_-0pt67_-0pt3_20mvs_200rpm_3cyc - Kopie.txt'
Kr_test_2 = "C:/CloudStation/Master/Forschungspraktikum Krischer/Data/nSi-Pt_20220225/3_ar_cv_-0pt67_0pt46_20mvs_200rpm_3cyc.txt"

radius = 0.2

cm = 1 / 2.54

#end of testing values

#apperancesetting
ct.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
#end

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
    return df


def CO_plot(df1, df2):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('CO Strip Evaluation')
    window.geometry(str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(int(d_x + widthfactor*8)) + '+' + str(int(d_y + heightfactor * 299)))
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
    higher0 = df[df['Diff'] >= 0]
    higher0 = higher0[higher0['Potential/V'] >= 0.06]
    integration = np.trapz(x=higher0['Potential/V'], y=higher0['Diff'])
    global co_area
    co_area = ((integration / 0.01) / 420e-6)

    global co_rf
    area_geo = np.pi * (radius ** 2)
    co_rf = co_area / area_geo
    firstvalue = higher0.head(1).index[0]

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())
        global co_area_norm
        co_area_norm = co_area * 0.0001 / loading

    ax_co = co_f.add_subplot(1,1,1)
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
    legend = ax_co.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)
    ax_co.fill_between(df['Potential/V'].loc[firstvalue:df.shape[0]],
                    df['Current/A_1'].loc[firstvalue:df.shape[0]],
                    df['Current/A_2'].loc[firstvalue:df.shape[0]], color=color)

    canvas.draw_idle()

    co_info_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=("grey80", 'grey20'))
    co_info_frame.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)

    co_info_frame.grid_rowconfigure(0, weight=10)
    co_info_frame.grid_rowconfigure(1, weight=1)
    co_info_frame.grid_rowconfigure(2, weight=10)
    co_info_frame.grid_columnconfigure(0, weight=0)
    co_info_frame.grid_columnconfigure(1, weight=1)
    co_info_frame.grid_columnconfigure(2, weight=0)
    # co_info_frame.grid_columnconfigure(0, minsize=140)
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
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='{0:.3f}'.format(co_area_norm), text_font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    else:
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='n.a.', text_font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_norm_frame, text='ECSA:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(Area_norm_frame, text='m²ₚₜ/gₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    rf_frame = ct.CTkFrame(master=co_variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    rf_frame.grid(row=1, column=0, sticky='nswe', pady=0, padx=5)
    rf_frame.grid_rowconfigure(0, weight=0)
    rf_frame.grid_rowconfigure(1, weight=1)
    rf_frame.grid_rowconfigure(2, weight=0)
    rf_frame.grid_columnconfigure(0, weight=0, minsize=80)
    rf_frame.grid_columnconfigure(1, weight=1, minsize=80)
    rf_frame.grid_columnconfigure(2, weight=0, minsize=125)
    rf_label = ct.CTkLabel(rf_frame, text='{0:.3f}'.format(co_rf), text_font=("Calibri", -20), width=1)
    rf_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(rf_frame, text='rf:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(rf_frame, text='cm²ₚₜ/cm²₉ₑₒ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    Area_frame = ct.CTkFrame(master=co_variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    Area_frame.grid(row=0, column=0, sticky='nswe', pady=5, padx=5)
    Area_frame.grid_rowconfigure(0, weight=0)
    Area_frame.grid_rowconfigure(1, weight=1)
    Area_frame.grid_rowconfigure(2, weight=0)
    Area_frame.grid_columnconfigure(0, weight=0, minsize=80)
    Area_frame.grid_columnconfigure(1, weight=1, minsize=80)
    Area_frame.grid_columnconfigure(2, weight=0, minsize=125)
    Area_label = ct.CTkLabel(Area_frame, text='{0:.3f}'.format(co_area), text_font=("Calibri", -20), width=1)
    Area_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_frame, text='Area Pt:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(Area_frame, text='cm²ₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    def exit1(df):
        window.destroy()
        global z
        a = z
        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=360)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='CO Strip Determination - ' + NameEntry.get(), text_font=("Calibri", -20)).grid(row=0, column=0,sticky=tk.W,padx=2, pady=5)
        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x', width=8, height=8, command=lambda: remove(a), text_font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=1, sticky=tk.E, pady=5, padx=5)
        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['a_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['a_f_{0}'.format(z)].grid(row=1, column=0, sticky='nswe', pady=5, padx=5, ipadx=2, ipady=2, columnspan=2)
        d['a_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['a_l_{0}'.format(z)] = ct.CTkLabel(d['a_f_{0}'.format(z)], text='{0:.3f}'.format(co_area), text_font=("Calibri", -20), width=1)
        d['a_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='Area Pt:', text_font=("Calibri", -20), width=1).grid(row=1,column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='cm²ₚₜ', text_font=("Calibri", -20), width=1).grid(row=1,column=2, sticky=tk.E, padx=2)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2, columnspan=2)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(co_rf),text_font=("Calibri", -20), width=1)
        d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='rf:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='cm²ₚₜ/cm²₉ₑₒ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2, columnspan=2)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(co_area_norm),text_font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', text_font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='ECSA:', text_font=("Calibri", -20), width=1).grid(row=1,column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='m²ₚₜ/gₚₜ', text_font=("Calibri", -20), width=1).grid(row=1,  column=2, sticky=tk.E, padx=2)

        data_canvas.update_idletasks()
        data_canvas.config(scrollregion=data_frame.bbox())

        df.rename(columns={'Potential/V': 'Potential/V_' + 'COStrip_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df.rename(columns={'Current/A_1': 'Current/A-1_' + 'first_scan_' + str(z)}, inplace=True)
        df.rename(columns={'Current/A_2': 'Current/A-2_' + 'second_scan_' + str(z)}, inplace=True)
        del df['Diff']
        global savefile
        savefile = pd.concat([savefile, df], axis=1)

        if LoadingEntry.get() != '':
            ecsa = co_area_norm
        else:
            ecsa = 'n.a.'

        result = pd.DataFrame({'COStrip_Area_cm^2_Pt_' + NameEntry.get() + '_' + str(z): [co_area], 'COStrip_rf_cm^2_Pt/cm^2_geo_' + str(z): [co_rf], 'COStrip_ECSA_cm^2_Pt/g_Pt_' + str(z): [ecsa]})
        global results
        results = pd.concat([results, result], axis=1)

        save_enable()

        z += 1

    button_frame = ct.CTkFrame(master=co_info_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    button_frame.grid(row=2, column=1, sticky='nswe', pady=10, padx=10)
    button_frame.grid_rowconfigure(0, weight=1)
    button_frame.grid_rowconfigure(1, weight=0)
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=0)
    button_frame.grid_columnconfigure(2, weight=0)
    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=lambda: exit1(df), text_font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, text_font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)

    def on_closing():
        window.destroy()
        # exit()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()


def Ar_Plot(anodic, cathodic):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('HUPD ECSA Evaluation')
    window.geometry(str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(int(d_x + widthfactor*8)) + '+' + str(int(d_y + heightfactor * 299)))
    #window.configure(background='white')
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
    ar_graph_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    ar_graph_frame.grid(row=0, column=0, sticky='nswe', pady=10, padx=10, ipadx=10, ipady=10)

    ar_graph_frame.grid_rowconfigure(0, weight=0)
    ar_graph_frame.grid_rowconfigure(1, weight=1)
    ar_graph_frame.grid_columnconfigure(0, weight=0, minsize=10)
    ar_graph_frame.grid_columnconfigure(1, weight=1)
    ar_graph_frame.grid_columnconfigure(2, weight=0, minsize=10)

    f = Figure(figsize=(28*cm, 18*cm), facecolor=bgcolor)

    canvas = FigureCanvasTkAgg(f, master=ar_graph_frame)
    canvas.get_tk_widget().grid(row=1, column=1)
    NavigationToolbar2Tk(canvas, ar_graph_frame, pack_toolbar=False).grid(row=0, column=1, sticky=tk.W, pady=10)

    ax = f.add_subplot(1,1,1)
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

    area_a = np.trapz(x=anodic['Potential/V'].loc[index_low:index_high],
                      y=anodic['Current/A'].loc[index_low:index_high] - init_anodic_A)
    area_c = np.trapz(x=cathodic['Potential/V'].loc[index_high_c:index_low_c],
                      y=cathodic['Current/A'].loc[index_high_c:index_low_c] - init_cathodic_A)
    global area
    area = (abs(area_a) + abs(area_c)) / 2
    area = (area / 0.02) / 201e-6

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())
        global area_norm
        area_norm = area / loading * 0.0001

    global rf
    area_geo = np.pi * (radius ** 2)
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

        area_a = np.trapz(x=anodic['Potential/V'].loc[index_low:index_high],
                          y=anodic['Current/A'].loc[index_low:index_high] - anodic_dl)
        area_c = np.trapz(x=cathodic['Potential/V'].loc[index_high_c:index_low_c],
                          y=cathodic['Current/A'].loc[index_high_c:index_low_c] - cathodic_dl)
        global area
        area = (abs(area_a) + abs(area_c)) / 2
        area = (area / 0.02) / 201e-6

        if LoadingEntry.get() != '':
            global loading
            loading = float(LoadingEntry.get())
            global area_norm
            area_norm = area / loading * 0.0001

        global rf
        area_geo = np.pi * (radius ** 2)
        rf = area / area_geo

        rf_label.config(text='{0:.3f}'.format(rf))
        Area_label.config(text='{0:.3f}'.format(area))
        if 'area_norm' in globals():
            Area_norm_label.config(text='{0:.3f}'.format(area_norm))
        else:
            Area_norm_label.config(text='n.a.')

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

    info_frame = ct.CTkFrame(master=window, corner_radius=10, fg_color=('grey80', 'grey20'))
    info_frame.grid(row=0, column=1, sticky='nswe', pady=10, padx=10)

    info_frame.grid_rowconfigure(0, weight=10)
    info_frame.grid_rowconfigure(1, weight=1)
    info_frame.grid_rowconfigure(2, weight=10)
    info_frame.grid_columnconfigure(0, weight=0)
    info_frame.grid_columnconfigure(1, weight=1)
    info_frame.grid_columnconfigure(2, weight=0)
    #info_frame.grid_columnconfigure(0, minsize=140)
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
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='{0:.3f}'.format(area_norm), text_font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    else:
        Area_norm_label = ct.CTkLabel(Area_norm_frame, text='n.a.', text_font=("Calibri", -20), width=1)
        Area_norm_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_norm_frame, text='ECSA:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(Area_norm_frame, text='m²ₚₜ/gₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    rf_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    rf_frame.grid(row=1, column=0, sticky='nswe', pady=0, padx=5)
    rf_frame.grid_rowconfigure(0, weight=0)
    rf_frame.grid_rowconfigure(1, weight=1)
    rf_frame.grid_rowconfigure(2, weight=0)
    rf_frame.grid_columnconfigure(0, weight=0, minsize=80)
    rf_frame.grid_columnconfigure(1, weight=1, minsize=80)
    rf_frame.grid_columnconfigure(2, weight=0, minsize=125)
    rf_label = ct.CTkLabel(rf_frame, text='{0:.3f}'.format(rf), text_font=("Calibri", -20), width=1)
    rf_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(rf_frame, text='rf:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(rf_frame, text='cm²ₚₜ/cm²₉ₑₒ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    Area_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=("grey80", 'grey20'))
    Area_frame.grid(row=0, column=0, sticky='nswe', pady=5, padx=5)
    Area_frame.grid_rowconfigure(0, weight=0)
    Area_frame.grid_rowconfigure(1, weight=1)
    Area_frame.grid_rowconfigure(2, weight=0)
    Area_frame.grid_columnconfigure(0, weight=0, minsize=80)
    Area_frame.grid_columnconfigure(1, weight=1, minsize=80)
    Area_frame.grid_columnconfigure(2, weight=0, minsize=125)
    Area_label = ct.CTkLabel(Area_frame, text='{0:.3f}'.format(area), text_font=("Calibri", -20), width=1)
    Area_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(Area_frame, text='Area Pt:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(Area_frame, text='cm²ₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    def exit1():
        window.destroy()
        global z

        a = z

        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=360)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='HUPD Determination - ' + NameEntry.get(), text_font=("Calibri", -20)).grid(row=0, column=0, sticky=tk.W, padx=2, pady=5)
        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x',width=8, height=8, command=lambda: remove(a), text_font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=1, sticky=tk.E, pady=5, padx=5)

        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['a_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['a_f_{0}'.format(z)].grid(row=1, column=0, columnspan=2, sticky='nswe', pady=5, padx=5, ipadx=2, ipady=2)
        d['a_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['a_l_{0}'.format(z)] = ct.CTkLabel(d['a_f_{0}'.format(z)], text='{0:.3f}'.format(area), text_font=("Calibri", -20), width=1)
        d['a_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='Area Pt:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='cm²ₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, columnspan=2, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(rf), text_font=("Calibri", -20), width=1)
        d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='rf:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='cm²ₚₜ/cm²₉ₑₒ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0,columnspan=2, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(area_norm), text_font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', text_font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='ECSA:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='m²ₚₜ/gₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        data_canvas.update_idletasks()
        data_canvas.config(scrollregion=data_frame.bbox())

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

        result = pd.DataFrame({'HUPD_Area_cm^2_Pt_' + NameEntry.get() + '_' + str(z): [area], 'HUPD_rf_cm^2_Pt/cm^2_geo_' + str(z): [rf], 'HUPD_ECSA_cm^2_Pt/g_Pt_' + str(z): [ecsa]})
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
    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=exit1, text_font=("Calibri", -24), text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, text_font=("Calibri", -24), text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)


    def on_closing():
        window.destroy()
        # exit()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()


def O2_plot(O2, Ar):
    d_x = root.winfo_x()
    d_y = root.winfo_y()
    window = tk.Toplevel(root)
    window.grab_set()
    window.title('ORR Evaluation')
    window.geometry(str(int(widthfactor * (width * 0.752))) + 'x' + str(int(heightfactor * (height * 0.615))) + '+' + str(int(d_x + widthfactor*8)) + '+' + str(int(d_y + heightfactor * 299)))
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

    df = interpolation(O2, Ar)
    df['Diff/A'] = df['Current/A_1'] - df['Current/A_2']
    df['E-iR/V'] = df['Potential/V'] - (df['Diff/A'] * R) - Ref

    v = df['E-iR/V']
    df = df.drop(['E-iR/V'], axis=1)
    df.insert(0, 'E-iR/V', v)

    max_current = df['Diff/A'].loc[df['Diff/A'].nlargest(1).index[0]]
    min_current = df['Diff/A'].loc[df['Diff/A'].nsmallest(1).index[0]]

    index_low = df.iloc[(df['Potential/V'] - 0.3).abs().argsort()[:1]].index[0]
    index_high = df.iloc[(df['Potential/V'] - 0.5).abs().argsort()[:1]].index[0]

    i_limiting = df['Diff/A'].loc[index_low:index_high].mean()
    index_0pt9 = df.iloc[(df['E-iR/V'] - 0.9).abs().argsort()[:1]].index[0]

    df['ik/A'] = (i_limiting * df['Diff/A']) / (i_limiting - df['Diff/A'])

    if 'area' in globals():
        df['is/A'] = abs(df['ik/A']) / area * 1000
        global i_surface_0pt9
        i_surface_0pt9 = df['is/A'].loc[index_0pt9]

    if LoadingEntry.get() != '':
        global loading
        loading = float(LoadingEntry.get())
        df['im/A'] = abs(df['ik/A']) / loading / 1000
        global i_mass_0pt9
        i_mass_0pt9 = df['im/A'].loc[index_0pt9]

    ax_o2.plot(df['E-iR/V'], df['Diff/A'], label='ORR_corrected')
    legend = ax_o2.legend(loc='lower right', frameon=False)
    for text in legend.get_texts():
        text.set_color(fgcolor)

    def dragged():
        lower_potential = Tline.getvalue()
        upper_potential = Tline2.getvalue()

        index_low = df.iloc[(df['Potential/V'] - lower_potential).abs().argsort()[:1]].index[0]
        index_high = df.iloc[(df['Potential/V'] - upper_potential).abs().argsort()[:1]].index[0]

        i_limiting = df['Diff/A'].loc[index_low:index_high].mean()
        index_0pt9 = df.iloc[(df['E-iR/V'] - 0.9).abs().argsort()[:1]].index[0]

        df['ik/A'] = (i_limiting * df['Diff/A']) / (i_limiting - df['Diff/A'])
        il_label.config(text='{0:.3e}'.format(i_limiting))

        if 'area' in globals():
            df['is/A'] = abs(df['ik/A']) / area * 1000
            global i_surface_0pt9
            i_surface_0pt9 = df['is/A'].loc[index_0pt9]
            is_label.config(text='{0:.3f}'.format(i_surface_0pt9))
        else:
            is_label.config(text='n.a.')

        if LoadingEntry.get() != '':
            global loading
            loading = float(LoadingEntry.get())
            df['im/A'] = abs(df['ik/A']) / loading / 1000
            global i_mass_0pt9
            i_mass_0pt9 = df['im/A'].loc[index_0pt9]
            im_label.config(text='{0:.3f}'.format(i_mass_0pt9))
        else:
            im_label.config(text='n.a.')


    class draggable_line:
        def __init__(self,canvas, ax, kind, XorY):
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
                #print("line selected ", event.artist)
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

            #print(self.XorY)
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
    is_frame.grid_columnconfigure(0, weight=0, minsize=80)
    is_frame.grid_columnconfigure(1, weight=1, minsize=115)
    is_frame.grid_columnconfigure(2, weight=0, minsize=90)
    if 'area' in globals():
        is_label = ct.CTkLabel(is_frame, text='{0:.3f}'.format(i_surface_0pt9), text_font=("Calibri", -20), width=1)
        is_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    else:
        is_label = ct.CTkLabel(is_frame, text='n.a.', text_font=("Calibri", -20), width=1)
        is_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(is_frame, text='iₛ:',text_font=("Calibri", -20),  width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(is_frame, text='A/cm²ₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    im_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    im_frame.grid(row=2, column=0, sticky='nswe', pady=5, padx=5)
    im_frame.grid_rowconfigure(0, weight=0)
    im_frame.grid_rowconfigure(1, weight=1)
    im_frame.grid_rowconfigure(2, weight=0)
    im_frame.grid_columnconfigure(0, weight=0, minsize=80)
    im_frame.grid_columnconfigure(1, weight=1, minsize=115)
    im_frame.grid_columnconfigure(2, weight=0, minsize=90)
    if LoadingEntry.get() != '':
        im_label = ct.CTkLabel(im_frame, text='{0:.3f}'.format(i_mass_0pt9), text_font=("Calibri", -20), width=1)
        im_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    else:
        im_label = ct.CTkLabel(im_frame, text='n.a.', text_font=("Calibri", -20), width=1)
        im_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(im_frame, text='iₘ:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(im_frame, text='mA/mgₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    il_frame = ct.CTkFrame(master=variable_frame, corner_radius=10, fg_color=('grey80', 'grey20'))
    il_frame.grid(row=0, column=0, sticky='nswe', pady=5, padx=5)
    il_frame.grid_rowconfigure(0, weight=0)
    il_frame.grid_rowconfigure(1, weight=1)
    il_frame.grid_rowconfigure(2, weight=0)
    il_frame.grid_columnconfigure(0, weight=0, minsize=80)
    il_frame.grid_columnconfigure(1, weight=1, minsize=115)
    il_frame.grid_columnconfigure(2, weight=0, minsize=90)
    il_label = ct.CTkLabel(il_frame, text='{0:.3e}'.format(i_limiting), text_font=("Calibri", -20), width=1)
    il_label.grid(row=1, column=1, sticky=tk.E, padx=0)
    ct.CTkLabel(il_frame, text='iₗᵢₘ:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
    ct.CTkLabel(il_frame, text='A', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

    def exit1(df):
        window.destroy()
        global z
        a = z
        d['v_f_{0}'.format(z)] = ct.CTkFrame(master=data_frame, corner_radius=10, fg_color=("grey70", 'grey30'))
        d['v_f_{0}'.format(z)].grid(row=z * 2 + 1, column=1, sticky='nswe')
        d['v_f_{0}'.format(z)].grid_columnconfigure(0, weight=1, minsize=360)
        d['v_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['v_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(2, weight=1)
        d['v_f_{0}'.format(z)].grid_rowconfigure(3, weight=1)
        ct.CTkLabel(d['v_f_{0}'.format(z)], text='ORR Determination - ' + NameEntry.get(), text_font=("Calibri", -20)).grid(row=0, column=0, sticky=tk.W, padx=2, pady=5)
        ct.CTkButton(master=d['v_f_{0}'.format(z)], text='x', width=8, height=8, command=lambda: remove(a), text_font=("Calibri", -20), text_color=("grey20", 'grey80')).grid(row=0, column=1, sticky=tk.E, pady=5, padx=5)

        data_frame.grid_rowconfigure(z * 2 + 2, minsize=10)

        d['a_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['a_f_{0}'.format(z)].grid(row=1, column=0, sticky='nswe', pady=5, padx=5, ipadx=2, ipady=2, columnspan=2)
        d['a_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        d['a_l_{0}'.format(z)] = ct.CTkLabel(d['a_f_{0}'.format(z)], text='{0:.3e}'.format(i_limiting), text_font=("Calibri", -20), width=1)
        d['a_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='iₗᵢₘ:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_f_{0}'.format(z)], text='A', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        d['rf_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['rf_f_{0}'.format(z)].grid(row=2, column=0, sticky='nswe', pady=0, padx=5, ipadx=2, ipady=2, columnspan=2)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['rf_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['rf_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if 'area' in globals():
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='{0:.3f}'.format(i_surface_0pt9), text_font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        else:
            d['rf_l_{0}'.format(z)] = ct.CTkLabel(d['rf_f_{0}'.format(z)], text='n.a.', text_font=("Calibri", -20), width=1)
            d['rf_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='iₛ:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['rf_f_{0}'.format(z)], text='A/cm²ₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        d['a_n_f_{0}'.format(z)] = ct.CTkFrame(master=d['v_f_{0}'.format(z)], corner_radius=10, fg_color=('grey80', 'grey20'))
        d['a_n_f_{0}'.format(z)].grid(row=3, column=0, sticky='nswe', pady=5, padx=5, ipady=2, ipadx=2, columnspan=2)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(0, weight=0)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(1, weight=1)
        d['a_n_f_{0}'.format(z)].grid_rowconfigure(2, weight=0)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(0, weight=0, minsize=80)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(1, weight=1, minsize=100)
        d['a_n_f_{0}'.format(z)].grid_columnconfigure(2, weight=0, minsize=125)
        if LoadingEntry.get() != '':
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='{0:.3f}'.format(i_mass_0pt9), text_font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        else:
            d['a_n_l_{0}'.format(z)] = ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='n.a.', text_font=("Calibri", -20), width=1)
            d['a_n_l_{0}'.format(z)].grid(row=1, column=1, sticky=tk.E, padx=0)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='iₘ:', text_font=("Calibri", -20), width=1).grid(row=1, column=0, sticky=tk.E, padx=2)
        ct.CTkLabel(d['a_n_f_{0}'.format(z)], text='mA/mgₚₜ', text_font=("Calibri", -20), width=1).grid(row=1, column=2, sticky=tk.E, padx=2)

        data_canvas.update_idletasks()
        data_canvas.config(scrollregion=data_frame.bbox())

        df.rename(columns={'E-iR/V': 'E-iR/V_' + 'ORR_' + NameEntry.get() + '_' + str(z)}, inplace=True)
        df.rename(columns={'Diff/A': 'Current/A_' + 'ORR_' + str(z)}, inplace=True)
        df.rename(columns={'ik/A': 'ik/A_' + 'ORR_' + str(z)}, inplace=True)
        if 'is/A' in df:
            df.rename(columns={'is/A': 'is/A_' + 'ORR_' + str(z)}, inplace=True)
        if 'im/A' in df:
            df.rename(columns={'im/A': 'im/A_' + 'ORR_' + str(z)}, inplace=True)

        del df['Potential/V']
        del df['Current/A_1']
        del df['Current/A_2']

        global savefile
        savefile = pd.concat([savefile, df], axis=1)

        if LoadingEntry.get() != '':
            i_m = i_mass_0pt9
        else:
            i_m = 'n.a.'

        if 'area' in globals():
            i_s = i_surface_0pt9
        else:
            i_s = 'n.a.'

        result = pd.DataFrame({'ORR_i_lim_A_' + NameEntry.get() + '_' + str(z): [i_limiting], 'ORR_i_s_A/cm^2_Pt_' + str(z): [i_s], 'ORR_i_m_mA/mg_Pt_' + str(z): [i_m]})
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
    ct.CTkButton(button_frame, text='Submit', width=100, height=50, command=lambda: exit1(df), text_font=("Calibri", -24),text_color=("grey20", 'grey80')).grid(row=1, column=2, sticky="se", pady=10, padx=10)

    def exit2():
        window.destroy()

    ct.CTkButton(button_frame, text='Cancel', width=100, height=50, command=exit2, text_font=("Calibri", -24),
                 text_color=("grey20", 'grey80')).grid(row=1, column=1, sticky="se", pady=10, padx=10)

    def on_closing():
        window.destroy()
        # exit()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    window.mainloop()

if __name__ == '__main__':
    root = ct.CTk()
    root.title('RDE Evaluation')
    root.iconphoto(True, tk.PhotoImage(file='iconRDE.png'))
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    widthfactor = width / 1920
    heightfactor = height / 1080
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

    data_canvas.config(yscrollcommand=yscrollbar.set)
    yscrollbar.config(command=data_canvas.yview)

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
    NameLabel = ct.CTkLabel(master=input_frame, text='Name:', text_font=("Calibri", -18))
    NameLabel.grid(row=1, column=1, sticky=tk.W)
    NameEntry = ct.CTkEntry(master=input_frame, width=200, text_font=("Calibri", -14))
    NameEntry.grid(row=1, column=2, sticky=tk.W)

    LoadingLabel = ct.CTkLabel(master=input_frame, text='Loading [g]:', text_font=("Calibri", -18))
    LoadingLabel.grid(row=3, column=1, sticky=tk.W)
    LoadingEntry = ct.CTkEntry(master=input_frame, width=200, text_font=("Calibri", -14))
    LoadingEntry.grid(row=3, column=2, sticky=tk.W)

    RLabel = ct.CTkLabel(master=input_frame, text=u'HFR [\u03A9]:', text_font=("Calibri", -18))
    RLabel.grid(row=5, column=1, sticky=tk.W)
    REntry = ct.CTkEntry(master=input_frame, width=200, text_font=("Calibri", -14))
    REntry.grid(row=5, column=2, sticky=tk.W)

    RefLabel = ct.CTkLabel(master=input_frame, text='Ref [V]:', text_font=("Calibri", -18))
    RefLabel.grid(row=7, column=1, sticky=tk.W)
    RefEntry = ct.CTkEntry(master=input_frame, width=200, text_font=("Calibri", -14))
    RefEntry.grid(row=7, column=2, sticky=tk.W)

    HUPDLabel = ct.CTkLabel(master=input_frame, text='Ar CV:', text_font=("Calibri", -18))
    HUPDLabel.grid(row=1, column=4, sticky=tk.W)
    HUPDEntry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    HUPDEntry.grid(row=1, column=5, sticky=tk.W)


    def HUPD():
        file = filedialog.askopenfilename(title='Open HUPD file', initialdir='/', filetypes=[('Textfile', '*.txt')])
        if file is not None:
            HUPDEntry.delete(0, 'end')
            HUPDEntry.insert(0, file)
            HUPDEval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=HUPD, text_font=("Calibri", -18), width=80).grid(row=1, column=6, sticky=tk.W, padx=20)


    def Ar_graph():
        # Ar = HUPDEntry.get()
        #Ar_cathodic, Ar_anodic = scan.singlescan(Ar)
        Kr1, Kr2 = scan.multiplescan(Kr_test_2, 2, sepvalue='\s+', headervalue=None, decimalvalue='.', skip=19, pot=2, cur=3)
        Ar_Plot(Kr2, Kr1)
        #Ar_Plot(Ar_anodic, Ar_cathodic)


    HUPDEval = ct.CTkButton(master=input_frame, text='Eval', command=Ar_graph, text_font=("Calibri", -18), width=80)
    HUPDEval.grid(row=1, column=7, sticky=tk.W, padx=20)
    # HUPDEval.configure(state=tk.DISABLED)

    COStripLabel = ct.CTkLabel(master=input_frame, text='CO Strip:', text_font=("Calibri", -18))
    COStripLabel.grid(row=3, column=4, sticky=tk.W)
    COStripEntry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    COStripEntry.grid(row=3, column=5, sticky=tk.W)


    def COStrip():
        file = filedialog.askopenfilename(title='Open COStrip file', initialdir='/', filetypes=[('Textfile', '*.txt')])
        if file is not None:
            COStripEntry.delete(0, 'end')
            COStripEntry.insert(0, file)
            HUPDEval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=COStrip, text_font=("Calibri", -18), width=80).grid(row=3, column=6, sticky=tk.W, padx=20)


    def CO_Strip_graph():
        # CO_Strip = COStripEntry.get()
        CO_cathodic_1, CO_anodic_1 = scan.multiplescan(CO_Strip, 1, sepvalue='\t', decimalvalue=',')
        CO_cathodic_2, CO_anodic_2 = scan.multiplescan(CO_Strip, 2, sepvalue='\t', decimalvalue=',')
        CO_plot(CO_anodic_1, CO_anodic_2)


    COStripEval = ct.CTkButton(master=input_frame, text='Eval', command=CO_Strip_graph, text_font=("Calibri", -18), width=80)
    COStripEval.grid(row=3, column=7, sticky=tk.W, padx=20)
    # COStripEval.configure(state=tk.DISABLED)

    ORRLabel = ct.CTkLabel(master=input_frame, text='ORR O2:', text_font=("Calibri", -18))
    ORRLabel.grid(row=5, column=4, sticky=tk.W)
    ORREntry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    ORREntry.grid(row=5, column=5, sticky=tk.W)


    def ORR():
        file = filedialog.askopenfilename(title='Open ORR O2 file', initialdir='/', filetypes=[('Textfile', '*.txt')])
        if file is not None:
            ORREntry.delete(0, 'end')
            ORREntry.insert(0, file)
            if ORRArEntry.get() != '':
                ORREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=ORR, text_font=("Calibri", -18), width=80).grid(row=5, column=6, sticky=tk.W, padx=20)

    ORRArLabel = ct.CTkLabel(master=input_frame, text='ORR Ar:', text_font=("Calibri", -18))
    ORRArLabel.grid(row=7, column=4, sticky=tk.W)
    ORRArEntry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    ORRArEntry.grid(row=7, column=5, sticky=tk.W)


    def ORR_Ar():
        file = filedialog.askopenfilename(title='Open ORR Ar file', initialdir='/', filetypes=[('Textfile', '*.txt')])
        if file is not None:
            ORRArEntry.delete(0, 'end')
            ORRArEntry.insert(0, file)
            if ORREntry.get() != '':
                ORREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=ORR_Ar, text_font=("Calibri", -18), width=80).grid(row=7, column=6, sticky=tk.W, padx=20)


    def ORR_graph():
        # O2 = ORREntry.get()
        # Ar_orr = ORRArEntry.get()
        R = None
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
            O2_anodic = scan.lsvscan(O2, headervalue=None)
            Ar_anodic_orr = scan.lsvscan(Ar_orr, headervalue=None)
            O2_plot(O2_anodic, Ar_anodic_orr)


    ORREval = ct.CTkButton(master=input_frame, text='Eval', command=ORR_graph, text_font=("Calibri", -18), width=80)
    ORREval.grid(row=5, column=7, rowspan=3, sticky=tk.W, padx=20)
    # ORREval.configure(state=tk.DISABLED)

    HORLabel = ct.CTkLabel(master=input_frame, text='HOR H2:', text_font=("Calibri", -18))
    HORLabel.grid(row=9, column=4, sticky=tk.W)
    HOREntry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    HOREntry.grid(row=9, column=5, sticky=tk.W)


    def HOR():
        file = filedialog.askopenfilename(title='Open HOR H2 file', initialdir='/', filetypes=[('Textfile', '*.txt')])
        if file is not None:
            HOREntry.delete(0, 'end')
            HOREntry.insert(0, file)
            if HORArEntry.get() != '':
                HOREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=HOR, text_font=("Calibri", -18), width=80).grid(row=9, column=6, sticky=tk.W, padx=20)

    HORArLabel = ct.CTkLabel(master=input_frame, text='HOR Ar:', text_font=("Calibri", -18))
    HORArLabel.grid(row=11, column=4, sticky=tk.W)
    HORArEntry = ct.CTkEntry(master=input_frame, width=400, text_font=("Calibri", -14))
    HORArEntry.grid(row=11, column=5, sticky=tk.W)


    def HOR_Ar():
        file = filedialog.askopenfilename(title='Open HOR Ar file', initialdir='/', filetypes=[('Textfile', '*.txt')])
        if file is not None:
            HORArEntry.delete(0, 'end')
            HORArEntry.insert(0, file)
            if HOREntry.get() != '':
                HOREval.configure(state=tk.NORMAL)


    ct.CTkButton(master=input_frame, text='Open', command=HOR_Ar, text_font=("Calibri", -18), width=80).grid(row=11, column=6, sticky=tk.W, padx=20)


    def HOR_graph():
        pass
        # H2 = HOREntry.get()
        # Ar_hor = HORArEntry.get()
        # H2_anodic = lsvscan(H2, headervalue=None)
        # Ar_anodic_HOR = lsvscan(Ar_hor, headervalue=None)
        # H2_plot(O2_anodic, Ar_anodic_HOR)


    HOREval = ct.CTkButton(master=input_frame, text='Eval', command=HOR_graph, text_font=("Calibri", -18), width=80)
    HOREval.grid(row=9, column=7, rowspan=3, sticky=tk.W, padx=20)
    HOREval.configure(state=tk.DISABLED)


    def save_enable():
        amount = len(list(data_frame.winfo_children()))
        if amount > 0:
            SaveButton.config(state=tk.NORMAL)
        else:
            SaveButton.config(state=tk.DISABLED)


    def save():
        file = filedialog.asksaveasfilename(title='Save As', initialdir='/', filetypes=[('Textfile', '*.txt')], initialfile=NameEntry.get())
        if file.strip():
            del savefile['ignore']
            del results['ignore']
            file1 = file + '.txt'
            file2 = file + '_results.txt'
            print(file1)
            # savefile.to_csv(file1, sep='\t', index=False, header=True)
            # results.to_csv(file2, sep='\t', index=False, header=True)
            w_list = list(data_frame.winfo_children())
            for element in w_list:
                element.destroy()
            global z
            z = 0
        else:
            pass


    SaveButton = ct.CTkButton(master=bottom_frame, text="Save", command=save, text_font=("Calibri", -18), width=80, height=10)
    SaveButton.grid(row=1, column=2, sticky=tk.E, padx=10)
    SaveButton.config(state=tk.DISABLED)


    def options():
        importwindow(root, widthfactor, heightfactor)

        config = open('Importconfig.txt')
        config_txt = config.readlines()
        config.close()

        Ar_config = config_txt[2].replace('\n', '').split()
        CO_config = config_txt[4].replace('\n', '').split()


    OptionsButton = ct.CTkButton(master=bottom_frame, text="Import Options", command=options, text_font=("Calibri", -18), width=160, height=10)
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

