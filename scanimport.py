import pandas as pd

#testing values
Ar = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-Ar-0.02mVs-CV-0.05-0.925mV-2.txt'
O2 = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-O2-1(1).txt'
Ar_orr = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-Ar-1(1).txt'
CO_Strip = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3_20210414-RRDE3_COstrip-0.05V_1Vs-1_0.01rpm_Ar_0_GC-19936-afterORRC_all cylcles.txt'
#end of testing values


def lsvscan(filename, sepvalue=';', headervalue=0, decimalvalue='.'):
    if headervalue is None:
        colnames = ['WE(1).Potential (V)', 'WE(1).Current (A)', 'empty', 'rpm', 'time', 'potential applied', 'index']
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue, names=colnames)
    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue)
    CV_reduced = CVs.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
    CV_reduced.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
    CV_reduced.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)
    CV_reduced.reset_index()

    return CV_reduced


def singlescan(filename, scan, sepvalue=';', headervalue=0, decimalvalue='.'):
    if headervalue is None:
        colnames = ['WE(1).Potential (V)', 'WE(1).Current (A)', 'empty', 'rpm', 'time', 'time_corr', 'index']
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue, names=colnames)
    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue)
    if 'Scan' in CVs:
        CV_scan = CVs[CVs['Scan'] == scan].reset_index()
        CV_reduced = CV_scan.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
    else:
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
    return CV_cathodic, CV_anodic


def multiplescan(filename, scan, sepvalue=';', headervalue=0, decimalvalue='.'):
    if headervalue is None:
        colnames = ['WE(1).Potential (V)', 'WE(1).Current (A)', 'empty', 'rpm', 'time', 'time_corr', 'index']
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue, names=colnames)
    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=0, header=headervalue, decimal=decimalvalue)
    if 'Scan' in CVs:
        CV_scan = CVs[CVs['Scan'] == scan].reset_index()
        CV_reduced = CV_scan.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
    else:
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
    return CV_cathodic, CV_anodic