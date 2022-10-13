import pandas as pd

#testing values
Ar = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-Ar-0.02mVs-CV-0.05-0.925mV-2.txt'
O2 = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-O2-1(1).txt'
Ar_orr = 'C:/CloudStation/Master/Forschungspraktikum Paulette/Data/RDE/20210414-RRDE3/20210414-RRDE3-1600rpm-0.02mVs-1-0.05mV-ORR-an-19936-CN-S31-Ar-1(1).txt'
CO_Strip = "C:/CloudStation/Doktor/Data/RRDE/RDETesting/20220822-RRDE3/GC-16507-COStrip.txt"
Kr_test = 'C:/CloudStation/Master/Forschungspraktikum Krischer/Data/nSi-Pt_20220225/5_ar_cv_-0pt67_-0pt3_20mvs_200rpm_3cyc - Kopie.txt'
#end of testing values


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


def multiplescan(filename, scan, sepvalue=';', headervalue=0, decimalvalue='.', skip=0, pot=2, u_V=1, cur=3, u_A=1):
    if headervalue is None:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=None, decimal=decimalvalue)
        headerlist = list(CVs)
        headerlist[pot] = 'WE(1).Potential (V)'
        headerlist[cur] = 'WE(1).Current (A)'
        CVs.columns = headerlist

    else:
        CVs = pd.read_csv(filename, sep=sepvalue, skiprows=skip, header=headervalue, decimal=decimalvalue)

    if 'Scan' in CVs:
        CV_scan = CVs[CVs['Scan'] == scan].reset_index()
        CV_reduced = CV_scan.loc[:, ['WE(1).Potential (V)', 'WE(1).Current (A)']]
        CV_reduced.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
        CV_reduced.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)

        upper = CV_reduced['Potential/V'].nlargest(1).index[0]
        lower = CV_reduced['Potential/V'].nsmallest(1).index[0]

        if upper == (CV_reduced.shape[0] - 1):
            CV_anodic = CV_reduced.iloc[lower+1:CV_reduced.shape[0]].reset_index()
            CV_cathodic = CV_reduced.iloc[0:lower].reset_index()

        else:
            CV_cathodic = CV_reduced.iloc[upper + 1:lower].reset_index()
            CV_anodic1 = CV_reduced.iloc[0:upper]
            CV_anodic2 = CV_reduced.iloc[lower + 1:CV_reduced.shape[0]]
            CV_anodic = pd.concat([CV_anodic2, CV_anodic1], ignore_index=True).reset_index()

        del CV_cathodic['index']
        del CV_anodic['index']
        return CV_cathodic, CV_anodic

    else:
        max = CVs.loc[:, 'WE(1).Potential (V)'][(CVs.loc[:, 'WE(1).Potential (V)'].shift(2) < CVs.loc[:, 'WE(1).Potential (V)']) & (CVs.loc[:, 'WE(1).Potential (V)'].shift(-2) < CVs.loc[:, 'WE(1).Potential (V)'])]
        max = max.reset_index()
        max_sorted_1 = max[(max['index'] + 1 == max['index'].shift(-1))].reset_index()
        del max_sorted_1['level_0']
        max_sorted_2 = max[(max['index'] - 1 == max['index'].shift(1))].reset_index()
        del max_sorted_2['level_0']
        max_sorted_3 = max[(max['index'] + 1 != max['index'].shift(-1)) & (max['index'] - 1 != max['index'].shift(1))].reset_index()
        max_list = list(max_sorted_3['index'])

        for i in range(max_sorted_1.shape[0]):
            if max_sorted_1.loc[i, 'WE(1).Potential (V)'] > max_sorted_2.loc[i, 'WE(1).Potential (V)']:
                max_list.append(max_sorted_1.loc[i, 'index'])
            if max_sorted_1.loc[i, 'WE(1).Potential (V)'] <= max_sorted_2.loc[i, 'WE(1).Potential (V)']:
                max_list.append(max_sorted_2.loc[i, 'index'])
        max_list.append(0)
        max_list.append(CVs.shape[0])
        max_list.sort()

        min = CVs.loc[:, 'WE(1).Potential (V)'][(CVs.loc[:, 'WE(1).Potential (V)'].shift(2) > CVs.loc[:, 'WE(1).Potential (V)']) & (CVs.loc[:, 'WE(1).Potential (V)'].shift(-2) > CVs.loc[:, 'WE(1).Potential (V)'])]
        min = min.reset_index()
        min_sorted_1 = min[(min['index'] + 1 == min['index'].shift(-1))].reset_index()
        del min_sorted_1['level_0']
        min_sorted_2 = min[(min['index'] - 1 == min['index'].shift(1))].reset_index()
        del min_sorted_2['level_0']
        min_sorted_3 = min[(min['index'] + 1 != min['index'].shift(-1)) & (min['index'] - 1 != min['index'].shift(1))].reset_index()
        min_list = list(min_sorted_3['index'])

        for i in range(min_sorted_1.shape[0]):
            if min_sorted_1.loc[i, 'WE(1).Potential (V)'] <= min_sorted_2.loc[i, 'WE(1).Potential (V)']:
                min_list.append(min_sorted_1.loc[i, 'index'])
            if min_sorted_1.loc[i, 'WE(1).Potential (V)'] > min_sorted_2.loc[i, 'WE(1).Potential (V)']:
                min_list.append(min_sorted_2.loc[i, 'index'])

        min_list.append(0)
        min_list.append(CVs.shape[0])
        min_list.sort()

        if max_list[1] < min_list[1]:
            CV_cathodic = CVs.loc[max_list[scan] + 1:min_list[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']].reset_index()
            del CV_cathodic['index']
            value = CVs.loc[0, 'WE(1).Potential (V)']

            anodic = CVs.loc[min_list[scan - 1] + 1:max_list[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            CV_anodic_1 = CVs.loc[abs(anodic['WE(1).Potential (V)'] - value).nsmallest(1).index[0]:max_list[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']]

            anodic = CVs.loc[min_list[scan] + 1:max_list[scan + 1], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            CV_anodic_2 = CVs.loc[min_list[scan] + 1: abs(anodic['WE(1).Potential (V)'] - value).nsmallest(1).index[0], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            CV_anodic = pd.concat([CV_anodic_2, CV_anodic_1], ignore_index=True)


        else:
            CV_anodic = CVs.loc[min_list[scan] + 1:max_list[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']].reset_index()
            del CV_anodic['index']
            value = CVs.loc[0, 'WE(1).Potential (V)']

            cathodic = CVs.loc[max_list[scan - 1] + 1:min_list[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            CV_cathodic_1 = CVs.loc[abs(cathodic['WE(1).Potential (V)'] - value).nsmallest(1).index[0]:min_list[scan], ['WE(1).Potential (V)', 'WE(1).Current (A)']]

            cathodic = CVs.loc[max_list[scan] + 1:min_list[scan + 1], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            CV_cathodic_2 = CVs.loc[max_list[scan] + 1: abs(cathodic['WE(1).Potential (V)'] - value).nsmallest(1).index[0], ['WE(1).Potential (V)', 'WE(1).Current (A)']]
            CV_cathodic = pd.concat([CV_cathodic_2, CV_cathodic_1], ignore_index=True)

        CV_cathodic.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
        CV_cathodic.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)
        CV_anodic.rename(columns={'WE(1).Potential (V)': 'Potential/V'}, inplace=True)
        CV_anodic.rename(columns={'WE(1).Current (A)': 'Current/A'}, inplace=True)

        CV_anodic_V = CV_anodic['Potential/V'] / u_V
        CV_anodic_A = CV_anodic['Current/A'] / u_A

        CV_anodic = pd.concat([CV_anodic_V, CV_anodic_A], axis=1, join='inner')

        CV_cathodic_V = CV_cathodic['Potential/V'] / u_V
        CV_cathodic_A = CV_cathodic['Current/A'] / u_A

        CV_cathodic = pd.concat([CV_cathodic_V, CV_cathodic_A], axis=1, join='inner')

        return CV_cathodic, CV_anodic


#for testing

#ORR = lsvscan(O2, headervalue=None)
#print(ORR)

#AR1, AR2 = singlescan(Ar, u_A=1000)
#print(AR1, AR2)

#CO1, CO2 = multiplescan(CO_Strip, 1, sepvalue='\t', decimalvalue='.')
#print(CO1, CO2)

#Kr1, Kr2 = multiplescan(Kr_test, 2, sepvalue='\s+', headervalue=None, decimalvalue='.', skip=19, pot=2, cur=3)
#print(Kr1)
#print(Kr2)
