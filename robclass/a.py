from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('disable-infobars')
driver = Firefox(executable_path='geckodriver', firefox_options=chrome_options)
url = 'https://mis.bjtu.edu.cn/home/'
driver.get(url)