########library#######
import os
import time
from selenium import webdriver
import requests
###########library#########

def scroll_to_end(wd):
    wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


def retrieve_image_url(search:str, max_links:int,wd:webdriver,sleep_bw_interact:float=1):

    #output set of image urls
    img_urls=set()

    google_img_url='https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img'
    #print('final_url_to_search- ',google_img_url.format(q=search))

    #time to get the page
    wd.get(google_img_url.format(q=search))
    img_count=0
    start_ind=0
    while_loop=0
    while img_count < max_links:
        while_loop+=1
        print('count started: ', while_loop)
        thumbnails=wd.find_elements_by_css_selector('img.Q4LuWd')
        scroll_to_end(wd)
        print('thumbnails found ',len(thumbnails))
        results_found=len(thumbnails)
        print('start with: {a} and end with : {b} '.format(a=start_ind,b=results_found))
        for i in thumbnails[start_ind:results_found]:
            try:
                i.click()
                time.sleep(sleep_bw_interact)
            except Exception as e:
                print(e,'while doing thumbnail click')
                continue

            #after click extract image url
            actual_img=wd.find_elements_by_css_selector('img.n3VNCb')
            for j in actual_img:
                if j.get_attribute('src') and 'http' in j.get_attribute('src'):
                    img_urls.add(j.get_attribute('src'))

            img_count = len(img_urls)
            if img_count >= max_links:
                print('got enough links ',img_count)
                break
        start_ind=len(thumbnails)


    return img_urls

def persist_image(url:str,folder_path,counter:int,search:str):
    img=requests.get(url).content
    path='null'
    if not os.path.exists(os.path.join(folder_path,search)):
        os.mkdir(os.path.join(folder_path,search))
        path=os.path.join(folder_path,search)
        f = open(os.path.join(path, 'JPG' + '_' + str(counter) + '.jpg'), 'wb')
        f.write(img)
        f.close()
    else:
        path=os.path.join(folder_path,search)
        f = open(os.path.join(path, 'JPG' + '_' + str(counter) + '.jpg'), 'ab')
        f.write(img)
        f.close()





executable_path='./chromedriver'
image_path='./images'
search=input('enter the search string ')
images_count=int(input('enter the no of images '))
with webdriver.Chrome(executable_path=executable_path) as wd:
    result_url=retrieve_image_url(search=search,max_links=images_count,wd=wd,sleep_bw_interact=5)
    count=0
    for i in result_url:
        persist_image(i,image_path,count,search)
        count+=1

''''
search='dogs'
google_img_url='https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img'
wd= webdriver.Chrome(executable_path='./chromedriver')
wd.get(google_img_url.format(q=search))
count=0
thumbnails=0
while True:
    count+=1
    thumbnails = wd.find_elements_by_css_selector('img.Q4LuWd')
    print('count for {a} thumbnails are {b}'.format(a=count,b=len(thumbnails)))
    scroll_to_end(wd)
    if(len(thumbnails)>=100):
        try:
            thumbnails[5].click()
            time.sleep(0.4)
        except:
            thumbnails[20].click()
            time.sleep(0.5)
        actual_img = wd.find_elements_by_css_selector('img.n3VNCb')
        for j in actual_img:
            if j.get_attribute('src') and 'http' in j.get_attribute('src'):
                print(j.get_attribute('src'))
    load_more_button = wd.find_element_by_css_selector(".mye4qd")
    if load_more_button:
        wd.execute_script("document.querySelector('.mye4qd').click();")

    if(len(thumbnails)==1000):
        break

'''''











