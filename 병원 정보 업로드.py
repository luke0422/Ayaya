from selenium import webdriver
import pyrebase
import json

hospital_list = []
hospital_path="Hospitals"

def crawling(department):
    hospital_list = []
    global hospital_path

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    
    driver = webdriver.Chrome(options=options)
    url = 'https://www.naver.com/'
    driver.get(url)

    elem1 = driver.find_element_by_id('query')
    elem1.send_keys('송도 ' + department)

    elem2 = driver.find_element_by_id('search_btn')
    elem2.click()

    elem3 = driver.find_elements_by_class_name('QLp9G')
    elem3_2=driver.find_elements_by_class_name('_3Apve')

    for i in elem3:
        hospital_list.append(i.text)
    for i in elem3_2:
        hospital_list.append(i.text)

    for i in hospital_list:
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        driver = webdriver.Chrome(options=options)
        
        url = 'https://www.naver.com/'
        driver.get(url)

        elem1 = driver.find_element_by_id('query')
        elem1.send_keys('송도 ' + i)

        elem2 = driver.find_element_by_id('search_btn')
        elem2.click()

        elem3 = driver.find_elements_by_class_name('_1mAZf')

        x = []
        cnt = 0
        for j in elem3:
            phone_number = ''
            if cnt == 2:
                break
            elif cnt == 0:
                for m in j.text:
                    if m in '0123456789-':
                        phone_number += m
                x.append(phone_number)
                cnt+=1
            else:   
                x.append(j.text.replace(" ","_"))
                print(j.text)
                cnt+=1
                
        db.child(hospital_path).child('{}/info'.format(i)).set(x)
        db.child(hospital_path).child('{}/rating'.format(i)).set(['3','1'])
        db.child(hospital_path).child('{}/rating/user/none'.format(i)).set('none')

def main():
    global hospital_path


    #department_list=['안과','이비인후과','내과','신경외과','정형외과','피부과','항문외과']
    department_list=['치과']

    for i in range(len(department_list)):
        hospital_path="Hospitals/{}".format(department_list[i])
        crawling(department_list[i])
    '''  
    if answer == 1:
        hospital_path+="/안과"
        crawling('안과')
    elif answer == 2:
        hospital_path+="/이비인후과"
        crawling('이비인후과')
    elif answer == 3:
        hospital_path+="/내과"
        crawling('내과')
    elif answer == 4:
        hospital_path+="/신경외과"
        crawling('신경외과')
    elif answer == 5:
        hospital_path+="/정형외과"
        crawling('정형외과')
    elif answer == 6:
        hospital_path+="/피부과"
        crawling('피부과')
    elif answer == 7:
        hospital_path+="/항문외과"
        crawling('항문외과')
    '''

with open('ayaya.json') as f:
    config = json.load(f)

firebase = pyrebase.initialize_app(config)
db = firebase.database()

main()
