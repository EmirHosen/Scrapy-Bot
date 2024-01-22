#import library
import pandas as pd

#import Ex File
file_path = r'C:\Users\weble\Desktop\Scrapy Bot\Scrapy-Bot\Tourthief\Scapy\spiders\Prices.xlsx'
df = pd.read_excel(file_path)
Prices = df.values.tolist()

#Bubble Sort 
for x in range(1, len(Prices)):
    for j in range(0, len(Prices) - 1):
        if Prices[j] > Prices[j + 1]:
            Prices[j], Prices[j + 1] = Prices[j + 1], Prices[j]

#Show data
print(Prices)
#Save Data 
df = pd.DataFrame({'Prices': Prices })
df.to_excel('Prices-Sort-Tork.xlsx', index=False)