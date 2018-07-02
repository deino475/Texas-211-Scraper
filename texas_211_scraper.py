from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import json

#This class is a struct for maintaining the organization data
class Organization:
	def __init__(self):
		self.name = "Name Not Available"
		self.eligibility = "Eligibility Requirements Not Available"
		self.location = "Location Not Available"
		self.phone = "Phone Number Not Available"
		self.program_hours = "Schedule Not Available"
		self.application_process = "Application Process Not Available"
		self.program_fees = "Program Fees Not Available"
		self.documents_required = "Document Requirements Not Available"
		self.service_area = "Service Area Not Available"

	def __repr__(self):
		data = { 
			'name': self.name, 
			'eligibility': self.eligibility, 
			'location' : self.location, 
			'phone' : self.phone, 
			'program hours' : self.program_hours,
			'application process' : self.application_process,
			'program fees' : self.program_fees,
			'documents required' : self.documents_required,
			'service area' : self.service_area
		}
		
		return str(data)


#This function saves the list of urls to a file
def save_data(list_of_urls):
	with open("texas_211_urls.json", "w") as urls_file:
		json.dump(list_of_urls,urls_file)

#This list stores all of the scraped URLs
urls = [] 

#This list stores all of the search queries we want to use
search_queries = ["housing"]
driver = webdriver.Firefox()

for search_query in search_queries:
	driver.get("http://na1.icarol.info/AdvancedSearch.aspx?org=72605&amp%3bCount=5&amp%3bNameOnly=True&amp%3bpst=Coverage&amp%3bsort=Proximity&amp%3bTaxExact=False&amp%3bCountry=United+States&amp%3bStateProvince=TX&amp%3bCounty=-1&amp%3bCity=-1&amp%3bPostalCode=")
	
	#Sends the search term to 
	driver.find_element_by_name("txtSearch").send_keys(search_query)

	driver.find_element_by_name("btnSearch").click()

	#Gives page time to load content
	time.sleep(25)

	#Searches for text that says "Page X of Y"
	page_count = driver.find_element_by_css_selector(".PagerInfoCell")


	#Sets start to the first numeric value in "Page X of Y"
	start = int(page_count.text.split(" ")[1])

	#Sets end to the second numeric value in "Page X of Y"
	end = int(page_count.text.split(" ")[3])

	#Sets a main window for reference
	main_window = driver.current_window_handle

	while start <= end:
		#List of all links on the page
		links = driver.find_elements_by_tag_name('a')
		for link in links:

			#Checks to see if the link grabbed was the 
			if link.get_attribute('id')[0:19] == "rptSearchResults_A2":
				#Grabs the link's ID
				link_id = link.get_attribute('id')

				#Sends javascript command to scroll the link into view for Selenium
				command = 'var mylink = document.getElementById("' + link_id + '"); mylink.scrollIntoView();'
				driver.execute_script(command)

				#Clicks the link
				link.click()

				#Focuses the driver on the correct tab to send commands to 
				driver.switch_to.window(driver.window_handles[0])
				time.sleep(3)
				driver.switch_to.window(driver.window_handles[-1])

				#Waits for the page's content to load
				time.sleep(12)

				#Scrapes Information
				data_url = driver.find_element_by_id('find_services_frame').get_attribute('src')
				print(data_url)

				#Save information to list
				urls.append(data_url)

				#Closes the opened tab
				driver.execute_script('window.close();')

				#Refocuses driver on correct tab
				driver.switch_to.window(main_window)

		#This selects the last pagination link and clicks it
		driver.find_elements_by_css_selector(".PagerHyperlinkStyle")[-1].click()

		#Calls function that saves URLs
		save_data(urls)
		
		#Gives time for page to load
		time.sleep(15)
		
		#Increments page by one
		start += 1

driver.close()
