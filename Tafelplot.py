import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import linregress

test = "C:/CloudStation/Doktor/Data/RRDE/Pt-TiOx-C/test_tafel.txt"

df = pd.read_csv(test, sep='\t', skiprows=0, header=0, decimal='.')

df = df[['E-iR(lim)/V_ORR__0', 'im/A_ORR_0']].dropna()
df = df.iloc[::-1].reset_index()
del df['index']

for i in range(df.shape[0]):
    window = 10
    if i % 10 == 0:
        df1 = df.head(window + i)
        linear = linregress(np.log10(df1['im/A_ORR_0']), df1['E-iR(lim)/V_ORR__0'])
        if linear[2] >= 0.99:
            plt.plot(df['im/A_ORR_0'], linear[0] * np.log10(df['im/A_ORR_0']) + linear[1])
            print(linear)
    else:
        pass


plt.plot(df['im/A_ORR_0'], df['E-iR(lim)/V_ORR__0'])
plt.plot(df['im/A_ORR_0'], linear[0]*np.log10(df['im/A_ORR_0'])+linear[1])
plt.xscale('log')
plt.show()