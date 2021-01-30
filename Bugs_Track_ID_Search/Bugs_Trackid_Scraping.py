import pandas as pd
import requests
from bs4 import BeautifulSoup

print("읽기시작합니다")
Input_data = pd.read_excel('Input_Data.xlsx')
print("Input 파일 읽는중")

# ↓ 회사 컴터 헤더
#headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
# ↓ 노트북 헤더
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}

Final_Album_ID_List = []
Final_Track_Seq_List  = []
Final_Track_ID_List = []

#print(Input_data.loc[0])
Number_of_Row = len(Input_data)

def Find_Bugs_Track_Id(Album_ID,Track_Seq):

    url =f'''https://music.bugs.co.kr/album/{Album_ID}?wl_ref=list_tr_11_search'''
    res = requests.get(url,headers=headers)

    soup = BeautifulSoup(res.text,'lxml')

    Tmp_Track_Seq_List = []
    Tmp_Track_ID_List = []

    Track_Seq_Info_List = soup.find_all("p", attrs={'class': 'trackIndex'})
    Track_Id_Info_List = soup.find_all('a', attrs={'class': 'trackInfo'})

    for now in Track_Id_Info_List:
        Tmp_Track_ID_List.append(str(now['href'])[31:-21])

    for Track in Track_Seq_Info_List:
        Tmp_Track_Seq_List.append((Track.find('em').get_text()))

    Track_Num = len(Tmp_Track_Seq_List)

    Tmp_Dictionary = {}

    for now in range(Track_Num):
        Tmp_Dictionary[Tmp_Track_Seq_List[now]]=Tmp_Track_ID_List[now]

    if Track_Seq not in Tmp_Dictionary:
        Real_Answer = "NULL"
    else :
        Real_Answer = Tmp_Dictionary[Track_Seq]

    Final_Track_ID_List.append(Real_Answer)

    print("Album ID : " , Album_ID, " Track Seq : ",Track_Seq, "Track_ID",Real_Answer,"구함")

for now in range(Number_of_Row):
    Tmp_Album_Code  = str(Input_data.loc[now,'Bugs_Album_Code']).strip()
    Tmp_Track_Seq   = str(Input_data.loc[now,'Bugs_Track_Seq']).strip()
    Find_Bugs_Track_Id(Tmp_Album_Code,Tmp_Track_Seq)

Final_Data = pd.DataFrame({'Album_Code':Final_Album_ID_List,
                           'Track_Seq' :Final_Track_Seq_List,
                           'Track_Code':Final_Track_ID_List})

Final_Data.to_excel('output.xlsx',index=False)
