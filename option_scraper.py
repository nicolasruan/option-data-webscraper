from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

data = [[], [], [], []]


pages = [
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-05-14-w&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-05-21-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-05-28-w&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-06-04-w&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-06-11-w&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-06-18-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-07-16-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-08-20-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-09-17-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2021-10-15-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2022-01-21-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2022-06-17-m&moneyness=allRows",
         "https://www.barchart.com/stocks/quotes/PG/options?expiration=2023-01-20-m&moneyness=allRows"]

for page in pages:
    
    driver.get(page)

    content = driver.page_source
    soup = BeautifulSoup(content, "lxml")



    maturity_wrapper = soup.find('div', attrs = {'class':'column small-12 medium-4 large-4'})
    maturity = maturity_wrapper.text.splitlines()[1].split()[0]

    containers = soup.find_all("tr", attrs = {'class':'odd'})

    laststrike = 50
    optiontype = 0

    for a in containers:
        strike_wrapper = a.find('td', attrs={'class':'strikePrice'})
        price_wrapper = a.find('td', attrs={'class':'midpoint'})
        

        price = price_wrapper.text.splitlines()[8]
        strike = strike_wrapper.text.splitlines()[8]

        if float(strike) < laststrike:
            optiontype = 1
        else:
            laststrike = float(strike)

        data[0].append(strike)
        data[1].append(price)
        data[2].append(optiontype)
        data[3].append(maturity)
        


df = pd.DataFrame({'strike':data[0], 'price':data[1], 'flag':data[2], 'maturity':data[3]}) 
df.to_csv('options.csv', index=False, encoding='utf-8')
