# import libraries 
import pandas as pd
import time, urllib.request
from urllib.request import urlopen
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#chromedriver in the same folder
chrome_path = "chromedriver.exe"

#customize options
custom_options = webdriver.ChromeOptions()

# translate the site into english 
prefs = {
    "translate_whitelists": {"ru": "en"},
    "translate": {"enabled":"true"}
}
custom_options.add_experimental_option("prefs", prefs)
driver=webdriver.Chrome(chrome_path, options=custom_options)
time.sleep(5)

# the actual link for the site 
driver.get("https://wiki.mipt.tech/index.php/")


#our file will contain the following fields from the table 
field_names = ["Faculty", "Full Name", "Date of Birth", "Alma mater", "Academic degree", "Works",
               "Leads", "Knowledge", "Ability to teach", "In communication",'"Free"', 'Overall rating']


# new csv file with headings empty file 
def empty_csv_heading(file_name):
    file_path = "./"+file_name+".csv"
    if(os.path.isfile("file_path")==False):
        with open(file_path,"w+") as f:
            data = ",".join(field_names)
            f.write(f"{data}\n")


# writing data to csv file 
def data_to_csv(data):
    file_path = "./"+file_name+".csv"
    for value in data:
        data[value] = [data[value].replace("\n"," ")]
    #dataframe 
    df = pd.DataFrame(data)
    # append data frame to CSV file
    df.to_csv(file_path, mode='a', index=False, header=False)
    
    print(data["Full Name"],"\tData is collected and saved to file\t",file_path)

# Get faculty names from the main page 
def get_faculty_name_and_links():
    time.sleep(2)
    faculty_names = []
    faculty_links = []
    faculty = driver.find_element_by_xpath('//div[@style="column-count: auto; column-width: 21rem;"]')
    faculty_data = faculty.find_elements_by_tag_name("a")

    for fac in faculty_data:
        faculty_names.append(fac.text)
        faculty_links.append(fac.get_attribute("href"))
    
    return({"names":faculty_names, "links":faculty_links})

# Get teacher names in the faculty list 
# Different faculties with different teachers (xpath)
def get_teachers_name_and_links(subject_link):
    driver.get(subject_link)
    time.sleep(1)
    teacher_names = []
    teacher_links = []
    driver.get(subject_link)
    # xpath for different faculties 
    teachers_data = driver.find_element_by_xpath('//div[@style="-moz-column-count:3; column-count:3; -webkit-column-count:3" or @class="srf-gallery srf-redirect"]')
    # embeded in tag "a"
    teachers_links = teachers_data.find_elements_by_tag_name("a")
    for teach in teachers_links:
        teacher_names.append(teach.text)
        teacher_links.append(teach.get_attribute("href"))
    return({"names":teacher_names, "links":teacher_links})

# collecting data from the table about the teachers from wiki card 
def collect_data_from_table(teacher):
    driver.get(teacher)
    time.sleep(1)
    wiki_card = driver.find_element_by_xpath('//table[@class="wikitable card"]')
    table_row = wiki_card.find_elements_by_tag_name("tr")
    row_heading = dict(zip(field_names, [""]*len(field_names)))
    for row_data in table_row:
        #time.sleep(2)
        try:
            reviews = row_data.find_elements_by_tag_name("table")
            if(len(reviews)>0):
                collect_reviews(row_heading,reviews)
                break
            row_h = row_data.find_element_by_tag_name("th").text
            if(row_h in row_heading.keys()):
                row_d = row_data.find_element_by_tag_name("td")
                row_heading[row_h] = row_d.text
        except:
            continue
    return row_heading


# collect ratings about teachers from the table 
def collect_reviews(info,reviews):
    reviews_table= reviews[1].find_elements_by_tag_name("tr")
    time.sleep(2)
    for row_data in reviews_table:
        #time.sleep(2)
        # ratings under ratingsinfo class 
        try:
            row_h = row_data.find_element_by_tag_name("td").text
            if(row_h in info.keys()):
                row_d = row_data.find_element_by_class_name("ratingsinfo-avg")
                info[row_h] = row_d.text
        except:
            continue
    print(info)




# Writing everything into the csv file 
file_name = input("What is the file name where you want store data: ")
empty_csv_heading(file_name)

faculty_names_links = get_faculty_name_and_links()
for i in range(len(faculty_names_links["links"])):
    try:
        # faculty 
        print(faculty_names_links['names'][i]," Data is collecting \n*****")
        teacher_names_and_links = get_teachers_name_and_links(faculty_names_links["links"][i])
        for j in range(len(teacher_names_and_links["links"])):
            try:
                # teachers 
                print(teacher_names_and_links["names"][j],"Data collection is in progress...\n*****")
                main_data = collect_data_from_table(teacher_names_and_links["links"][j])
                main_data['Faculty'] = faculty_names_links['names'][i]
                main_data['Full Name'] = teacher_names_and_links["names"][j]
                data_to_csv(main_data)
            except:
                print("Data is not avaiable")
                continue
    except:
        # Break if need to collect only some faculty information 
        print("Data cannot be found")
        choice = input("To continue press Y, to stop any key : ")
        if(choice!='y' or choice!='Y'):
            break
    choice = input("To continue press Y, to stop any key : ")
    if(choice!='y' or choice!='Y'):
        continue 

# the scrapped data is saved in data.csv 