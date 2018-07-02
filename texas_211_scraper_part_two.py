import json
from bs4 import BeautifulSoup
import requests
import csv

class Organization:
	def __init__(self):
		self.program_name = "Program Name Not Available"
		self.agency_name = "Agency Name Not Available"
		self.program_description = "Description Not Available"
		self.program_website = "Website Not Available"
		self.program_email = "Email Address Not Available"
		self.program_address = "Physical Address Not Available"
		self.program_hours = "Schedule Not Available"
		self.program_ada = "Disability Information Not Available"
		self.program_eligibility = "Eligibility Requirements Not Available"
		self.languages = "Languages Offered Not Available"
		self.application_process = "Application Process Not Available"
		self.documents_required = "Documents Not Available"
		self.fee_structure = "Fee Structure Not Available"
		self.coverage_area = "Coverage Area Not Available"

	def export(self):
		return [self.program_name, self.agency_name, self.program_description, self.program_website, 
		self.program_email, self.program_address, self.program_hours, self.program_ada, self.program_eligibility,
		self.languages, self.application_process, self.documents_required, self.fee_structure, self.coverage_area]

organizations_list = []

print("Start Scraping")

with open('texas_211_urls.json') as file_to_read:
	list_of_urls = json.load(file_to_read)
	for url in list_of_urls:
		r = requests.get(url)
		page_text = r.text 
		soup = BeautifulSoup(page_text)
		new_organization = Organization()
		try:
			new_organization.program_name = soup.find(id="lblTitle").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.agency_name = soup.find(id="hlLinkToParentAgency").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_description = soup.find(id="lblAgencyDescription").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_website = soup.find(id="lblAgencyWebsite").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_email = soup.find(id="lblAgencyEmailAddress").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_address = soup.find(id="lblAgencyPhysicalAddress").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_hours = soup.find(id="lblAgencyHours").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_ada = soup.find(id="lblDisabilitiesAccess").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.program_eligibility = soup.find(id="lblEligibility").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.languages = soup.find(id="lblLanguagesOffered").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.application_process = soup.find(id="lblApplicationProcess").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.documents_required = soup.find(id="lblDocumentsRequired").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.fee_structure = soup.find(id="lblFeeStructure").getText().encode('utf-8').strip()
		except:
			pass
		try:
			new_organization.coverage_area = soup.find(id="lblCoverageArea").getText().encode('utf-8').strip()
		except:
			pass

		organizations_list.append(new_organization.export())
print("Finished Scraping")
print("Start Saving Data")


with open('211_texas_data.csv','w') as file_to_write:
	csv_writer = csv.writer(file_to_write)
	for row in organizations_list:
		csv_writer.writerow(row)


print("Finished Saving Data")


		
