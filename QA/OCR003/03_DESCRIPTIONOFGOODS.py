inputOcr = '''
1 CONT. 40'X9'6" REEFER CONTAINER
1692 CARTON(S)
FROZEN FRENCH FRIES
TEMPERATURE TO BE SET AT -2l,0 C
'''


# 설명 : CONTAINER에 있는 PACKAGE,DESCRIPTIONOFGOODS 구하기



field_value = {}    # field_value 딕셔너리 선언

field_value['DESCRIPTIONOFGOODS'] = ''  # DESCRIPTIONOFGOODS 초기값 설정

field_value['PACKAGES'] = ''# PACKAGES 초기값 설정

DESCRIPTIONOFGOODS_list = []    # DESCRIPTIONOFGOODS_list 리스트 선언

PACKAGES_list = []  # PACKAGES_list 리스트 선언


inputOcr = inputOcr.upper() # inputOcr 대문자로 변경

inputOcr = inputOcr.replace('WTTH','WITH') # 잘못 인식한 값 REPLACE

split_list = inputOcr.split('\n')   # inputOcr을 줄바꿈 기준으로 리스트 선언




# 제외 리스트 키워드(추가적으로 제거해야되는 문자가 있으면 리스트형태로 값을 넣어주면됨.)
EXCEPT_LIST = ['OF','2000 CT']




# Find_PACKGES : PACKGES에 해당하는 키워드
Find_PACKAGES = ["PKGS","CTNS","PACKAGE(S)","CARTON(S)","CASES","CARTONS","BAGS", "BOXES", "B0XES", "CRTS", "DRS", "PLTS", "ROLS", "TANKS"] # 대문자




# Find_DESCRIPTIONOFGOODS : 해당 상품 리스트 (품목이 증가 되면 추가 해줘야됨)
Find_DESCRIPTIONOFGOODS = ['FROZEN','CREAM','FUSED','CHEESE','BASSO', 'BLACK', 'BUTTER', 'CANNED', 'CHINESE', 'GROZEN', 'INDELHI', 'INSTANT', 'MUSHROOM', 'OLIVE', 'SMOKED', 'SQUID', 'WHIPPING', 'HADAY', 'MILKY', 'PEELED', 'SOY', 'SWEET', 'CREAM', 'ALIMENTARY', 'GREEN', 'CURRY', 'MILK', 'MOZZARELLA', 'DANG', 'RENNET', 'SUNLEE', 'NATURAL', "IT'S", 'CORN', 'PASTAVILLA', 'UNSALTED', 'WELL', 'HNT', 'SALT']






for Find_Value in split_list: # 이중루프로 리스트 마다 해당하는 값을 찾음

    Find_Value.strip()    # 양쪽 공백 제거

    # weight and Count 有
    if 'COUNT' in Find_Value:
        break

    for PACKGES in Find_PACKAGES:   # Find_PACKAGES에 해당하는 값이 포함되어 있으면 PACKGES에 포함된 값 저장

        # if PACKAGES_list:   # PACKAGES_list에 값이 존재 시 루프 탈출 (현재는 하나의 값만 가져오기 위해 설정)
        #     break

        if 'WITH' in Find_Value:
            continue

        if PACKGES in Find_Value: # Find_Value에 PACKGES의 포함된 값이 있을경우 

            find_Gap = Find_Value.find(PACKGES) # find_Gap에 인덱스 저장 (Find_PACKAGES의 포함된 리스트 값 제거)
            Find_Value = Find_Value.replace('I','1')    # 1을 I로 읽었을 경우 바꿔줌
            pattern = r"\d{0,}\s{0,}"+ re.escape(PACKGES)  # 숫자 최소 0개 문자 최소 0개의 PACKAGE_LIST의 해당하는 값의 패턴
            matches = re.findall(pattern, Find_Value)   # 찾은 패턴을 matches에 리스트 형태로 저장
            matches = matches[0].replace(PACKGES,'')    # matches의 첫번째 리스트 값의 PACKGES의 값 제거 (예시) 1060CARTONS -> 1060
            PACKAGES_list.append(matches) # PACKAGES_list에 제외 문구 전까지의 값 저장

         #   PACKAGES_list.append(Find_Value)


    for DESCRIPTIONOFGOODS in Find_DESCRIPTIONOFGOODS:  # Find_DESCRIPTIONOFGOODS 리스트 수만큼 루프
        if DESCRIPTIONOFGOODS_list: # 값이 있으면 for문 끝내기
            break

        if DESCRIPTIONOFGOODS in Find_Value:    # Find_DESCRIPTIONOFGOODS에 해당 값이 같으면 DESCRIPTIONOFGOODS에 값 저장

            # if Find_Value not in DESCRIPTIONOFGOODS_list:  # 중복 항목을 추가하지 않도록 확인
            #     DESCRIPTIONOFGOODS_list.append(Find_Value)
                for EXCEPT_word in EXCEPT_LIST: # 제외 키워드 확인 후 값 해당하는 값 지우기
                    if DESCRIPTIONOFGOODS_list: # 값이 있으면 for문 끝내기
                         break

                    elif EXCEPT_word in Find_Value: # Find_Value에 제외키워드가 포함시 제거
                        Find_Value = Find_Value.replace(EXCEPT_word,'') # 해당하는 제외 리스트가 있을 경우 공백으로 제거
                        Find_Value = Find_Value.strip() # 양쪽 공백 제거
                        DESCRIPTIONOFGOODS_list.append(Find_Value)  # DESCRIPTIONOFGOODS_list 값 저장
                    else:   # if문을 안타면 다음 값 실행
                        continue
                    
                if len(DESCRIPTIONOFGOODS_list) == 0:   # 제외키워드를 못타고 값을 못 받을 시
                    DESCRIPTIONOFGOODS_list.append(Find_Value)


                    # break

# 컨테이너가 2대 이상일 경우 첫번쨰 같은 나머지 값의 합친 값이며 그 값을 제거
# if len(PACKAGES_list) != 1: 
#     del PACKAGES_list[0]



if DESCRIPTIONOFGOODS_list: # DESCRIPTIONOFGOODS_list의 값이 여러개가 존재 할때 ,로 구분하여 field_value['DESCRIPTIONOFGOODS']에 저장

    # i = 0

    # for x in DESCRIPTIONOFGOODS_list:

    #     if i == 0:

    #         field_value['DESCRIPTIONOFGOODS'] = x

    #     else:

    #         field_value['DESCRIPTIONOFGOODS'] = field_value['DESCRIPTIONOFGOODS'] + ',' + x

    #     i += 1

    field_value["DESCRIPTIONOFGOODS"] = DESCRIPTIONOFGOODS_list

# 값이 없을 경우 N/A로 값 지정 (만약 현업에서 N/A로 나오지 않으면 else 부분 삭제 및 주석으로 처리하면 됨)
else:

    field_value["DESCRIPTIONOFGOODS"] = 'N/A'




if PACKAGES_list:   #PACKAGES_list의 값이 여러개가 존재 할때 ,로 구분하여 field_value['PACKAGES']에 저장

    # i = 0

    # for x in PACKAGES_list:

    #     if i == 0:

    #         field_value['PACKAGES'] = x

    #     else:

    #         field_value['PACKAGES'] = field_value['PACKAGES'] + ',' + x

    #     i += 1

    field_value["PACKAGES"] = PACKAGES_list

# 값이 없을 경우 N/A로 값 지정 (만약 현업에서 N/A로 나오지 않으면 else 부분 삭제 및 주석으로 처리하면 됨)
else:

    field_value["PACKAGES"] = 'N/A'