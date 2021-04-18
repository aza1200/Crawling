from bs4 import BeautifulSoup
import pandas as pd
import requests
import urllib.request

#↓ 노트북 헤더
#headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
#↓ 콘샐러드 헤더
headers = { "User-Agent" :  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}


Final_Album_Name = []
Final_Track_Artist_Name = []
Final_Album_ID = []

count = 0

def Find_Album_ID(Album_Name,Track_Artist):
    global count
    count +=1
    print(count,"번째 함수 실행")
    Send_Key_Element = Album_Name + " " + Track_Artist
    Send_Key_Element = urllib.parse.quote(Send_Key_Element)

    url = f'''https://music.bugs.co.kr/search/album?q={Send_Key_Element}'''

    res = requests.get(url,headers = headers)

    soup = BeautifulSoup(res.text,'lxml')

    try:
        print('검색 후 앨범검색페이지 넘어옴')
        Album_Number = soup.find('table').find_all('td')[2]
        Album_Number = Album_Number.find('span').get_text().strip()


        if Album_Number == '(1)':
            Final_Data = soup.find('figure')['albumid'].strip()
            print(f'''{Album_Name} 아티스트 {Track_Artist} 의 앨범 아이디는 {Final_Data}''')
        else:
            Final_Data = "NULL"
            print(f'''{Album_Name} 아티스트 {Track_Artist} 의 앨범 아이디는 {Final_Data}''')



    except:
        Final_Data  = "NULL"
        print(Album_Name, " 하고 ",Track_Artist,"는 안나오는듯 " , Final_Data)

    Final_Album_Name.append(Album_Name)
    Final_Track_Artist_Name.append(Track_Artist)
    Final_Album_ID.append(Final_Data)

def main():

    print("데이터 읽기 시작")
    Input_Data = pd.read_excel('Input_Data.xlsx')
    print("데이터 다 읽음")


    Number_of_Row = len(Input_Data)


    for now in range(Number_of_Row):
        Tmp_Album_Name =  str(Input_Data.loc[now,'앨범명']).strip()
        Tmp_Track_Artist_Name = str(Input_Data.loc[now,'트랙 아티스트명']).strip()
        Find_Album_ID(Tmp_Album_Name,Tmp_Track_Artist_Name)

    Final_Data = pd.DataFrame({'Album_Code':Final_Album_Name,
                               'Track_Artist_Name' :Final_Track_Artist_Name,
                               'Album_ID':Final_Album_ID})

    Final_Data.to_excel('output.xlsx',index=False)

if __name__ == "__main__":
    main()