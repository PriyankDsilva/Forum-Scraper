from lxml import html
import requests
from bs4 import BeautifulSoup
import re,os
import codecs


Flag=True
url=r'https://forums.getpebble.com/categories/general-discussion'

PostCount=1

while (Flag == True and PostCount <=200):
#while (Flag == True ):
    #print('Topi URL :',url)
    print(url,'<-Topic Url\tPosts->',PostCount)
    app_page_data=requests.get(url)
    soup = BeautifulSoup(app_page_data.content, "lxml")

    for link in soup.find_all("div",class_="Title"):
        try:
            PostName=link.a.text
            PostUrl=link.a.get("href")
            #print("Creating Review Scrape file . . .")
            #file_name=link.a.text.strip('\n')
            file_name=re.sub('[^A-Za-z0-9]+', ' ', PostName)
            review_file=r'./'+file_name+'.txt'
            #print(review_file)

            #f=open(review_file,'w')
            f = codecs.open(review_file, 'w', encoding='utf8')
            f.write("Topic :"+link.a.text.strip('\n')+"\n")
            f.write("URL :"+link.a.get("href")+"\n")
            f.write("Comments : \n")

            #Loop for reviews
            ReviewCount=0
            ReviewFlag=True

            while (ReviewFlag == True):
                #print('Debug...')
                app_page_data=requests.get(PostUrl)
                soup2 = BeautifulSoup(app_page_data.content, "lxml")
                for link2 in soup2.find_all("div",class_="Message"):
                    try:
                        ReviewCount+=1
                        f.write(link2.text)
                    except Exception as e:
                        f.write("Unable to get comments due to error :" + e)
                        #print(e)


                EntryFlag=True
                for link in soup2.find_all("a",class_="Next"):
                    EntryFlag=False
                    #print("for loop...")

                    if link.text == "»":
                        #print("Next Page Found . . .")
                        PostUrl=link.get("href")
                        ReviewFlag=True
                        break
                    else:
                        #print("No Page Found")
                        ReviewFlag=False

                if EntryFlag == True:
                    ReviewFlag=False

            print(PostName,'<-Post\tReplies->',ReviewCount)
            #f.close()
            #print(PostCount)
            PostCount+=1


        except Exception as e:
            print(e)

    EntryFlag=True
    for link in soup.find_all("a",class_="Next"):
        EntryFlag=False
        #print("for loop...")

        if link.text == "»":
            #print("Next Page Found . . .")
            url=(link.get("href"))
            Flag=True
            break
        else:
            #print("No Page Found")
            Flag=False

    if EntryFlag == True:
        Flag=False
