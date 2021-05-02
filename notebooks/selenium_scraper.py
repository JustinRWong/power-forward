from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

class WebDriver:

	location_data = {}

	def __init__(self):
		# self.PATH = "chromedriver.exe"
		self.options = Options()
		# self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
		self.options.add_argument("--headless")
		self.driver = webdriver.Chrome()

		self.location_data['address'] = []
		self.location_data["rating"] = "NA"
		self.location_data["reviews_count"] = "NA"
		self.location_data["location"] = "NA"
		self.location_data["contact"] = "NA"
		self.location_data["website"] = "NA"
		self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
		self.location_data["Reviews"] = []
		self.location_data["Popular Times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}

	def click_open_close_time(self):

		if(len(list(self.driver.find_elements_by_class_name("cX2WmPgCkHi__section-info-hour-text")))!=0):
			element = self.driver.find_element_by_class_name("cX2WmPgCkHi__section-info-hour-text")
			self.driver.implicitly_wait(5)
			ActionChains(self.driver).move_to_element(element).click(element).perform()

	def click_all_reviews_button(self):

		try:
			WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "allxGeDnJMl__button")))

			element = self.driver.find_element_by_class_name("allxGeDnJMl__button")
			element.click()
		except:
			self.driver.quit()
			return False

		return True

	def get_location_data(self):

		try:
			avg_rating = self.driver.find_element_by_class_name("section-star-display")
			total_reviews = self.driver.find_element_by_class_name("section-rating-term")
			address = self.driver.find_element_by_css_selector("[data-item-id='address']")
			phone_number = self.driver.find_element_by_css_selector("[data-tooltip='Copy phone number']")
			website = self.driver.find_element_by_css_selector("[data-item-id='authority']")
		except:
			pass
		try:
			self.location_data["rating"] = avg_rating.text
			self.location_data["reviews_count"] = total_reviews.text[1:-1]
			self.location_data["location"] = address.text
			self.location_data["contact"] = phone_number.text
			self.location_data["website"] = website.text
		except:
			pass


	def get_location_open_close_time(self):

		try:
			days = self.driver.find_elements_by_class_name("lo7U087hsMA__row-header")
			times = self.driver.find_elements_by_class_name("lo7U087hsMA__row-interval")

			day = [a.text for a in days]
			open_close_time = [a.text for a in times]

			for i, j in zip(day, open_close_time):
				self.location_data["Time"][i] = j

		except:
			pass

	def get_popular_times(self):
		try:
			a = self.driver.find_elements_by_class_name("section-popular-times-graph")
			dic = {0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
			l = {"Sunday":[], "Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[]}
			count = 0

			for i in a:
				b = i.find_elements_by_class_name("section-popular-times-bar")
				for j in b:
					x = j.get_attribute("aria-label")
					l[dic[count]].append(x)
				count = count + 1

			for i, j in l.items():
				self.location_data["Popular Times"][i] = j
		except:
			pass

	def scroll_the_page(self):
		try:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))

			pause_time = 2
			max_count = 5
			x = 0

			while(x<max_count):
				scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
				try:
					self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
				except:
					pass
				time.sleep(pause_time)
				x=x+1
		except:
			self.driver.quit()

	def expand_all_reviews(self):
		try:
			element = self.driver.find_elements_by_class_name("section-expand-review")
			for i in element:
				i.click()
		except:
			pass

	def get_address(self):
		try:
			add = self.driver.find_elements_by_css_selector("[class='section-result-description']")
			print('Result from driver')
			print(add)
			add_final = []

			for i in add:
				print(i)
				add_final.append(i.text)
				self.location_data['address'].append(i.text)
			return add_final
		except Exception as e:
			pass

	def scrape(self, url):
		while True:
			with open("dataFile.txt","w") as f:
				try:
					self.driver.get(url)
				except Exception as e:
					self.driver.quit()
					continue
				time.sleep(10)

				print('Trying to get address')
				self.get_address()
				print('FInished to get address')
				if(self.click_all_reviews_button()==False):
					continue
				time.sleep(5)
				self.scroll_the_page()
				self.expand_all_reviews()
				self.get_reviews_data()
				self.driver.quit()

				for addy in self.location_data['address']:
					f.write(addy +"\n")
				return(self.location_data)

url = "https://www.google.com/maps/search/ev+charging+stations/@37.6629515,-122.4343552,12z/data=!3m1!4b1"
x = WebDriver()
print(x.scrape(url))
