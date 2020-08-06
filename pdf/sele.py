from selenium import webdriver
driver=webdriver.Chrome("./chromedriver.exe")
with open("book.txt",'r')as f :
    ls=f.readlines()
    for url in ls:
        driver.get(url)
