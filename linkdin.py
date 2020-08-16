from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector
import csv


def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field


file_name = 'Linkedin_lead.csv'
writer = csv.writer(open(file_name, 'w'))
writer.writerow(['Name', 'Job Title', 'School', 'Location', 'URL'])

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options, executable_path=r'E:\selenium\chromedriver.exe')

driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys('alamin493641@gmail.com')
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys('!1@2#3qw')
sleep(0.5)

sign_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
sign_in_button.click()
sleep(5)
for i in range(10):
    driver.get('https://www.bing.com/')
    sleep(3)

    search_query = driver.find_element_by_name('q')
    search_query.send_keys('site:linkedin.com/in/ AND "python developer " and "london"' + 'page' + str(i))

    search_query.send_keys(Keys.RETURN)
    sleep(3)

    linkedin_urls = driver.find_elements_by_tag_name('cite')
    linkedin_urls = [url.text for url in linkedin_urls]
    sleep(0.5)

    for linkedin_url in linkedin_urls:
        driver.get(linkedin_url)
        sleep(5)
        linkedin_url = driver.current_url

        sel = Selector(text=driver.page_source)

        name = sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[1]/li[1]/text()').extract_first()
        if name:
            print('Name: ' + name)

        job_title = sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/h2/text()').extract_first()
        if job_title:
            print('Job_Title: ' + job_title)

        school = sel.xpath('//*[@id="ember97"]/text()').extract_first()
        if school:
            school = school.strip()
            print('School: ' + school)

        location = sel.xpath('//*[@id="ember51"]/div[2]/div[2]/div[1]/ul[2]/li[1]/text()').extract_first()
        if location:
            print('Location: ' + location)

        print(linkedin_url)

        linkedin_url = driver.current_url

        name = validate_field(name)
        job_title = validate_field(job_title)
        school = validate_field(school)
        location = validate_field(location)
        linkedin_url = validate_field(linkedin_url)

        writer.writerow([name.encode('utf-8'),
                         job_title.encode('utf-8'),
                         school.encode('utf-8'),
                         location.encode('utf-8'),
                         linkedin_url.encode('utf-8')])

        try:
            driver.find_element_by_xpath('//span[text()="Connect"]').click()
            sleep(3)

            driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click()
            sleep(3)

        except:
            pass

driver.quit()
