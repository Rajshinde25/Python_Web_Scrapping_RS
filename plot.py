import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv (r'output.csv',encoding='cp1252')

k=df.groupby(by='State').agg('count')
k["College Name"].plot(kind ='bar')

plt.title('Total Colleges in repective States')
plt.xlabel('States')
plt.ylabel('Count')
plt.ylim(0,300)
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.show(block=True)

unique = df.groupby('State')['District'].nunique()
unique.plot.bar(x='DISTRICT', y='STATE',color = "purple")
plt.title('Total District in repective States')
plt.xlabel('States')
plt.ylabel('Count')
plt.ylim(0,100)
plt.subplots_adjust(bottom = 0.4)
plt.show(block=True)
