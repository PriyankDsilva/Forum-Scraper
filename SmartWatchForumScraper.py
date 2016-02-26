import requests
from bs4 import BeautifulSoup
import re,os
import codecs

#defining main function
def main():
    #url for the smartwatch website
    url=r'http://www.smartwatchforum.com/forum/index.php/forum/1-smartwatch-forums/'
    app_page_data=requests.get(url)
    soup = BeautifulSoup(app_page_data.content, "lxml")

    #looping through sub forums
    for link in soup.find_all("td",class_="col_c_forum"):
        try:
            print('#####'+link.a.text+'#####')
            print(link.a.get("href"))
            print("Creating Folder . . . ")
            #create folder
            TopicName=link.a.text
            if not os.path.exists(TopicName):
                os.makedirs(TopicName)

            count=0
            #Loop for Topic
            TopicFlag=True
            TopicUrl=link.a.get("href")

            while (TopicFlag == True):
                #fetching data for Sub Forumn
                app_page_data=requests.get(TopicUrl)
                soup2 = BeautifulSoup(app_page_data.content, "lxml")

                #Looping through Topics of Sub Forum
                for link2 in soup2.find_all("td",class_="col_f_content "):
                    try:
                        count+=1

                        print(link2.a.text.strip('\n'))
                        print(link2.a.get("href"))
                        print("Creating Review Scrape file . . .")

                        #creating file structure for the Topic and Comments
                        file_name=link2.a.text.strip('\n')
                        file_name=re.sub('[^A-Za-z0-9]+', ' ', file_name)
                        review_file=r'./'+TopicName+r'/'+file_name+'.txt'
                        print(review_file)

                        f = codecs.open(review_file, 'w', encoding='utf8')
                        f.write("Topic :"+link2.a.text.strip('\n')+"\n")
                        f.write("URL :"+link2.a.get("href")+"\n")
                        f.write("Parent Forum :"+TopicName+"\n")
                        f.write("Comments : \n")

                        #loop for reviews
                        replycount=0
                        ReviewFlag=True
                        ReviewUrl=link2.a.get("href")

                        while (ReviewFlag == True):
                            app_page_data=requests.get(ReviewUrl)
                            soup3 = BeautifulSoup(app_page_data.content, "lxml")

                            for link3 in soup3.body.find_all("div",class_="post entry-content "):
                                try:
                                    replycount+=1
                                    f.write(link3.text)
                                except Exception as e:
                                    f.write("Unable to get comments due to error :" + e)

                            EntryFlag=True
                            for link in soup3.find_all("li",class_="next"):
                                EntryFlag=False
                                print("for loop...")

                                if link.text == "Next":
                                    print("Next Page Found . . .")
                                    ReviewUrl=(link.a.get("href"))
                                    ReviewFlag=True
                                    break
                                else:
                                    print("No Page Found")
                                    ReviewFlag=False

                            if EntryFlag == True:
                                ReviewFlag=False

                        print('Replies : ',replycount)
                        #Closing the file
                        f.close()


                    except Exception as e:
                        print(e)

                EntryFlag=True
                for link in soup2.find_all("li",class_="next"):
                    EntryFlag=False
                    print("for loop...")

                    if link.text == "Next":
                        print("Next Page Found . . .")
                        TopicUrl=(link.a.get("href"))
                        TopicFlag=True
                        break
                    else:
                        print("No Page Found")
                        TopicFlag=False

                if EntryFlag == True:
                    TopicFlag=False

            print("Topic - Posts Count : ",count)

        except Exception as e:
            print(e)

#calling main function
main()

