from soupclass8 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import sys, re
import time
#example of code

text_cred = text_l('C:\\Users\\Owner\\Documents\\Important\\catcred.txt')
class Cat_session(object):#parent class for this pseudo-API
	def __init__(self, *args):
		#self.username = input('Username:') 
		#self.password = getpass.getpass('Password:')
		self.username = text_cred[0]
		self.password = text_cred[1]
		self.driver = webdriver.Firefox()
		#in the future allow the user to select which browser to use (would need to make this a child of a parent that did that)
		#self.driver = webdriver.PhantomJS()
		self.args = args
	def main(self):
		terminate = ['Log off','Logout', 'Exit']
		self.session_start()
		data = ''
		#return self.driver
		while data not in terminate:
			data = input('>>')
			self.interpreter(data)
	def source(self):
		return bs(self.driver.page_source, 'lxml')


	def start(self):#login method
		self.driver.get('https://accounts.crystalcommerce.com/users/sign_in')
		element = self.driver.find_element_by_id('user_email')
		element1 = self.driver.find_element_by_id('user_password')
		element.send_keys(self.username)
		element1.send_keys(self.password)
		element3 = self.driver.find_element_by_name('commit')# sign in button
		element3.click()
		self.target()
		return self.driver
	def target(self):
		element = self.driver.find_element_by_link_text('Catalog')
		element.click()
		if self.driver.current_url == 'https://catalog.crystalcommerce.com/users/login':#checks to see if it got kicked back
			element_1 = self.driver.find_element_by_class_name('sinewave-button')
			element_1.click()

		else:
			return self.driver
	def cat_grab(self):#untested
		#grabs all the current categories
		self.driver.get('https://catalog.crystalcommerce.com/categories')
		element_1 = self.driver.find_element_by_link_text('New Category')
		element_1.click()
		return self.driver

	def push_skus(self,x):
		self.cat_goto(x)
		try:
			checkbox = self.driver.find_element_by_id('all_products')
			#all_in_checkbox = self.driver.execute_script('return document.getElementById("product_variation_category_id").click()')
			checkbox.click()
			self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		except:
			print("Something went wrong")
		self.b_grab('btn btn-info','value', 'Push Skus to Clients').click()

	def push_asins(self,x):
		self.cat_goto(x)
		try:
			checkbox = self.driver.find_element_by_id('all_products')
			checkbox.click()
			self.driver.execute_script('document.getElementById("product_variation_category_id").click()')
		except:
			print("Something went wrong.")
		self.b_grab('btn btn-info', 'value', 'Push ASINs to Clients').click()

	def push_asins_cc(self, x):
		#pushes ASINs for all child categories underneath a specified parent category (x)
		self.cat_goto(x)
		children = self.child_cats()
		for i in range(0, len(children)):
			self.push_asins(children[i])

	def push_skus_cc(self, x):
		#pushes skus for all child categories underneath a specified parent category (x)
		self.cat_goto(x)
		children = self.child_cats()
		for i in range(0, len(children)):
			self.push_skus(children[i])

	def move_cat(self, x, target_cat):
		#moves a single item to a different category
		self.prod_go_to(x + '/edit')
		categories = self.driver.execute_script('document.getElementsByClassName("select required select2 wide-category-select")[0].children')
		#clicks on the drop down menu
		self.driver.execute_script('document.getElementsByClassName("select2-offscreen select2-focusser")[0].click();')
		#once the menu has been clicked the options are now visible 



	def prod_go_to(self, x):
		try:
			int(x)
		except ValueError as VE:
			return "{0} must be an integer".format(x)


		url = 'https://catalog.crystalcommerce.com/products/' + str(x)
		self.driver.get(url)


	def cat_find(self, x):
		categories = self.driver.execute_script('return document.getElementsByClassName("select required select2 wide-category-select")[0].children')
		for i in range(0, len(categories)):
			cat = categories[i].get_attribute('value')
			if x == cat:
				name = self.driver.execute_script('return document.getElementsByClassName("select required select2 wide-category-select")[0].children[%s].innerHTML;' % str(i))
				return name
		return
	def delete_product_single (self, x):
		self.prod_go_to(x)
		start = self.driver.current_url
		#ideally this function would store a temporary copy of the item in order to aid in
		#the recovery of items that were deleted by mistake
		self.driver.execute_script('''
			var items = document.getElementsByClassName('btn btn-danger');
			for (i = 0 ; i < items.length ; i++){
				if (items[i].innerHTML.contains('Delete')){
					items[i].click();
				}
			}


			''')
		try:
			self.driver.switch_to_alert().accept()
		except:
			return (x, False)
		while self.driver.execute_script('return document.readyState') != "complete" and self.driver.current_url == start:
			time.sleep(.5)
		print("Successfully deleted {0}".format(x))
		return x




	def descriptor_get(self, x):
		d_info = {}
		#retrieves the descriptors and their current values for a single product given its url or its product number
		try:
			int(x)
		except ValueError as VE:
			#if the argument is the full url (sans the '/edit' )
			url = x + '/edit'
			self.prod_go_to(url)
		else:
			url = 'https://catalog.crystalcommerce.com/products/' + str(x) + '/edit'
			self.prod_go_to(url)

		elements = driver.self.execute_script("return document.getElementsByClassName('control-group string optional product_product_descriptors_value')")
		d_element = "document.getElementsByClassName('control-group string optional product_product_descriptors_value')"
		d_num = driver.self.execute_script("return document.getElementsByClassName('control-group string optional product_product_descriptors_value')[0].children.length")
		for i in range(0, int(d_num) - 1):
			name = driver.self.execute_script("return document.getElementsByClassName('control-group string optional product_product_descriptors_value')[%s].children[0].innerHTML;" % str(i))
			d_info[name] = driver.self.execute_script("return document.getElementsByClassName('control-group string optional product_product_descriptors_value')[%s].children[1].value;" % str(i))
		return d_info





	def descriptor_edit(self, x):
		pass
		








	def b_grab(self, t_class, attribute, value): 
		#allows you to select a specific button given its class, attribute and that attribute's value
		items = self.driver.execute_script('return document.getElementsByClassName(%s)' % ('"' + t_class + '"'))
		if items == []:
			return "None found"
		for i in range(0, len(items)):
			r_value = items[i].get_attribute(attribute)
			if r_value == value:
				return items[i]
		return

	def child_cats(self):
		site = self.source()
		target = site.find('h3').find_next()
		links_r = S_table(target).table_eater_exp('a',1,3)
		new = [fn_grab(S_format(str(links_r[i])).linkf('<a href=')) for i in range(0, len(links_r))]
		return new










	def cat_goto(self, cat_number):
		self.driver.get('https://catalog.crystalcommerce.com/categories/' + cat_number) #goes to the category
		return self.driver
	def prod_s_cat(self,prod_name):#search within a given category once the driver is "parked" in the category
		element_1 = self.driver.find_element_by_id('product_search_name_cont')
		element_1.send_keys(prod_name)#puts product name in the search field
		element_1.send_keys(Keys.RETURN)




	def cat_s(self, cat_name):#searches for a category (cat_name)
		element_1 = self.driver.find_element_by_link_text('Categories')#
		element_1.click()
		element_2 = self.driver.find_element_by_id('categories_search_q')
		element_2.send_keys(cat_name)#puts cat_name into the search box
		element_2.send_keys(Keys.RETURN)#using keystroke key in order to avoid accidently clicking other buttons (in case they change in the future)
		return self.driver
	def prod_s(self, prod_name):
		element_1 = self.driver.find_element_by_name('q[name_cont]')
		element_1.send_keys(prod_name)
		element_1.send_keys(Keys.RETURN)
		return self.driver
	def prod_s_ADV(self, prod_name, *args):#advanced search feature, will be improved in the future
		pass

class S_results(object):#should probably be made a child of Cat_session once it is completed
	def __init__(self, site):#takes a webdriver object as site, calls its page_source method and then parses it through bs
		self.site = site.source() #turns the source into bsObject
		self.bsObject = bs(self.site, 'lxml') 


	def table_results_s(self):#returns the results on a singles results page in the catalog
		table = self.bsObject.find('table', {'class': 'table table-striped'})
		rows = table.find_all('tr', {'class':'product'})
		return rows #
	def cat_grab(self):#untested
		cats_cont = self.bsObject.find('select',{'id':'category_parent_id'})
		cats = cats_cont.find_all('option')
		new = [(S_format(str(cats[i])).linkf('<option value='), cats[i].text) for i in range(0, len(cats))]
		#new should be a list of tuples containin the category ID and the category name
		return new




class Cat_product_add(object):
	def __init__(self, session):
		self.session = session
	#need add_to_cat_single and add_to_cat_batch
	def add_prod_cat_def(self, target_cat, attrs, image_folder="C:\\Users\\Owner\\Desktop\\I\\"):
		#adds a single product to a single category (id)
		def_image = "C:\\Users\\Owner\\Desktop\\I\\Card Backs & Logos\\no-image.jpg"
		assert type(target_cat) == int, "{0} must be int".format(target_cat)
		assert type(attrs) == dict, "{0} must be dict".format(attrs)
		self.session.get("https://catalog.crystalcommerce.com/categories/{0}".format(target_cat))
		self.session.execute_script(
			'''
			var f = document.getElementsByClassName('control-group')[0];
			for (i = 0 ; i < f.children.length ; i++){
			if (f.children[i].innerHTML == "New Product"){
      			f.children[i].click();
			}
			else{
    			console.log("DID NOT FIND IT");
			}}'''
			)
		start = self.session.current_url
		
		keys = list(attrs.keys())
		if "Product Name" not in keys:
			raise Crit_not_present("Product Name desciptor not found")
		if "Category" not in keys:
			raise Crit_not_present("Category id not present")
		self.crit_find("Product Name", attrs["Product Name"])
		#product name must be added first in order to prevent it from being overridden by unneccessary/improper descriptors (e.g. "Name")

		for i in range(0, len(keys)):
			if keys[i] != "Category" or keys[i] != "Product Name":
				self.crit_find(keys[i], attrs[keys[i]])
		#need to add image loader here
		photo_name = attrs.get('Product Image', def_image)
		b_list = [def_image, '']
		if photo_name not in b_list:
			photo_path = image_folder + photo_name
			check = self.add_image(photo_path)
			if not check:
				attrs['Photo Present'] = 0
			else:
				attrs['Photo Present'] = 1
		



		self.session.execute_script(
			'''
			var items = document.getElementsByTagName('*');
			for (i = 0; i < items.length ; i++){
   					if ( items[i].value == "Create Product"){
        			var result = items[i] ;
        			result.click();
			}}''')
		while self.session.execute_script('return document.readyState') != "complete" and self.session.current_url == start:
			time.sleep(.5)
			#needs exception handling in order to catch any kickback from server regarding duplicate barcodes and/or ASINs
		final_url = self.session.current_url
		product_id = fn_grab(final_url)
		attrs["Product Id"] = product_id
		print(attrs)#only for testing
		return attrs
	def add_prod_cat_batch(self, fname):
		results = []
		failure_list = []
		items = dictionarify(fname)
		for i in range(0, len(items)):
			try:
				confirm = self.add_prod_cat_def(int(items[i]['Category']), items[i])
			except:
				print("ERROR HAS OCCCURED")
				failed_item = S_format(items[i]).d_sort()
				failure_list.append(failed_item)

			else:
				results.append(list(confirm.values())) 
				#for testing only, ideally this should make an entry into a database
		w_csv(results, 'batch_create.csv')
		if failure_list != []:
			print("Some items were not added due to errors. Please see fail_file.csv for more")
			w_csv(failure_list, "fail_file.csv")
		return results
	def add_image(self, image_name):
		try:
			photo_element = self.session.find_element_by_id('product_photo')
		except:
			return False
		photo_element.send_keys(image_name)
	def update_image(self, prod_id, image_name):
		assert type(prod_id) == int, "Product Id must be int"
		start = self.session.current_url
		url = 'https://catalog.crystalcommerce.com/products/' + str(x) + '/edit'
		self.session.get(url)
		while load_check(start):
			time.sleep(.3)
		self.add_image(image_name)

	def load_check(self, start):
		#takes initial url (url of page before request) as argument

		if self.session.execute_script('return document.readyState') != "complete" and self.session.current_url == start:
			return True
		else:
			return False


	def crit_find(self, crit, value):
		#should use a function in the future
		#also needs exception handling
		value = re.sub("'", "\\\'",  value)
		value = re.sub('"', '\\\"', value)

		command = '''
			var items = document.getElementsByTagName('label');
			for (i = 0; i < items.length; i++){{
				var ind_item  = items[i].innerHTML;
				if (ind_item.includes('{0}') && items[i].nextElementSibling.children[0].value == '') {{
					items[i].nextElementSibling.children[0].value = '{1}' ; 
				}}
				}}
			'''.format(crit, value)
		self.session.execute_script(command)





		#clicks the "New Product" button
test_d = {"Product Name":'  Captain America - 1', "MSRP":'5.99', 'Barcode/UPC': '1337', 'Manufacturer SKU':'TEST 01', 'Category': 22054}



def dictionarify(x):
	#should produce list of dictionaries from a csv, with the column headers as the keys
	item = C_sort(x)
	items = item.contents
	crit = item.contents[0]
	results = []
	for i in range(1, len(items)):
		d = dict.fromkeys(crit, 0)
		for i_2 in range(0, len(items[i])):
			d[crit[i_2]] = items[i][i_2]
		results.append(d)
	return results



test_inst = Cat_session()
test_inst.start()
time.sleep(5)
#test_inst.delete_product_single(6317013)
test_add = Cat_product_add(test_inst.driver)
#time.sleep(2)
#test_add.add_prod_cat_def(21333, test_d)
#test_add.add_prod_cat_batch('test_csv.csv')




if len(sys.argv) > 1:
	if sys.argv[1] == '-t':
		print(sys.argv[2])
		splitter(sys.argv[2])
	elif sys.argv[1] == '-s':
		main_imp(sys.argv[2],sys.argv[3])
else:
	print("[data]")



class Crit_not_present(Exception):
	pass




def j_script(x,target, atr_val):

			'''

			for (i = 0 ; i < f.children.length ; i++){
			if (f.children[i]. == "New Product"){
      			f.children[i].click();
			}
			else{
    			console.log("DID NOT FIND IT");
			}}'''
			
		
