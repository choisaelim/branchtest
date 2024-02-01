inputOcr = '''21617.040
KGM
55.000
MTQ
'''

inputOcr = '''21617.040
KGM
'''

import re

# HAPAG GROSSWEIGHT, MEASURMENT 구하기
def ReplaceToBlank(find_row_text, text):
    
    if type(text) == list:
        try:
            for t in text:   
                find_row_text = find_row_text.replace(t, "")
        except:
            pass   

    elif type(text) == str:
        find_row_text = find_row_text.replace(text, "")

    return find_row_text


def test(inputOcr):
    inputOcr = inputOcr.replace(",",".")
    list_row = inputOcr.split('\n')  #개행문자로 각 줄을 list로 전환
    # 결과값을 담을 딕셔너리 선언
    return_value = {} # 딕셔너리 선언
    return_value['GROSSWEIGHT'] = '' 
    return_value['MEASUREMENT'] = '' 

    # 결과값을 담을 리스트 선언
    list_GROSSWEIGHT = []
    list_MEASUREMENT = []

    # 값을 찾기 위한 기준들을 담은List
    UnitList_GROSSWEIGHT = ["KGS", "LBS", "KGM", "NET"] # GROSSWEIGHT 리스트
    UnitList_MEASUREMENT = ["CBM", "CUM", "MTQ", "M3"]  # MEASUREMENT 리스트

    for idx, find_row_text in enumerate(list_row):
        # if len(list_GROSSWEIGHT) != 0 and len(list_MEASUREMENT) != 0:   # 가장 최상단의 중량 가져오기 위해서 만듬(한개만 가져오기 위해 추가)
        #     break

        before_find_row_text = ""

        # 전 문장 담아두기
        if idx == 0:
            pass
            
        else:
            before_find_row_text = list_row[idx-1]

        # 필요한 정보를 잘못 읽을 수 있기 때문에 replace
        find_row_text = find_row_text.replace('H&','HQ')
        find_row_text = find_row_text.replace('HC','HQ')
        find_row_text = find_row_text.replace(' HQ','HQ')
        find_row_text = find_row_text.replace(' DRY','DRY')
        find_row_text = find_row_text.replace('\"','\'')
        find_row_text = find_row_text.replace('○','O')
        find_row_text = find_row_text.replace('X2O\'GP','X20GP')
        find_row_text = find_row_text.replace('X2O\'DV','X20DV')
        find_row_text = find_row_text.replace('cu. m.','cum')
        find_row_text = find_row_text.replace('YGM','KGM')
        find_row_text = find_row_text.replace('MTO','MTQ')
        find_row_text = find_row_text.replace('NET KGS','NET') # 마지막에 NET KGS 로 다시 바꿔주기
        find_row_text = find_row_text.replace('KGMTQ','KXXMTQ') # 2차 반복문에서 처리

        # print(f"idx : {idx} // find_row_text : {find_row_text} // before_find_row_text : {before_find_row_text} ")

        # GROSSWEIGHT, MEASUREMENT
        # 단위(WEIGHT : KGS, VOLUME : CBM 이 있을 경우)

        #소수점 세 자릿수인 숫자 형식
        p_GROSSWEIGHT = r"\d+[.,]\s?\d{3}|\d+[.,]\s?\d{1}"
        p_MEASUREMENT = r"\d+[.,]\d{3}|\d+[.,]\d{1}"

        for weight in UnitList_GROSSWEIGHT:
            if weight in find_row_text:
                t_GROSSWEIGHT = re.compile(p_GROSSWEIGHT).findall(find_row_text)
                if len(t_GROSSWEIGHT) == 0: # ex) 123456.000kgs 가 아닐 경우
                    t_GROSSWEIGHT = re.compile(p_GROSSWEIGHT).findall(before_find_row_text) # 이전문장에서 찾기

                    # t_GROSSWEIGHT 에 weight + volume 값이 들어갈때
                    if len(t_GROSSWEIGHT) == 2:
                        list_GROSSWEIGHT.append(t_GROSSWEIGHT[0]+weight)
                        # del t_GROSSWEIGHT[1]
                        before_find_row_text = ReplaceToBlank(before_find_row_text, t_GROSSWEIGHT[0])

                        for volume in UnitList_MEASUREMENT:
                            if volume in find_row_text:
                                t_MEASUREMENT = re.compile(p_MEASUREMENT).findall(before_find_row_text)
                                # before_find_row_text = ReplaceToBlank(before_find_row_text, t_MEASUREMENT)
                                t_MEASUREMENT[0] += volume
                                list_MEASUREMENT.extend(t_MEASUREMENT)
                            
                    # t_GROSSWEIGHT 에 weight 값만 들어갈때
                    elif len(t_GROSSWEIGHT) == 1:
                        t_GROSSWEIGHT[0] += weight
                        list_GROSSWEIGHT.append(t_GROSSWEIGHT[0])
                        before_find_row_text = ReplaceToBlank(before_find_row_text, t_GROSSWEIGHT[0])
                
                else:
                    pass
    # print(f"list_GROSSWEIGHT : {list_GROSSWEIGHT} // {len(list_GROSSWEIGHT)}")
    if len(list_GROSSWEIGHT) == 0: # 단위가 없어서
        before_find_row_text = ""

        # 전 문장 담아두기
        if idx == 0:
            pass
            
        else:
            before_find_row_text = list_row[idx-1] 

        UnitList_Except = ["KG"] # 기타 단위(여기서는 KGS KGM KG 가 겹치므로 KG를 따로 뺐음)

        for idx, find_row_text in enumerate(list_row):
            for e_weight in UnitList_Except:
                if e_weight in find_row_text:
                    t_GROSSWEIGHT = re.compile(p_GROSSWEIGHT).findall(find_row_text)
                    print(f"t_GROSSWEIGHT : {t_GROSSWEIGHT}")
                    if len(t_GROSSWEIGHT) == 0: # ex) 123456.000kgs 가 아닐 경우
                        print(f"before_find_row_text : {before_find_row_text}")
                        t_GROSSWEIGHT = re.compile(p_GROSSWEIGHT).findall(before_find_row_text) # 이전문장에서 찾기

                        # t_GROSSWEIGHT 에 weight + volume 값이 들어갈때
                        if len(t_GROSSWEIGHT) == 2:
                            list_GROSSWEIGHT.append(t_GROSSWEIGHT[0]+e_weight)
                            # del t_GROSSWEIGHT[1]
                            before_find_row_text = ReplaceToBlank(before_find_row_text, t_GROSSWEIGHT[0])

                            for volume in UnitList_MEASUREMENT:
                                if volume in find_row_text:
                                    t_MEASUREMENT = re.compile(p_MEASUREMENT).findall(before_find_row_text)
                                    # before_find_row_text = ReplaceToBlank(before_find_row_text, t_MEASUREMENT)
                                    t_MEASUREMENT[0] += volume
                                    list_MEASUREMENT.extend(t_MEASUREMENT)
                                
                        # t_GROSSWEIGHT 에 weight 값만 들어갈때
                        elif len(t_GROSSWEIGHT) == 1:
                            t_GROSSWEIGHT[0] += e_weight
                            list_GROSSWEIGHT.append(t_GROSSWEIGHT[0])
                            before_find_row_text = ReplaceToBlank(before_find_row_text, t_GROSSWEIGHT[0])
                    
                    else:
                        pass

    # 딕셔너리에 값 넣기(중복 제거)
    # print(f"list_GROSSWEIGHT : {list_GROSSWEIGHT}")
#============================================
    # list_GROSSWEIGHT = list(set(list_GROSSWEIGHT))
    # return_value['GROSSWEIGHT'] = list_GROSSWEIGHT
    # #return_value['GROSSWEIGHT'] = return_value['GROSSWEIGHT'].replace(",",".")
    # return_value['GROSSWEIGHT'] = re.sub(r"[^\d.]",'',return_value['GROSSWEIGHT'])

    # for val in list_GROSSWEIGHT:
    #     if len(val) < 5 or len(val) > 11:
    #         list_GROSSWEIGHT.remove(val)
#======================================
#     list_MEASUREMENT = list(set(list_MEASUREMENT))
#     return_value['MEASUREMENT'] = list_MEASUREMENT
#    # return_value['MEASUREMENT'] = return_value['MEASUREMENT'].replace(",",".")
#     return_value['MEASUREMENT'] = re.sub(r"[^\d.]",'',return_value['MEASUREMENT'])
#=======================================
#     # for val in list_MEASUREMENT:
    #     if len(val) < 5 or len(val) > 11:
    #         list_MEASUREMENT.remove(val)

    # for i in range(len(list_GROSSWEIGHT)):
    #     if "NET" in list_GROSSWEIGHT[i]:
    #         list_GROSSWEIGHT[i] = list_GROSSWEIGHT[i].replace("NET", "NET KGS")


    # 중량이 두개 이상일 경우 맨 처음값 삭제(첫번째 값은 합한 값이기 때문)
    #if list_MEASUREMENT != 1:
        #del list_MEASUREMENT[0]
    #if list_GROSSWEIGHT != 1:
        #del list_GROSSWEIGHT[0]

    # 중복값 제거
    list_GROSSWEIGHT = dict.fromkeys(list_GROSSWEIGHT)
    list_MEASUREMENT = dict.fromkeys(list_MEASUREMENT)

    list_GROSSWEIGHT = "!".join(list_GROSSWEIGHT)    # join 부분에서 !로 구분하기 위해 사용
    list_MEASUREMENT = "!".join(list_MEASUREMENT)

    list_GROSSWEIGHT = list_GROSSWEIGHT.replace(",",".").replace('!',',') # 리스트 값 넣기전 ,를 .으로 고치고 !를 ,로 변경
    list_MEASUREMENT = list_MEASUREMENT.replace(",",".").replace('!',',') # 리스트 값 넣기전 ,를 .으로 고치고 !를 ,로 변경

    # 숫자와 ',', '.'를 제외한 나머지 문자 제거
    list_GROSSWEIGHT = re.sub(r"[^\d.,]",'',list_GROSSWEIGHT) 
    list_MEASUREMENT = re.sub(r"[^\d.,]",'',list_MEASUREMENT)

    # ','를 기준으로 split 후 list 화
    list_GROSSWEIGHT = list_GROSSWEIGHT.split(',')
    list_MEASUREMENT = list_MEASUREMENT.split(',')

    res_MESUREMENT = []
    for str in list_MEASUREMENT :
        #공백이면 0으로 처리
        if len(str) == 0:
            str = '0'
        res_MESUREMENT.append(str)
    # 딕셔너리 선언
    return_value['GROSSWEIGHT'] = list_GROSSWEIGHT
    return_value['MEASUREMENT'] = res_MESUREMENT


    # return_value['GROSSWEIGHT'] = val_GROSSWEIGHT.replace(",",".").replace('!',',') # 리스트 값 넣기전 ,를 .으로 고치고 !를 ,로 변경
    # return_value['MEASUREMENT'] = val_MEASUREMENT.replace(",",".").replace('!',',') # 리스트 값 넣기전 ,를 .으로 고치고 !를 ,로 변경


    # # 숫자와 ',', '.'를 제외한 나머지 문자 제거
    # return_value['GROSSWEIGHT'] = re.sub(r"[^\d.,]",'',return_value['GROSSWEIGHT']) 
    # return_value['MEASUREMENT'] = re.sub(r"[^\d.,]",'',return_value['MEASUREMENT'])


    return return_value
    


field_value = test(inputOcr)
'''
field_value = {}
field_value['GROSSWEIGHT'] = inputOcr
field_value['MEASUREMENT'] = inputOcr
'''