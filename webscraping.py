import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
import time
from requests.api import request

program_run_time = time.time()
# List
job_detials_list = []
job_location_list = []
company_name_list = []
job_title_list = []
job_exp_list = []
link_list = []
Job_Sallary_list = []
job_relased_date_list = []
Job_Description_list = []
Job_Requirements_list = []

#           GUI
# root = tkinter.Tk()
# root.geometry("600x250")
# text_bage_limit = tkinter.Label(root, text="how many bage number u want it", font=(
#     "Arial", 12), background="green").pack()
# bage_limit = tkinter.IntVar()

# bage_limit_input = tkinter.Entry(
#     root, width=4, textvariable=bage_limit).pack()

# get_url = tkinter.StringVar()
# get_url = tkinter.Entry(
#     root, width=4, textvariable=bage_limit).pack()




bage_num = 0
bage_limit = int(input("how many bage number u want : ").strip())+1
get_url = input("enter ur url bage: ")
get_url = get_url[:-2]

while bage_num < bage_limit:

    # الموقع اللي هيتحلل بياناته
    data_url = requests.get(f"{get_url[:-2]}{bage_num}")
    # نحط البيانات من الموقع في فاريبال
    bage_contant = data_url.content
    soup = BeautifulSoup(bage_contant, "lxml")
    # نحط اسماء الوظائف في فاريبال لوحدوا من اسم كود في الhtml اسم الكلاس الخاص بيه
    job_title = soup.find_all("h2", {"class": "job-title"}, "span")
    job_detials = soup.find_all(
        "div", {"class": "job-details"})
    company_name = soup.find_all(
        "span", {"class": "company-name"})
    job_location = soup.find_all(
        "span", {"class": "location-mobile"})
    job_relased_date = soup.find_all(
        "time", {"class": "time1 job-date"})

    for i in range(len(job_location)):
        job_title_list.append(job_title[i].text.strip())

        job_detials_list.append(job_detials[i].text.replace(
            "\n", "").replace("  ", "").strip())
        print(job_detials_list)
        link_list.append(
            job_title[i].find("a").attrs['href'])
        job_relased_date_list.append(
            job_relased_date[i].text.strip())

        job_location_list.append(
            job_location[i].text.strip())

        company_name_list.append(
            company_name[i].text.strip())
    job_detials_list = [i.strip()
                        for i in job_detials_list]
    print("link_list")
    bage_num += 1
    # اخذ بيانات من داخل كل صفحه داخليه
for link in link_list:
    inner_url = requests.get(link)
    inner_data_page = inner_url.content
    inner_soup = BeautifulSoup(inner_data_page, "lxml")
    Job_Requirements = inner_soup.find(
        "div", {"class": "css-1t5f0fr"})
    Job_Requirements = inner_soup.find("ul")
    Job_Requirements_text = "* "
    for dot in Job_Requirements.find_all("li"):
        Job_Requirements_text = Job_Requirements_text + dot.text + "\n* "
    Job_Requirements_text = Job_Requirements_text[:-2]
    Job_Requirements_list.append(Job_Requirements_text)

# كل البيانات تتحط في ليست واحده
file_all_list = [job_title_list, job_location_list, company_name_list,
                 job_detials_list, job_relased_date_list, link_list, Job_Requirements_list]
# تضبيط البيانات اللي في ليست واحده وفردها
file_one_list = zip_longest(*file_all_list)
with open("D:\project\python\jobsheet.csv", "w") as jobsheet:
    wr = csv.writer(jobsheet)
    wr.writerow(["job title", "job location", "compant name",
                 "job details", "job relased date", "link", "Job Requirements"])
    wr.writerows(file_one_list)
print(time.time()-program_run_time)



# get_data = tkinter.Button(root, text="Get Data in Csv file", borderwidth=1,
#                           background="light green", fg="black", command=getdata).pack()
# root.mainloop()

