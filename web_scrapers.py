import requests
import webbrowser
import sys
import subprocess
from bs4 import BeautifulSoup

def google_search(qs):

    URL = 'https://www.google.com/search?q=' + qs
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.findAll("a")
    all_links = []
    for link in links:
       link_href = link.get('href')
       if "url?q=" in link_href and not "webcache" in link_href:
           all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))

    flag= False
    for link in all_links:
       if 'https://en.wikipedia.org/wiki/' in link:
           wiki = link
           flag = True
           break

    div0 = soup.find_all('div',class_="kvKEAb")
    div1 = soup.find_all("div", class_="Ap5OSd")
    div2 = soup.find_all("div", class_="nGphre")
    div3  = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")
    
    if len(div0)!=0:
        answer = div0[0].text
    elif len(div1) != 0:
       answer = div1[0].text+"\n"+div1[0].find_next_sibling("div").text
    elif len(div2) != 0:
       answer = div2[0].find_next("span").text+"\n"+div2[0].find_next("div",class_="kCrYT").text
    elif len(div3)!=0:
        answer = div3[1].text
    elif flag==True:
       page2 = requests.get(wiki)
       soup = BeautifulSoup(page2.text, 'html.parser')
       title = soup.select("#firstHeading")[0].text
       
       paragraphs = soup.select("p")
       for para in paragraphs:
           if bool(para.text.strip()):
               answer = title + "\n" + para.text
               break
    else:
        answer = "Sorry. I could not find the desired results"
        
    return answer
        
def getlinks(rjson):     
    url_list = []
    countlinks=0
        
    for i in rjson["items"]:
        if i["is_answered"]:
            url_list.append(i["link"])
        countlinks+=1
        if(countlinks==4 or countlinks==len(rjson["items"])):
            break
        
    for i in url_list:
        webbrowser.open(i)

def sendreq(stroutput):
    errortype,errormsg = stroutput.split('Error:')
    respoutput = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=Python&intitle={}&site=stackoverflow".format(stroutput))
    restype = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=Python&intitle={}&site=stackoverflow".format(errortype))
    respmsg = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=Python&intitle={}&site=stackoverflow".format(errormsg))
    print(respmsg.json())
    getlinks(respoutput.json())
    getlinks(restype.json())
    getlinks(respmsg.json())

if __name__ == "__main__":
    c = input("Stack or Google: ")
    if c.lower()=="stack":
        error = input("Enter the error message: ")
        sendreq(error)
    else:
        answer = google_search(input("Enter Search Query: "))
        print(answer)
    
    
    