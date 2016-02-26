from lxml import html
import requests
from bs4 import BeautifulSoup
import re,os
import codecs
import time
import socket
socket.getaddrinfo('localhost', 8080)

def main():
    base_url=r'http://forum.xda-developers.com'
    main_url=r'/galaxy-gear'
    app_page_data=requests.get(base_url+main_url)
    soup = BeautifulSoup(app_page_data.content, "lxml")

    for link in soup.find_all("div",class_="forum-cell"):
        try:
            TopicName=link.a.text
            TopicUrl=link.a.get("href")
            print("############################################################################\n")
            print('TopicName :',TopicName)
            print('TopicURL :',TopicUrl)
            print("Creating Topic Folder . . . ")
            if not os.path.exists(TopicName):
                os.makedirs(TopicName)
            print("\n############################################################################\n")

            #Loop for Topic
            PostCounts=0
            TopicFlag=True

            while (TopicFlag == True and PostCounts<200 ):
                app_page_data=requests.get(base_url+TopicUrl)
                print('Topic LINK:',base_url+TopicUrl)
                soup2 = BeautifulSoup(app_page_data.content, "lxml")
                for link2 in soup2.find_all("div",class_="thread-row"):
                    try:
                        PostCounts+=1
                        PostName=link2.find("a",class_="threadTitle threadTitleUnread").text
                        PostUrl=link2.find("a",class_="threadTitle threadTitleUnread").get("href")

                        #print(link2.a.text.strip('\n'))
                        #print(link2.find("a",class_="threadTitle threadTitleUnread").text)
                        #print(link2.a.get("href"))
                        #print(link2.find("a",class_="threadTitle threadTitleUnread").get("href"))
                        #print("Creating Review Scrape file . . .")
                        #file_name=link2.find("a",class_="threadTitle threadTitleUnread").text
                        file_name=re.sub('[^A-Za-z0-9]+', ' ', PostName)
                        review_file=r'./'+TopicName+r'/'+file_name+'.txt'
                        #print(review_file)

                        #f=open(review_file,'w')
                        f = codecs.open(review_file, 'w', encoding='utf8')
                        f.write("Topic :"+link2.find("a",class_="threadTitle threadTitleUnread").text+'\n')
                        f.write("URL :"+link2.find("a",class_="threadTitle threadTitleUnread").get("href")+'\n')
                        f.write("Parent Forum :"+TopicName+"\n")
                        f.write("Forum Topic : \n")
                        Count=1

                        #loop for reviews
                        ReviewCount=0
                        ReviewFlag=True
                        #ReviewUrl=link2.find("a",class_="threadTitle threadTitleUnread").get("href")

                        while (ReviewFlag == True):
                            app_page_data=requests.get(base_url+PostUrl)
                            #print("Replies LINK :",base_url+PostUrl)
                            #print("URL :"+base_url+link2.find("a",class_="threadTitle threadTitleUnread").get("href"))
                            soup3 = BeautifulSoup(app_page_data.content, "lxml")

                            for link3 in soup3.find_all("div",class_="post-text"):
                                try:
                                    ReviewCount+=1
                                    if Count==2:
                                        f.write("\n Forum Comments : \n")

                                    Count+=1

                                    f.write(link3.text)
                                    #print(link3.text.encode("utf-8"))
                                except Exception as e:
                                    f.write("Unable to get comments due to error :" + e)
                                    #print("Unable to get comments due to error :" + e)


                            EntryFlag=True
                            list=['next']
                            for link in soup3.find_all("a",class_="smallfont"):
                                EntryFlag=False
                                #print("for loop...")

                                if link.get('rel')==list:
                                    #print("Next Page Found . . .")
                                    PostUrl=('/'+link.get("href"))
                                    ReviewFlag=True
                                    break
                                else:
                                    #print("No Page Found")
                                    ReviewFlag=False


                            if EntryFlag == True:
                                ReviewFlag=False

                        print(PostName,'<-Post\tReplies->',ReviewCount)
                        f.close()

                            #break



                    except Exception as e:
                        print(e)


                EntryFlag=True
                list=['next']
                for link in soup2.find_all("a",class_="smallfont"):
                    EntryFlag=False
                    #print("In Loop . . .")

                    if link.get('rel')==list:
                        #print("Next Page Found . . .")
                        TopicUrl=(link.get("href"))
                        #print(TopicUrl)
                        TopicFlag=True
                        break
                    else:
                        #print("No Page Found")
                        TopicFlag=False

                if EntryFlag == True:
                    TopicFlag=False




            print("Topic - Posts Count : ",PostCounts)
            #break
        except Exception as e:
            print(e)

main()

