# import webdriver
from selenium import webdriver

# create webdriver object
driver = webdriver.Firefox()

# get geeksforgeeks.org
driver.get("https://www.geeksforgeeks.org/")

# get element
element = driver.find_element_by_xpath('/html/body/div[1]/div[4]/button[1]')

# get text_length property
res = element.get_property("previousElementSibling")
# print(res)
print(res == None)
