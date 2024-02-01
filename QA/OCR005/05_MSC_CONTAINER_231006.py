import re

inputOcr = '''
MSDU1463329 1 FIexibag of 100% REFINED BLEACHED DEODORIZED WINTERIZED SUNFLOWER 21,580.000 kgs.
20' DRY VAN SEED
OIL,NO ADDITIVES ; Customs Code 150930
Seal Number: Net weight 21480.00 KGM
L/C number MD1N32210NS00491 (see clause 14.5 hereof)
FX16723109
Tare Weight: 2,220 kgs. STATUS N
Marks and Numbers: .
FXT#TB2303132227
MSDU2129126 1 FIexibag of 100% REFINED BLEACHED DEODORIZED WINTERIZED SUNFLOWER 21,580.000 kgs.
20' DRY VAN SEED
OIL,NO ADDITIVES ; Customs Code 150930
Seal Number: Net weight 21480.00 KGM
L/C number MD1N32210NS00491 (see clause 14.5 hereof)
FX16716672
Tare Weight: 2,100 kgs. STATUS N
Marks and Numbers: .
FXT#TB2303108454
MSDU2547208 1 FIexibag of 100% REFINED BLEACHED DEODORIZED WINTERIZED SUNFLOWER 21,520.000 kgs.
20' DRY VAN SEED
OIL, NO ADDITIVES ; Customs Code 150930
Seal Number: Net weight 21420.00 KGM
L/C number MD1N32210NS00491 (see clause 14.5 hereof)
FX16716532
Tare Weight: 2,100 kgs. STATUS N
Marks and Numbers: .
FXT#TB220770028
FREIGHT PREPAID
HS CODE: 1512.19
PACKED IN 3 FLEXIBAG
Total net weight 64,380.000kg
Total gross weight 64,680.000kg
CFR INCHEON, SOUTH KOREA (3*20'FCL)
PORT OF DISCHERGE : Incheon South Korea republic of
PORT OF LOADING: Sines, Portugal
14 DAYS FREETIME
Total : 64,680.000 kgs.
'''

#MEDUFN238359
inputOcr = '''
SEGU9285032
4OHIGHCUBEREEFER
Seal Number:
Shipper 2880555
Marks and Numbers: Ryan :
S22089310
1970 Case(s) of
DAIRY PRODUCTS
Net Weight : 23569,08 KG
FREIGHT PREPAID
SHIPPED ON BOARD
Temperature: 3.0 C
Total Items: 1970 
24,762.900 kgs.
30.905cu,m.
'''


inputOcr = '''
SEGU9285032
4OHIGHCUBEREEFER
Seal Number:
NET WEIGHT : 22.424,420 KGS
002728
Marks and Numbers: Ryan :
S22089310
Net Weight : 23569,08 KG
FREIGHT PREPAID
SHIPPED ON BOARD
Temperature: 3.0 C
Total Items: 1970 
24,762.900 kgs.
30.905cu,m.
'''

### MEDUAW091063 BL
inputOcr = '''
MEDU9606012
1150 Carton(s) MOZZARELLA CHEESE FROZEN
23,366.270kgs.
40' HIGH CUBE REEFER
(EACH 2 X 10 KG NET APPROX)
TEMP REC 1 : 200000287613
Seal Number:002728
NET WEIGHT : 22.424,420 KGS
Temperature: -18.0 c
Total Items: 2296
'''

### MEDULZ450379 BL
inputOcr = '''
TRHU8476667
1260 Package(s) TERMS OF PRICE:CFR
25,951.800kgs.
40' HIGH CUBE
COUNTRYOF ORIGINITALY
Seal Number:11650
BASSO POMACE OLIVE OIL(5Kg/EA):2,520 BOX
607257
LC N.MD1N32303NS00566
Tare Weight:3.700 kgs
DATE OF ISSUE 230330
HSCODE15109000
MTSU9644703
1260 Package(s)+TERMS OF PRICE:CFR
25,951.800kgs.
40'HIGH CUBE
COUNTRY OFORIGIN:ITALY
Seal Number:009191
BASSO POMACE OLIVE OIL(5Kg/EA):2,520 BOX
011618
LC N.MD1N32303NS00566
Tare Weight:3.700 kgs.
DATE OF ISSUE230330
HS CODE15109000
'''

### MEDULZ450379 BL - new
inputOcr = '''
TRHU8476667 1260 Package(s)+TERMS OF PRICE:CFR 25,951.800kgs.
40'HIGH CUBE +COUNTRYOF ORIGINITALY
Seal Number:11650 BASSO POMACE OLIVE OIL(5Kg/EA):2,520 BOX
607257 LC N.MD1N32303NS00566
Tare Weight:3.700 kgs. DATE OF ISSUE 230330
HSCODE15109000
MTSU9644703 1260 Package(s)+TERMS OF PRICE:CFR 25,951.800kgs.
40'HIGH CUBE +COUNTRY OFORIGIN:ITALY
Seal Number:009191 BASSO POMACE OLIVE OIL(5Kg/EA):2,520 BOX
011618 LC N.MD1N32303NS00566
Tare Weight:3.700 kgs. DATE OF ISSUE230330
HS CODE15109000
'''

# 추출값 가공
inputOcr = inputOcr.upper()         # 대문자
inputOcr = inputOcr.split('\n')     # 각 줄을 split으로 구분

# 해당 Container 추출 제외 키워드 (Main에서 처리)
Extract_value = 'SEAL'    # 추출 키워드

# 변수 가공
Extract_Start_Bool = False    # 추출 or 추출 X 비교 변수( T = 추출, F = 추출X )

#■■ 추출 데이터 비교 함수
def Extract_comparison(inputOcr, Extract_Start_Bool):

    for find_Extract in inputOcr:

        if Extract_value in find_Extract:   # 'Seal' 값이 있으면 데이터 추출
            Extract_Start_Bool = True
            return Extract_Start_Bool

        else:
            Extract_Start_Bool = False
            continue

#■■ 필요한 정보를 잘못 읽을 수 있기 떄문에 replace
def ReplaceToBlank(find_row_text, text):
    try:
        for t in text:   
            find_row_text = find_row_text.replace(t, "")    # 잘못 읽은 데이터 삭제
    except:
        pass   

    return find_row_text

#■■■■■ sub1 (ContainerNo, Sealno, ContainerType) ■■■■■
# 설명 : CONTAINER에 있는 ContainerNo, Sealno, ContainerType 구하기
def Sub1(find_row_text, list_CONTAINERNO, list_SEALNO, list_CONTAINER_TYPE, before_find_row_text, before2_find_row_text): #두번째 전 값 비교 추가(SealNo 때문)

    # CONTAINER_TYPE 키워드( ★새로운 키워드 발생시 추가 )
    UnitList_CONTAINER_TYPE = ["DRY", "HC", "RF", "OT", "FR", "HIGH CUBE"]

    #
    SealNo_bool = False

    # 필요한 정보를 잘못 읽을 수 있기 때문에 replace
    find_row_text = find_row_text.replace('H&','HQ')
    find_row_text = find_row_text.replace('HIGHCUBE','HIGH CUBE')
    find_row_text = find_row_text.replace(' HQ','HQ')
    find_row_text = find_row_text.replace(' DRY','DRY')
    find_row_text = find_row_text.replace('\"','\'')
    find_row_text = find_row_text.replace('○','O')
    find_row_text = find_row_text.replace('X2O\'GP','X20GP')
    find_row_text = find_row_text.replace('X2O\'DV','X20DV')
    find_row_text = find_row_text.replace("4O'HIGH","40'HIGH") # Descriptionofgoods 에서 '0' 를 'O'로 잘못 인식했을경우 replace
    find_row_text = find_row_text.replace("4O' HIGH","40'HIGH") # Descriptionofgoods 에서 '0' 를 'O'로 잘못 인식했을경우 replace
    find_row_text = find_row_text.replace("4OHIGH","40HIGH")
    find_row_text = find_row_text.replace("4QHIGH","40HIGH")
    find_row_text = find_row_text.replace("4Q'HIGH","40'HIGH") 
    find_row_text = find_row_text.replace("4Q' HIGH","40'HIGH") 

    # 정규식 패턴(2)
    #r"[A-Z]{4}\s?[A-Z]?[0-9]{6}[-]?[0-9]{1}" > r"[A-Z]{3}[U]{1}\s?[A-Z]?[0-9]{6}[-]?[0-9]{1}"
    p_CONTAINERNO = r"[A-Z]{3}[U]{1}\s?[A-Z]?[0-9]{6}[-]?[0-9]{1}" # WHSU6111902(문자4, 숫자7), 숫자포함 0개 또는 1개이며 대문자 영어 4개이고 공백0개 또는 1개이며,대문자 영어 0개이상 포함하며 숫자는 7개
    # p_SEALNO = r"\d{7,9}|[^PO: /()a-z][A-Z]{2,3}\d{6,7}" # SM492952(문자2, 숫자6), 211393091(숫자 9), JPC586297(문자3, 숫자6) 'PO' 문자 제외
    p_SEALNO = r"[A-Z]{2}\d{6,8}[A-Z]*|[A-Z]{3}\d{6,8}|\d{3}[A-Z]{2}\d{6}|\d{6,8}"  # (문자2, 숫자6~8, 문자 인식 전체), (문자3, 숫자6~8), (숫자3, 문자2, 숫자6), (숫자 6~8)

    #■■ CONTAINERNO
    if "containerno" in find_row_text.lower().replace(" ", ""):         # find_row_text 를 소문자로 만들면서 공백은 제거 후 'containerno'가 find_row_text 안에 있는지 확인
        p_CONTAINERNO = r"Container\s?No\s?:\[A-Z]{4}[A-Z]?[0-9]{6}[-]?[0-9]{1}"
        t_CONTAINERNO = re.compile(p_CONTAINERNO).findall(find_row_text)       # P_Containerno 정규식에 맞는 문자만 list로 추출
        
        for i in range(len(t_CONTAINERNO)):
            t_CONTAINERNO[i] = re.sub(r"Container\s?No\s?:","",t_CONTAINERNO[i]).replace('-','').replace(' ','')
            list_CONTAINERNO.extend(t_CONTAINERNO)
    elif re.compile(r"[A-Z]{4}[A-Z]?[0-9]{7}\s?\/\s?\w+?\d+-?\d{2}\w?").match(find_row_text) != None:
        t_CONTAINERNO = re.compile(r"[A-Z]{4}[A-Z]?[0-9]{7}\s?\/\s?\w+?\d+-?\d{2}\w?").match(find_row_text).group()
        list_tmp = t_CONTAINERNO.split("/")
        # print(list_tmp)
        list_CONTAINERNO.append(list_tmp[0])
        list_SEALNO.append(list_tmp[1])
        find_row_text = ReplaceToBlank(find_row_text, t_CONTAINERNO)
        list_tmp = []
        
    else:
        t_CONTAINERNO = re.compile(p_CONTAINERNO).findall(find_row_text)
        # t_CONTAINERNO 안에 CODE 가 있으면 Break, 아니면 값 추출
        for String_Validation in t_CONTAINERNO:
            if 'CODE' in String_Validation:
                break
            elif len(t_CONTAINERNO) != 0: # 빈 값 덮어쓰기 방지
                find_row_text = ReplaceToBlank(find_row_text, t_CONTAINERNO)
                for i in range(len(t_CONTAINERNO)):
                    t_CONTAINERNO[i] = re.sub(r"Container\s?No\s?:","",t_CONTAINERNO[i]).replace('-','').replace(' ','')
                    list_CONTAINERNO.extend(t_CONTAINERNO)
                # list_CONTAINERNO.extend(t_CONTAINERNO)
                break
        

    #■■ SEALNO
    # SEAL 또는 L/C 가 before_find_row_text, find_row_text 변수 안에 값 유무 확인 ( 有 = seal number 찾기, 無 = pass )
    if 'SEAL' in before_find_row_text or 'L/C' in before_find_row_text or 'SEAL' in find_row_text or 'SEAL' in before2_find_row_text:
        if "sealno" in find_row_text.lower().replace(" ", ""): # SEAL NO : ~~
            p_SEALNO = r"Seal\s?No\s?:\s?\d{7,9}|[^PO: /()][A-Z]{2,3}\d{7}"
            t_SEALNO = re.compile(p_SEALNO).findall(find_row_text)
            for i in range(len(t_SEALNO)):
                t_SEALNO[i] = re.sub(r"Seal\s?No\s?:","",t_SEALNO[i])
                list_SEALNO.extend(t_SEALNO)

        # # 전 줄에 Seal 번호가 있고 정규식 조건에 맞으면
        # elif 'SEAL' in before_find_row_text and re.compile(r"[A-Z]{2}\d{6,8}[A-Z]*|[A-Z]{3}\d{6,8}|\d{3}[A-Z]{2}\d{6}|\d{6,8}|\d{5}"):
        #     p_SEALNO = r"[A-Z]{2}\d{6,8}[A-Z]*|[A-Z]{3}\d{6,8}|\d{3}[A-Z]{2}\d{6}|\d{6,8}|\d{5}"
        #     t_SEALNO = re.compile(p_SEALNO).findall(find_row_text)
        #     for i in range(len(t_SEALNO)):
        #         t_SEALNO[i] = re.sub(r"Seal\s?No\s?:","",t_SEALNO[i])
        #         list_SEALNO.extend(t_SEALNO)

        elif re.compile(r"[A-Z]{5}[0-9]{5}").match(find_row_text) != None:
            pass
        
        else:
            # p_SEALNO = r"[A-Z]{2}\d{6,8}[A-Z]*|[A-Z]{3}\d{6,8}|\d{3}[A-Z]{2}\d{6}|\d{6,8}|\d{5}"
            # t_SEALNO = re.compile(p_SEALNO).findall(find_row_text)
            # # print(f"t_SEALNO : {t_SEALNO}")
            # if len(t_SEALNO) != 0: # 빈 값 덮어쓰기 방지
            #         list_SEALNO.extend(t_SEALNO)

            # 패턴 0 = 영어 2개 이상, 숫자 6~8개, 영어 전체, or 영어 3개, 숫자 6~8개, or 숫자 3개, 영어2개,숫자6개, or 숫자 6~8개
            # 패턴 1 = 숫자가 5개
            p_SEALNO = r"[A-Z]{2}\d{6,8}[A-Z]*|[A-Z]{3}\d{6,8}|\d{3}[A-Z]{2}\d{6}|\d{6,8}", r"\s?\d{5}"
            # 정규식 패턴[0]에 매칭되는 부분을 추출
            P_match = re.search(p_SEALNO[0], find_row_text)
            # match에 값이 존재 할 경우
            #except 체크에 TOTAL, HS COD 추가
            if 'TOTAL' in find_row_text or 'HS COD' in find_row_text or 'L/C' in find_row_text or 'NET WEIGHT' in find_row_text or 'DATE' in find_row_text:
                pass
            elif P_match:
                SealNo_bool = True
                P_result = P_match.group()
                if len(list_SEALNO) == len(list_CONTAINERNO):
                    list_SEALNO.pop(-1) #마지막 값을 빼고 신규값 추가
                list_SEALNO.append(P_result)
                
            elif SealNo_bool == False:   # 정규식 패턴[0]에 매칭이 안되면 정규식 패턴[1]에 매칭되는 부분을 추출

                P_match = re.search(p_SEALNO[1], find_row_text)
                if 'TOTAL' in find_row_text or 'HS COD' in find_row_text or 'L/C' in find_row_text or 'NET WEIGHT' in find_row_text or 'DATE' in find_row_text:
                    pass
                elif P_match:
                    P_result = P_match.group()
                    if len(list_SEALNO) == len(list_CONTAINERNO):
                        list_SEALNO.pop(-1) #마지막 값을 빼고 신규값 추가
                    list_SEALNO.append(P_result)


        # # 예외case1
        # if "referencenumber" in find_row_text.lower().replace(" ", ""):
        #     for t in t_SEALNO:
        #         list_SEALNO.remove(t)
        # # 예외case2
        # if "NUMBER" in find_row_text.upper().replace(" ", ""): 
        #     for t in t_SEALNO:
        #         list_SEALNO.remove(t)
    else:
        pass

    #■■ CONTAINER TYPE
    for type in UnitList_CONTAINER_TYPE:
        # if type.replace(" ","") in find_row_text.upper().replace(" ",""):
        if type in find_row_text.upper():

            # type 변수 안에 find_row_Text가 있고 type이 'OTPU'에 포함되어 있으면 Continue
            # 이후 제외 키워드가 많을시 제외리스트 만들 예정
            if type in find_row_text.upper() and type in 'OTPU':
                continue
            

            # ["DRY", "HC", "RF", "OT", "FR", "HIGH CUBE"]
            p_CONTAINERTYPE = r"\d{2}[`']?\s?DRY|\d{2}[`']?\s?HC|\d{2}[`']?\s?RF|\d{2}[`']?\s?OT\n\
            |\d{2}[`']?\s?FR|\w{2}[`']?\s?HIGH\s?CUBE\s?REEFER|\w{2}[`']?\s?HIGH\s?CUBE"
            t_CONTAINERTYPE = re.compile(p_CONTAINERTYPE).findall(find_row_text)
            for i in range(len(t_CONTAINERTYPE)):
                t_CONTAINERTYPE[i] = re.sub(r"[`']","",t_CONTAINERTYPE[i]).replace(' ','')
                list_CONTAINER_TYPE.extend(t_CONTAINERTYPE)
            # list_CONTAINER_TYPE.extend(t_CONTAINERTYPE)

    return list_CONTAINERNO, list_SEALNO, list_CONTAINER_TYPE, before_find_row_text, before2_find_row_text


#■■■■■ sub2 (Packages, Description of Goods) ■■■■■
# 설명 : CONTAINER에 있는 PACKAGE,DESCRIPTIONOFGOODS 구하기
def Sub2(find_row_text, list_DESCRIPTIONOFGOODS, list_PACKAGES):

    find_row_text = find_row_text.replace('CASE{S)','CASE(S)')

    # Descriptionofgoods 에서 가공할 list 변수 선언
    find_row_list = []

    # ★ 제외 리스트 키워드("Description of goods"항목에 추가적으로 제거해야되는 문자가 있으면 리스트형태로 값을 넣어주면됨. ★)
    EXCEPT_LIST = ['OF','2000 CT','CARTON(S)','CARTONS']

    # Find_PACKGES : ★ PACKGES에 해당하는 키워드 ★
    Find_PACKAGES = ["PKGS","CTNS","CARTON(S)","CASES", "CASE(S)","CARTONS","BAGS", "BOXES", "CRTS", "DRS", "PLTS", "ROLS", "TANKS", "PACKAGE"] # 대문자

    # Find_DESCRIPTIONOFGOODS : ★ 해당 상품 리스트 (품목이 증가 되면 추가 해줘야됨) ★
    Find_DESCRIPTIONOFGOODS = ['FROZEN','CREAM','FUSED','CHEESE','BASSO', 'BLACK', 'BUTTER', 'CANNED', 'CHINESE', 'GROZEN', 'INDELHI', 'INSTANT', 'MUSHROOM', 'OLIVE', 'SMOKED', 'SQUID', 'WHIPPING', 'HADAY', 'MILKY', 'PEELED', 'SOY', 'SWEET', 'CREAM', 'ALIMENTARY', 'GREEN', 'CURRY', 'MILK', 'MOZZARELLA', 'DANG', 'RENNET', 'SUNLEE', "IT'S", 'CORN', 'PASTAVILLA', 'UNSALTED', 'WELL', 'HNT', 'SALT', 'FROZEN BONELESS BEEF-20C', 'FROZEN PORK', 'FROZEN MANGOES', 'RENNET CASEIN', 'FROZEN FRENCH FRIES', 'BASSO POMACE OLIVE OIL', 'FROZEN SALMON COHO HG','SUNFLOWER', 'DAIRY PRODUCTS','DAIRY PRODUCT']

    # 만약 제외 키워드가 없는 데이터가 나왔는데 Description of goods 에 필요없는 값이 나올 경우 필요한 변수
    EXCEPT_Bool = False

    find_row_text.strip()    # 양쪽 공백 제거

    # 필요한 정보를 잘못 읽을 수 있기 때문에 replace
    find_row_text = find_row_text.replace('FRQZEN','FROZEN')    # Descriptionofgoods 에서 'O' 를 'Q'로 잘못 인식했을경우 replace
    find_row_text = find_row_text.replace('ATLANT1C','ATLANTIC') # Descriptionofgoods 에서 'I' 를 '1'로 잘못 인식했을경우 replace


    #■■ PACKGES 구하기
    for PACKGES in Find_PACKAGES:   # Find_PACKAGES에 해당하는 값이 포함되어 있으면 PACKGES에 포함된 값 저장
        # if list_PACKAGES:   # list_PACKAGES 값이 존재 시 루프 탈출 (현재는 하나의 값만 가져오기 위해 설정)
        #     break
        if 'TOTAL' in find_row_text:
            continue
        if PACKGES in find_row_text: # find_row_text PACKGES의 포함된 값이 있을경우 
            find_Gap = find_row_text.find(PACKGES) # find_Gap에 인덱스 저장 (Find_PACKAGES의 포함된 리스트 값 제거)
            # find_row_text = find_row_text.replace('I','1')    # 1을 I로 읽었을 경우 바꿔줌
            pattern = r"\d{0,}\s{0,}"+ re.escape(PACKGES)  # 숫자 최소 0개 문자 최소 0개의 PACKAGE_LIST의 해당하는 값의 패턴
            matches = re.findall(pattern, find_row_text)   # 찾은 패턴을 matches에 리스트 형태로 저장
            matches = matches[0].replace(PACKGES,'')    # matches의 첫번째 리스트 값의 PACKGES의 값 제거 (예시) 1060CARTONS -> 1060
            matches = matches.strip()     # 양쪽 공백 제거

            if '' == matches:       # 공백이 들어오면 다음건으로 넘어가기
                pass
            else:       # matches에 값이 있으면 list_PACKGES에 값 추가
                list_PACKAGES.append(matches) # list_PACKAGES 제외 문구 전까지의 값 저장
                # list_PACKAGES.append(find_row_text)
       
    
    #■■ DESCRIPTIONOFGOODS 구하기
    for DESCRIPTIONOFGOODS in Find_DESCRIPTIONOFGOODS:  # Find_DESCRIPTIONOFGOODS 리스트 수만큼 루프

        if DESCRIPTIONOFGOODS in find_row_text:    # Find_DESCRIPTIONOFGOODS에 해당 값이 같으면 DESCRIPTIONOFGOODS에 값 저장

            for EXCEPT_word in EXCEPT_LIST: # 제외 키워드 확인 후 값 해당하는 값 지우기
                
                if EXCEPT_word in find_row_text: # find_row_text 제외키워드가 포함시 제거
                    EXCEPT_Bool = True
                    find_row_list = find_row_text.split(EXCEPT_word)    # 제외키워드를 기준으로 split
                    find_row_text = find_row_list[1]    # list의 1번쨰 값 추출
                    find_row_text = re.sub("\d*[.,]{1,1}\w*[ ]?\w*", '', find_row_text) # 뒤에 영어가 있고 ".", ","가 1개가 포함된 숫자가 있으면 제거
                    if '(' in find_row_text:
                        find_row_list = find_row_text.split('(')    # '('제외키워드)''를 기준으로 split
                        find_row_text = find_row_list[0]    # list의 0번쨰 값 추출
                    find_row_text = find_row_text.strip() # 양쪽 공백 제거
                    list_DESCRIPTIONOFGOODS.append(find_row_text)  # list_DESCRIPTIONOFGOODS 값 저장
                else:   # if문을 안타면 다음 값 실행
                    continue

                
            if len(list_DESCRIPTIONOFGOODS) == 0 or EXCEPT_Bool == False:   # 제외키워드를 못타고 값을 못 받을 시
                find_row_list2 = find_row_text.split(DESCRIPTIONOFGOODS)
                find_row_text = DESCRIPTIONOFGOODS + " " + find_row_list2[1]
                find_row_text = re.sub("\d*[.,]{1,1}\w*[ ]?\w*", '', find_row_text) # 뒤에 영어가 있고 ".", ","가 1개가 포함된 숫자가 있으면 제거
                if '(' in find_row_text:
                    find_row_list = find_row_text.split('(')    # '('제외키워드)''를 기준으로 split
                    find_row_text = find_row_list[0]    # list의 0번쨰 값 추출
                find_row_text = find_row_text.strip() # 양쪽 공백 제거
                list_DESCRIPTIONOFGOODS.append(find_row_text)
                break
    
    # # PACKAGES, DESCRIPTIONOFGOODS 추출 대상이 없을 경우
    # if len(list_PACKAGES) == 0:
    #     list_PACKAGES.append('추출 대상이 없습니다.')
    # if len(list_DESCRIPTIONOFGOODS) == 0:
    #     list_DESCRIPTIONOFGOODS.append('추출 대상이 없습니다.')

    return list_DESCRIPTIONOFGOODS, list_PACKAGES


#■■■■■ sub3 (GrossWeight, Measurement) ■■■■■
def Sub3(find_row_text, GROSS_LIST, MEASUREMENT_LIST):

    # 필요한 정보를 잘못 읽을 수 있기 때문에 replace
    find_row_text = find_row_text.replace('YGM','KGM')
    find_row_text = find_row_text.replace('MTO','MTQ')
    find_row_text = find_row_text.replace('CU. M.','CUM')
    find_row_text = find_row_text.replace('CU M.','CUM')
    find_row_text = find_row_text.replace('CU. M','CUM')
    find_row_text = find_row_text.replace('CU.M.','CUM')
    find_row_text = find_row_text.replace('CU.M','CUM')
    find_row_text = find_row_text.replace('CUM.','CUM')

    # ★ 제외 리스트 키워드("GROSS_WEIGHT"항목에 추가적으로 제거해야되는 문자가 있으면 리스트형태로 값을 넣어주면됨. ★)
    EXCEPT_LIST = ['WEIGHT','TOTAL','BOX']

    # 중량 단위 리스트 형태로 저장 (추후 새로운 중량 단위가 나올경우 넣어줘야됨)
    GROSS = ["KGS", "LBS", "KGM", "NET"]
    MEASUREMENT = ["CBM", "CUM", "MTQ", "M3"]

    # 중량 단위가 있으면 check
    GROSS_check = False

    # gross_weight 제외 키워드가 있으면 제외
    for EXCEPT_word in EXCEPT_LIST:
        if EXCEPT_word in find_row_text:
            return GROSS_LIST, MEASUREMENT_LIST


    # 여러개의 객체를 묶어서 동시에 반복
    for g,w in zip(GROSS,MEASUREMENT):

        
        # # TOTAL 값은 제외
        # if 'TOTAL' in find_row_text:
        #     continue
        
        result = ''
        result2 = ''

        # GROSS 와 MEASURMENT가 같이 포함될 경우
        if g in find_row_text:
            # 단위가 있을 경우 True
            GROSS_check = True

            # GROSS에 포함된 단위 찾기
            # 패턴 0 = 숫자가 1개이상이고 (".", ",") 1개이상이며 g(단위)가 포함된 수
            # 패턴 1 = 숫자가 1개이상이고 g(단위)가 포함된 수
            pattern = r"(\d{1,}[,.])+\d{3,}\s{0,}" + re.escape(g), r"(\d{1,})"+ re.escape(g) 
            # 정규식 패턴[0]에 매칭되는 부분을 추출
            match = re.search(pattern[0], find_row_text)
            # match에 값이 존재 할 경우
            if match:
                result = match.group()
                # 숫자와 ',', '.' 를 제외한 나머지 문자 제거
                result = re.sub(r"[^\d.,¿]",'',result)
                GROSS_LIST.append(result)

            else:   # 정규식 패턴[0]에 매칭이 안되면 정규식 패턴[1]에 매칭되는 부분을 추출
                match = re.search(pattern[1], find_row_text)
                if match:
                    result = match.group()
                    # 숫자와 ',', '.' 를 제외한 나머지 문자 제거
                    result = re.sub(r"[^\d.,¿]",'',result)
                    GROSS_LIST.append(result)
        
        elif g == GROSS[-1] and GROSS_check == False:
            pattern = r"(\d{1,}[.,])+\d{3,}\s?"
            match = re.search(pattern, find_row_text)
            
            if match:
                result = match.group()
                result = re.sub(r"[^\d.,¿]",'',result)
                GROSS_LIST.append(result)

        # GROSS 와 MEASURMENT가 같이 포함될 경우
        if w in find_row_text:

            # MEASUREMENT에 포함된 단위 찾기
            # 패턴 0 = 숫자가 1개이상이고 (".", ",") 1개이상이며 w(단위)가 포함된 수
            # 패턴 1 = 숫자가 1개이상이고 w(단위)가 포함된 수
            pattern = r"(\d{1,}[,.])+\d{3,}\s{0,}" + re.escape(w), r"(\d{1,})"+ re.escape(w)
            # 정규식 패턴에 매칭되는 부분을 추출
            match = re.search(pattern[0], find_row_text)
            # match에 값이 존재 할 경우
            if match:
                result2 = match.group()
                # 숫자와 ',', '.' 를 제외한 나머지 문자 제거
                result2 = re.sub(r"[^\d.,¿]",'',result2)
                MEASUREMENT_LIST.append(result2)
            else:   # 정규식 패턴[0]에 매칭이 안되면 정규식 패턴[1]에 매칭되는 부분을 추출
                match = re.search(pattern[1], find_row_text)
                if match:
                    result2 = match.group()
                    # 숫자와 ',', '.' 를 제외한 나머지 문자 제거
                    result = re.sub(r"[^\d.,¿]",'',result2)
                    MEASUREMENT_LIST.append(result2)
        elif w == MEASUREMENT[-1] and GROSS_check == False:
            pattern = r"\s?\d{1,}[.,]+\d{3,}"
            match = re.findall(pattern, find_row_text)

            if match :
                result2 = match[-1]
                result2 = re.sub(r"[^\d.,¿]", '', result2)
                MEASUREMENT_LIST.append(result2)

    # Gross_weight, Measurement 단위가 없으면 타는 로직
    # 단위가 없으면 Patten(정규식)을 찾고 찾는 값이 있으면 Gross_weight list , Measurement list 에 값 저장
        

    return GROSS_LIST, MEASUREMENT_LIST

#■■■■■ Main ■■■■■
def Main(inputOcr):

    # 결과 값을 담을 딕셔너리 선언
    return_value = {} # 딕셔너리 선언

    # 다중 필드 선언
    return_value['CONTAINERNO'] = ''         # CONTAINERNO 필드 선언
    return_value['SEALNO'] = ''              # SEALNO 필드 선언
    return_value['CONTAINERTYPE'] = ''       # CONTAINERTYPE 필드 선언
    return_value['DESCRIPTIONOFGOODS'] = ''  # DESCRIPTIONOFGOODS 필드 선언
    return_value['PACKAGES'] = ''            # PACKAGES 필드 선언
    return_value['GROSSWEIGHT'] = ''         # GROSSWEIGHT 필드 선언
    return_value['MEASUREMENT'] = ''         # MEASUREMENT 필드 선언

    # 결과를 담은 List 선언
    list_CONTAINERNO = []
    list_SEALNO = []
    list_CONTAINER_TYPE = []
    list_DESCRIPTIONOFGOODS = []
    list_PACKAGES = []
    GROSS_LIST = []
    MEASUREMENT_LIST = []

    # 변수 선언
    before_find_row_text = ''
    before2_find_row_text = '' #2번째 전 문장에 Seal이 포함되어있는지 확인 위해 추가

    # 데이터를 추출해야 할지 판단하는 로직
    find_Extract_compare = Extract_comparison(inputOcr, Extract_Start_Bool)

    # 추출 키워드가 없으면( find_Extract_compare == False )  강제 종료
    if find_Extract_compare == None:
        return return_value     # 공백 값 추출

    # 여러개의 객체를 묶어서 동시에 입력
    for find_row_text in inputOcr:
        
        # Sub1 (ContainerNo, Sealno, ContainerType, before_find_row_text) 호출  # before_find_row_text = 추출한 전 문장을 보기 위해서 필요
        Sub1_Result = Sub1(find_row_text, list_CONTAINERNO, list_SEALNO, list_CONTAINER_TYPE, before_find_row_text, before2_find_row_text)

        # Sub2 (Packages, Description of Goods) 호출
        Sub2_Result = Sub2(find_row_text, list_DESCRIPTIONOFGOODS, list_PACKAGES)

        # Sub3 (GrossWeight, Measurement) 호출
        Sub3_Result = Sub3(find_row_text, GROSS_LIST, MEASUREMENT_LIST)

        ## 전전 문장 담기
        before2_find_row_text = before_find_row_text

        # 전 문장 담기
        before_find_row_text = find_row_text

    # GROSS_LIST 길이가 0이 아니고 Measurement_list 값이 없으면 Gross_list 개수 만큼 0추가
    if len(GROSS_LIST) != 0 and len(MEASUREMENT_LIST) == 0:
        gross_weight = len(GROSS_LIST)
        # Gross_list 갯수만큼 0 추가
        MEASUREMENT_LIST = ["0" for i in GROSS_LIST]

    # List 중복 제거 (key값을 기준으로 순서대로 중복값 제거)
    list_CONTAINERNO = list(dict.fromkeys(list_CONTAINERNO))
    list_SEALNO = list(dict.fromkeys(list_SEALNO))
    # list_CONTAINER_TYPE = list(dict.fromkeys(list_CONTAINER_TYPE))
    # list_DESCRIPTIONOFGOODS = list(dict.fromkeys(list_DESCRIPTIONOFGOODS))
    # GROSS_LIST = list(dict.fromkeys(GROSS_LIST))


    # 딕셔너리에 값 넣기
    return_value['CONTAINERNO'] = list_CONTAINERNO
    return_value['SEALNO'] = list_SEALNO
    return_value['CONTAINERTYPE'] = list_CONTAINER_TYPE
    return_value['DESCRIPTIONOFGOODS'] = list_DESCRIPTIONOFGOODS
    return_value['PACKAGES'] = list_PACKAGES
    return_value['GROSSWEIGHT'] = GROSS_LIST
    return_value['MEASUREMENT'] = MEASUREMENT_LIST
    
    return return_value

field_value = Main(inputOcr)