from lxml import html
import requests
from bs4 import BeautifulSoup
import re,os
import codecs


Flag=True
base_url=r'http://www.androidauthority.com/community'
main_url=r'/forums/smartwatch-discussion.492'

while (Flag == True):
    app_page_data=requests.get(base_url+main_url)
    print('Topic Link:',base_url+main_url)
    soup = BeautifulSoup(app_page_data.content, "lxml")

    for link in soup.find_all("div",class_="titleText"):
        try:
            PostName=link.a.text
            PostUrl=link.a.get("href")
            #print('Post Topic :',PostName)
            #print('Post Url :',PostUrl)
            #print("Creating Review Scrape file . . .")
            #file_name=link.a.text.strip('\n')
            file_name=re.sub('[^A-Za-z0-9]+', ' ', PostName)
            review_file=r'./'+file_name+'.txt'
            #print(review_file)

            #f=open(review_file,'w')
            f = codecs.open(review_file, 'w', encoding='utf8')
            f.write("Topic :"+link.a.text.strip('\n')+"\n")
            f.write("URL :"+base_url+"/"+link.a.get("href")+"\n")
            f.write("Comments : \n")

            #loop for Reviews
            ReviewCount=0
            ReviewFlag=True

            while (ReviewFlag == True):
                #print('Debug...')
                app_page_data=requests.get(base_url+"/"+PostUrl)
                #print('Review Link:',base_url+"/"+PostUrl)
                soup2 = BeautifulSoup(app_page_data.content, "lxml")
                for link2 in soup2.find_all("blockquote",class_="messageText SelectQuoteContainer ugc baseHtml"):
                    try:
                        f.write(link2.text)
                        ReviewCount+=1
                    except Exception as e:
                        f.write("Unable to get comments due to error :" + e)
                        #print(e)

                EntryFlag=True
                for link in soup2.find_all("a",class_="text"):
                    EntryFlag=False
                    if link.text == "Next >":
                        #print("Next Page Found . . .")
                        PostUrl=('/'+link.get("href"))
                        ReviewFlag=True
                        break
                    else:
                        ReviewFlag=False

                if EntryFlag == True:
                    ReviewFlag=False

            print(PostName,'<-Post\tReplies->',ReviewCount)
            f.close()

        except Exception as e:
            print(e)

    for link in soup.find_all("a",class_="text"):
        if link.text == "Next >":
            #print("Next Page Found . . .")
            main_url=('/'+link.get("href"))
            Flag=True
            break
        else:
            Flag=False
