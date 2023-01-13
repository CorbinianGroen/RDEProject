import pandas as pd

# testing values
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

Ar = 'C:/CloudStation/Doktor/Data/RRDE/Pt-TiOx-C/GC3 PtTiOxC_HT/GC-21305-ORR-Ar-CV-0,05-1,05mV-0,01mVs-1600rpm-3cycles.txt'
Ar1 = 'C:/CloudStation/Doktor/Data/RRDE/Pt-TiOx-C/GC3 PtTiOxC_HT/GC-21305-ORR-Ar-CV-0,05-1,05mV-0,01mVs-1600rpm-3cyclestest.txt'
O2 = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-O2-1(1).txt'
Ar_orr = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-Ar-1(1).txt'
CO_Strip = "C:/CloudStation/Doktor/Data/RRDE/RDETesting/20220822-RRDE3/GC-16507-COStrip.txt"
Kr_test = 'C:/CloudStation/Master/Forschungspraktikum Krischer/Data/nSi-Pt_20220225/5_ar_cv_-0pt67_-0pt3_20mvs_200rpm_3cyc - Kopie.txt'
Imp_test = 'C:/CloudStation/Doktor/Data/RRDE/Pt-TiOx-C/CG2 PtC/GC-21305-Ar-200rpm-0,9356689453125V-Impedance.txt'


# end of testing values


def lsvscan(filename, sepvalue=';', headervalue=0, decimalvalue='.', skip=0, pot=0, cur=1):
    if headervalue is None:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=None, decimal=decimalvalue)
        headerlist = list(CVs)
        headerlist[pot] = 'WE(1).Potential (V)'
        headerlist[cur] = 'WE(1).Current (A)'
        CVs.columns = headerlist
    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue)
    CV_reduced = CVs.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
    CV_reduced.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
    CV_reduced.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)
    CV_reduced.reset_index()

    return 'None', CV_reduced


def singlescan(filename, sepvalue=';', headervalue=0, decimalvalue='.', skip=0, pot=0, u_V=1, cur=1, u_A=1):
    if headervalue is None:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=None, decimal=decimalvalue)
        headerlist = list(CVs)
        headerlist[pot] = 'WE(1).Potential (V)'
        headerlist[cur] = 'WE(1).Current (A)'
        CVs.columns = headerlist
    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue)

    CV_reduced = CVs.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
    CV_reduced.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
    CV_reduced.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)
    CV_reduced = CV_reduced.reset_index()
    del CV_reduced['index']

    CV_reduced['Potential/V'] = CV_reduced['Potential/V'] / u_V
    CV_reduced['Current/A'] = CV_reduced['Current/A'] / u_A

    maxima = find_peaks(CV_reduced['Potential/V'], width=10)[0]

    if len(maxima) == 0:
        upper = 0

    else:
        upper = maxima[0]

    minima = find_peaks(-CV_reduced['Potential/V'], width=10)[0]

    if len(minima) == 0:
        lower = 0

    else:
        lower = minima[0]

    if len(minima) != 0 and len(maxima) != 0:
        if maxima[0] < minima[0]:
            CV_anodic = pd.concat([CV_reduced.iloc[lower + 1:CV_reduced.shape[0]], CV_reduced.iloc[0:upper]], ignore_index=True).reset_index()
            CV_cathodic = CV_reduced.iloc[upper + 1:lower].reset_index()


        else:
            CV_cathodic = pd.concat([CV_reduced.iloc[0:lower], CV_reduced.iloc[upper + 1:CV_reduced.shape[0]]], ignore_index=True).reset_index()
            CV_anodic = CV_reduced.iloc[lower + 1:upper].reset_index()

    if len(minima) == 0:
        CV_anodic = CV_reduced.iloc[0:upper].reset_index()
        CV_cathodic = CV_reduced.iloc[upper + 1: CV_reduced.shape[0]].reset_index()

    if len(maxima) == 0:
        CV_cathodic = CV_reduced.iloc[0:lower].reset_index()
        CV_anodic = CV_reduced.iloc[lower + 1: CV_reduced.shape[0]].reset_index()

    del CV_cathodic['index']
    del CV_anodic['index']



    return CV_cathodic, CV_anodic

    '''
    CV_reduced = CVs.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
    CV_reduced.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
    CV_reduced.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)

    upper = CV_reduced['Potential/V'].nlargest(1).index[0]
    lower = CV_reduced['Potential/V'].nsmallest(1).index[0]
    CV_cathodic = CV_reduced.iloc[upper + 1:lower].reset_index()

    del CV_cathodic['index']
    CV_anodic1 = CV_reduced.iloc[0:upper]
    CV_anodic2 = CV_reduced.iloc[lower + 1:CV_reduced.shape[0]]
    CV_anodic = pd.concat([CV_anodic2, CV_anodic1], ignore_index=True).reset_index()
    del CV_anodic['index']

    CV_anodic_V = CV_anodic['Potential/V'] / u_V
    CV_anodic_A = CV_anodic['Current/A'] / u_A

    CV_anodic = pd.concat([CV_anodic_V, CV_anodic_A], axis=1, join='inner')

    CV_cathodic_V = CV_cathodic['Potential/V'] / u_V
    CV_cathodic_A = CV_cathodic['Current/A'] / u_A

    CV_cathodic = pd.concat([CV_cathodic_V, CV_cathodic_A], axis=1, join='inner')

    return CV_cathodic, CV_anodic
    '''

def multiplescan(filename, scan, sepvalue=';', headervalue=0, decimalvalue='.', skip=0, pot=2, u_V=1, cur=3, u_A=1):
    if headervalue is None:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=None, decimal=decimalvalue)
        headerlist = list(CVs)
        headerlist[pot] = 'WE(1).Potential (V)'
        headerlist[cur] = 'WE(1).Current (A)'
        CVs.columns = headerlist

    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=headervalue, decimal=decimalvalue)

    if 'Scan1' in CVs:
        CV_scan = CVs[CVs['Scan'] == scan].reset_index()
        CV_reduced = CV_scan.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]


    else:
        max = find_peaks(CVs['WE(1).Potential (V)'], width=10)[0]
        min = find_peaks(-CVs['WE(1).Potential (V)'], width=10)[0]

        first_value = CVs['WE(1).Potential (V)'].iloc[0]

        if max[0] < min[0]:
            if scan == 1:
                beginning = CVs.loc[0:max[scan - 1], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            else:
                beginning = CVs.loc[min[scan - 2]:max[scan - 1], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            end = CVs.loc[min[scan - 1]:max[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            endofscan = abs(end['WE(1).Potential (V)'] - first_value).idxmin()
            beginningofscan = abs(beginning['WE(1).Potential (V)'] - first_value).idxmin()


        else:
            if scan == 1:
                beginning = CVs.loc[0:min[scan - 1], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            else:
                beginning = CVs.loc[max[scan - 2]:min[scan - 1], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            end = CVs.loc[max[scan - 1]:min[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            endofscan = abs(end['WE(1).Potential (V)'] - first_value).idxmin()
            beginningofscan = abs(beginning['WE(1).Potential (V)'] - first_value).idxmin()

        CV_reduced = CVs.loc[beginningofscan:endofscan, ['WE(1).Potential (V)', 'WE(1).Current (A)']]

    CV_reduced.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
    CV_reduced.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)
    CV_reduced = CV_reduced.reset_index()
    del CV_reduced['index']

    CV_reduced['Potential/V'] = CV_reduced['Potential/V'] / u_V
    CV_reduced['Current/A'] = CV_reduced['Current/A'] / u_A

    maxima = find_peaks(CV_reduced['Potential/V'], width=10)[0]

    if len(maxima) == 0:
        upper = 0

    else:
        upper = maxima[0]

    minima = find_peaks(-CV_reduced['Potential/V'], width=10)[0]

    if len(minima) == 0:
        lower = 0

    else:
        lower = minima[0]

    if len(minima) != 0 and len(maxima) != 0:
        if maxima[0] < minima[0]:
            CV_anodic = pd.concat([CV_reduced.iloc[lower + 1:CV_reduced.shape[0]], CV_reduced.iloc[0:upper]], ignore_index=True).reset_index()
            CV_cathodic = CV_reduced.iloc[upper + 1:lower].reset_index()


        else:
            CV_cathodic = pd.concat([CV_reduced.iloc[0:lower], CV_reduced.iloc[upper + 1:CV_reduced.shape[0]]], ignore_index=True).reset_index()
            CV_anodic = CV_reduced.iloc[lower + 1:upper].reset_index()


    if len(minima) == 0:
        CV_anodic = CV_reduced.iloc[0:upper].reset_index()
        CV_cathodic = CV_reduced.iloc[upper + 1: CV_reduced.shape[0]].reset_index()


    if len(maxima) == 0:
        CV_cathodic = CV_reduced.iloc[0:lower].reset_index()
        CV_anodic = CV_reduced.iloc[lower + 1: CV_reduced.shape[0]].reset_index()

    del CV_cathodic['index']
    del CV_anodic['index']
    return CV_cathodic, CV_anodic


def HFRscan(filename, sepvalue=';', headervalue=0, decimalvalue='.', skip=0, R=2, u_R=1):
    if headervalue is None:
        Imp = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=None, decimal=decimalvalue)

    else:
        Imp = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=headervalue, decimal=decimalvalue)

    Imp = Imp.iloc[:, R]
    HFR = float(Imp.nsmallest(1))

    HFR = HFR / u_R

    return HFR


# for testing

# ORR = lsvscan(O2, headervalue=None)
# print(ORR)

#AR1, AR2 = multiplescan(Ar, 2, sepvalue='\t')  # , headervalue=None, skip=1)
#AR3, AR4 = multiplescan(Ar1, 1, sepvalue='\t', headervalue=None, skip=1)

#plt.plot(AR2['Potential/V'], AR2['Current/A'])
#plt.show()
#plt.plot(AR1['Potential/V'], AR1['Current/A'])
#plt.show()

# CO1, CO2 = multiplescan(CO_Strip, 1, sepvalue='\t', decimalvalue='.')
# print(CO1, CO2)

# Kr1, Kr2 = multiplescan(Kr_test, 2, sepvalue='\s+', headervalue=None, decimalvalue='.', skip=19, pot=2, cur=3)
# print(Kr1)
# print(Kr2)

# HFRscan(Imp_test, sepvalue='\t', headervalue=None, decimalvalue='.', skip=1, R=3, u_R=1)
