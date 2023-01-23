import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress

test = "C:/CloudStation/Doktor/Data/RRDE/Pt-TiOx-C/test_tafel.txt"

df = pd.read_csv(test, sep='\t', skiprows=0, header=0, decimal='.')

df = df[['E-iR(lim)/V_ORR__0', 'im/A_ORR_0']].dropna()
df = df.iloc[::-1].reset_index()
del df['index']

z = 0

if int(df.shape[0]*0.01) >= 5:
    window = int(df.shape[0]*0.01)
else:
    window = 5

for i in range(df.shape[0]-window):

    df1 = df.head(window + i)
    linear = linregress(np.log10(df1['im/A_ORR_0']), df1['E-iR(lim)/V_ORR__0'])

    if (-1*linear[2]) >= z:
        z = (-1*linear[2])
        coefficents = linear



print(z)
print(coefficents[0])
plt.plot(df['im/A_ORR_0'], df['E-iR(lim)/V_ORR__0'])
plt.plot(df['im/A_ORR_0'], coefficents[0]*np.log10(df['im/A_ORR_0'])+coefficents[1])
plt.plot(df['im/A_ORR_0'], np.linspace(0.9, 0.9, df['im/A_ORR_0'].shape[0]))
plt.xscale('log')
plt.show()