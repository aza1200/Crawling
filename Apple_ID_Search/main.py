import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib
import time
from selenium import webdriver

print("프로그램 시작")
Input_Data= pd.read_excel('test.xlsx')
Right_Count = 0
print(Input_Data)

Kor_Name_List = []
Eng_Name_List = []
Apple_Id_List = []

start_time = time.time()

#↓ 노트북 헤더
headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
#↓ 콘샐러드 헤더
#headers = { "User-Agent" :  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}


options = webdriver.ChromeOptions()
options.headless = True

driver = webdriver.Chrome(options = options)
driver.maximize_window()


count = 0

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return  False

def Find_Apple_id(Kor_Name,Eng_Name):
    print('\n\n')
    global count
    count +=1
    print(count," 번째 함수 시작 한글명 : ",Kor_Name, " 영어이름 ", Eng_Name)


    url_eng = f'''https://music.apple.com/kr/search?term={Eng_Name}'''
    url_kor = f'''https://music.apple.com/kr/search?term={Kor_Name}'''

    try:
        Tmp_Artist_ID_List = []

        if Kor_Name != 'nan':
            print(Kor_Name, " 아티스트 아이디 생성값 찾는중")
            driver.get(url_kor)
            print("3초간 기다리세요")
            time.sleep(3)
            kor_soup = BeautifulSoup(driver.page_source,'lxml')

            Artist_Info_Table = kor_soup.find('div', attrs={'class': 'shelf-grid shelf-grid--onhover'})
            Artist_List = Artist_Info_Table.find_all('li', attrs={'class': 'shelf-grid__list-item'})

            #(Artist_List,' ')

            for now in Artist_List:
                Artist_Link = str(now.find('a',attrs={'class':'line lockup__name'})['href']).strip()
                tmp_list=Artist_Link.split('/')
                if isNumber(tmp_list[-1]):
                    Tmp_Artist_ID_List.append(tmp_list[-1])
                    print(tmp_list[-1])
                else:
                    print(tmp_list[-1] , " 는 숫자형식이 아닙니다")

        if Eng_Name != 'nan':
            print(Eng_Name, " 아티스트 아이디 생성값 찾는중")
            driver.get(url_eng)
            print("4초간기다리세요")
            time.sleep(4)
            eng_soup = BeautifulSoup(driver.page_source,'lxml')

            Artist_Info_Table = eng_soup.find('div', attrs={'class': 'shelf-grid shelf-grid--onhover'})
            Artist_List = Artist_Info_Table.find_all('li', attrs={'class': 'shelf-grid__list-item'})

            for now in Artist_List:
                Artist_Link = str(now.find('a',attrs={'class':'line lockup__name'})['href']).strip()
                tmp_list=Artist_Link.split('/')
                if isNumber(tmp_list[-1]):
                    Tmp_Artist_ID_List.append(tmp_list[-1])
                    print(tmp_list[-1])
                else:
                    print(tmp_list[-1] , " 는 숫자형식이 아닙니다")


        Final_Data = 'NULL'

        print("아티스트 아이디 리스트 추출 완료")
        print("TMP ARTIST LIST 임 ",Tmp_Artist_ID_List)
        for tmp_id in Tmp_Artist_ID_List:
            if Check_Same(Kor_Name,Eng_Name,int(tmp_id))==True:
                Final_Data = tmp_id
                print(Kor_Name," ",Eng_Name," 의 아티스트 아디이디",tmp_id," 찾음")
                break

        Apple_Id_List.append(Final_Data)

    except:
        if len(Tmp_Artist_ID_List)==0:
            print(Kor_Name, " " , Eng_Name,"Apple id 값 못찾겠심다")
            Apple_Id_List.append('NULL')
        else:
            Final_Data = 'NULL'
            for tmp_id in Tmp_Artist_ID_List:
                #print(tmp_id," ",Kor_Name," " ,Eng_Name," 비교시작 ")
                if Check_Same(Kor_Name, Eng_Name, int(tmp_id)) == True:
                    Final_Data = tmp_id
                    print(Kor_Name, " ", Eng_Name, " 의 아티스트 아이디", tmp_id, " 찾음")
                    break

            print("애플아이디 값 ",Final_Data , '집어넣음 ')
            Apple_Id_List.append(Final_Data)


def Check_Same(Kor_Name,Eng_Name,Apple_id):
    global Right_Count
    eng_url = f'''https://itunes.apple.com/us/artist/shinhwa/{Apple_id}'''
    kor_url = f'''https://itunes.apple.com/kr/artist/shinhwa/{Apple_id}'''

    try:
        tmp_eng_res = requests.get(eng_url,headers=headers)
        time.sleep(1)
        tmp_eng_soup = BeautifulSoup(tmp_eng_res.text,'lxml')
        tmp_eng_name = tmp_eng_soup.find('h1',attrs={'class':'artist-header__product-title-product-name'}).get_text().strip()

        tmp_kor_res = requests.get(kor_url,headers=headers)
        time.sleep(1)
        tmp_kor_soup = BeautifulSoup(tmp_kor_res.text,'lxml')
        tmp_kor_name = tmp_kor_soup.find('h1',attrs={'class':'artist-header__product-title-product-name'}).get_text().strip()


        if Kor_Name == 'nan':
            if Eng_Name.lower().replace(' ','') == tmp_eng_name.lower().replace(' ',''):
                Right_Count += 1
                return True

        if Eng_Name == 'nan':
            if Kor_Name.replace(' ','') == tmp_kor_name.replace(' ',''):
                Right_Count += 1
                return True

        if Kor_Name == tmp_kor_name and Eng_Name.lower().replace(' ','') == tmp_eng_name.lower().replace(' ',''):
            Right_Count +=1
            return True

        if tmp_kor_name == tmp_eng_name and Eng_Name.lower().replace(' ','') == tmp_eng_name.lower().replace(' ',''):
            Right_Count +=1
            return True

        return False

    except:
        print("위 애플아이디 ",Apple_id,"는 유효하지 않은 페이지 입니다. ")
        return False


def main():

    #https://music.apple.com/us/search?term=
    for now_row in range(len(Input_Data)):
        Now_Artist_Kor_Name = str(Input_Data.loc[now_row]['국문']).strip()
        Now_Artist_Eng_Name = str(Input_Data.loc[now_row]['영문']).strip()

        Kor_Name_List.append(Now_Artist_Kor_Name)
        Eng_Name_List.append(Now_Artist_Eng_Name)

        Find_Apple_id(Now_Artist_Kor_Name,Now_Artist_Eng_Name)
        print(now_row+1, "중에서 ",Right_Count,"만큼 찾았음 ")
        print(int(time.time()-start_time),"초 만큼 현재 걸렸습니다 ")
        time.sleep(0.5)

    Final_Data = pd.DataFrame({'한글명' : Kor_Name_List,'영문명':Eng_Name_List,'Apple id' : Apple_Id_List})
    Final_Data.to_excel('Fianl_Data.xlsx',index=False)

    print()
    print(len(Input_Data)," 중에서 아티스트 아이디 에서",Right_Count," 만큼 찾았심다 " )

if __name__ == '__main__':
    main()