from selenium import webdriver
from selenium.webdriver.common.keys import  Keys

driver=webdriver.Chrome("./chromedriver.exe")
i=1
with open("cmp.txt","r",encoding="utf8")as f:
    ls=f.readlines()[100*i:100*(i+1)]
    for link in ls:
        link=link.strip().strip("\n")
        print(link)
        driver.get(link)
        driver.find_element_by_css_selector("body").send_keys(Keys.CONTROL +"t");
        p=driver.page_source
        print(p)
        exit()