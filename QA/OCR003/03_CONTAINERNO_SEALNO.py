inputOcr = ''

# 설명 : 해당 CONTAINER NUMBER와 SEAL NUMBER을 구하기



def ReplaceToBlank(find_row_text, text):
    try:
        for t in text:   
            find_row_text = find_row_text.replace(t, "")
    except:
        pass   

    return find_row_text

# inputOcr 값 가공
def test(inputOcr):
    list_row = inputOcr.split('\n')  #개행문자로 각 줄을 list로 전환
    
    # 결과값을 담을 딕셔너리 선언
    return_value = {} # 딕셔너리 선언
    return_value['CONTAINERNO'] = '' # 다중 필드 1 선언
    return_value['SEALNO'] = '' # 다중 필드 1 선언

    # 결과값을 담을 리스트 선언
    list_CONTAINERNO = []
    list_SEALNO = []

    # enumerate를 이용하여 CONTAINER NUMBER와 SEAL NUMBER을 구하기
    for idx, find_row_text in enumerate(list_row):

        # 전 문장 담아두기
        if idx == 0:
            before_find_row_text = find_row_text

        # list_row -1 의 길이가 idx 랑 같을 경우
        elif len(list_row)-1 == idx:
            before_find_row_text = find_row_text

        # 모든 조건이 성립하지 않을 경우
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
        find_row_text = find_row_text.replace('0022C004095','002AC004095')
        find_row_text = find_row_text.replace('0021W000056','002IW000056')

        # 정규식 패턴(2)
        p_CONTAINERNO = r"[0-9]?[A-Z]{4}\s?[A-Z]?[0-9]{7}" # WHSU6111902(문자4, 숫자7)
        # p_SEALNO = r"\d{7,9}|[^PO: /()a-z][A-Z]{2,3}\d{6,7}" # SM492952(문자2, 숫자6), 211393091(숫자 9), JPC586297(문자3, 숫자6) 'PO' 문자 제외
        p_SEALNO = r"[A-Z]{2}\d{7}|[A-Z]{3}\d{6,8}|\d{3}[A-Z]{2}\d{6}|\d{6,7}" 

        # CONTAINERNO
    
        if "containerno" in find_row_text.lower().replace(" ", ""): # find_row_text를 소문자 변환, 띄어쓰기 공백으로 제거, containerno가 포함된 단어가 있을 경우 
            p_CONTAINERNO = r"Container\s?No\s?:\s[0-9]?[A-Z]{4}[A-Z]?[0-9]{7}" # 정규식(문자 4개, 숫자 7개)
            t_CONTAINERNO = re.compile(p_CONTAINERNO).findall(find_row_text)    # compile : 매칭되는 패턴 찾기, findall : 매칭된 패턴을 리스트 형태로 t_CONTAINERNO에 저장
            for i in range(len(t_CONTAINERNO)): # t_CONTAINERNO의 길이 범위만큼 루프수행
                
                # Container No:와 그 주변의 공백 문자를 찾아 해당 부분을 빈 문자열로 대체
                t_CONTAINERNO[i] = re.sub(r"Container\s?No\s?:","",t_CONTAINERNO[i])
                
                # t_CONTAINERNO의 요소를 list_CONTAINERNO에 한번에 추가    
                list_CONTAINERNO.extend(t_CONTAINERNO)  

        elif re.compile(r"[0-9]?[A-Z]{4}[A-Z]?[0-9]{7}\s?\/\s?\w+?\d+-?\d{2}").match(find_row_text) != None:    # 주어진 정규 표현식 패턴과 일치하는 경우 해당 패턴을 찾아 t_CONTAINERNO 변수에 저장
            t_CONTAINERNO = re.compile(r"[0-9]?[A-Z]{4}[A-Z]?[0-9]{7}\s?\/\s?\w+?\d+-?\d{2}").match(find_row_text).group()
            
            # "/"를 기준으로 문자열을 분리하여 list_tmp에 저장
            list_tmp = t_CONTAINERNO.split("/")

            # 분리된 요소들을 각각의 리스트(list_CONTAINERNO, list_SEALNO)에 추가
            list_CONTAINERNO.append(list_tmp[0])
            list_SEALNO.append(list_tmp[1])

            #find_row_text에서 t_CONTAINERNO를 빈 문자열로 대체
            find_row_text = ReplaceToBlank(find_row_text, t_CONTAINERNO)

            # list_tmp 값 초기화
            list_tmp = []
        
        else:
            t_CONTAINERNO = re.compile(p_CONTAINERNO).findall(find_row_text)
            if len(t_CONTAINERNO) != 0: # 빈 값 덮어쓰기 방지

                # find_row_text에서 t_CONTAINERNO를 빈 문자열로 대체
                find_row_text = ReplaceToBlank(find_row_text, t_CONTAINERNO)
                # t_CONTAINERNO를 list_CONTAINERNO에 추가
                list_CONTAINERNO.extend(t_CONTAINERNO)

        # SEALNO
    
        if "sealno" in find_row_text.lower().replace(" ", ""): # SEAL NO : ~~
            p_SEALNO = r"Seal\s?No\s?:\s?\d{7,9}|[^PO: /()][A-Z]{2,3}\d{7}"
            t_SEALNO = re.compile(p_SEALNO).findall(find_row_text)
            for i in range(len(t_SEALNO)):
                t_SEALNO[i] = re.sub(r"Seal\s?No\s?:","",t_SEALNO[i])
                list_SEALNO.extend(t_SEALNO)
        
        elif "seal:" in before_find_row_text.lower().replace(" ", ""):
            t_SEALNO = re.compile(p_SEALNO).findall(find_row_text)
            list_SEALNO.extend(t_SEALNO)
        
        # 4011508099 숫자 10자리 예외처리
        elif re.compile(r"\d{10}").match(find_row_text) != None:
            pass

        else:
            t_SEALNO = re.compile(p_SEALNO).findall(find_row_text)
            if len(t_SEALNO) != 0: # 빈 값 덮어쓰기 방지
                if int(len(list_row)*0.9) > idx or idx < 5:
                    list_SEALNO.extend(t_SEALNO)
            # find_row_text = ReplaceToBlank(find_row_text, t_SEALNO)

        # 예외case1
        if "referencenumber" in find_row_text.lower().replace(" ", ""):
            for t in t_SEALNO:
                list_SEALNO.remove(t)
        # 예외case2
        if "NUMBER" in find_row_text.upper().replace(" ", ""): 
            for t in t_SEALNO:
                list_SEALNO.remove(t)
        # 예외case3
        if "EXPORTER" in find_row_text.upper().replace(" ", ""): 
            for t in t_SEALNO:
                list_SEALNO.remove(t)

    # 리스트 안에 있는 요소의 공백 제거
    list_CONTAINERNO = [i.strip().replace(" ","") for i in list_CONTAINERNO]
    list_SEALNO = [i.strip().replace(" ","") for i in list_SEALNO]

    # 리스트에 중복된 값 제거 (정렬X)
    val_CONTAINERNO = list(dict.fromkeys(list_CONTAINERNO))
    val_SEALNO = list(dict.fromkeys(list_SEALNO))

    # # 딕셔너리에 값 넣기(중복 제거)
    # val_CONTAINERNO = ",".join(list(set(list_CONTAINERNO)))
    # val_SEALNO = ",".join(list(set(list_SEALNO)))

    # return_value['CONTAINERNO'] = val_CONTAINERNO.replace(" ","")

    return_value['CONTAINERNO'] = val_CONTAINERNO
    return_value['SEALNO'] = val_SEALNO    

    return return_value

field_value = test(inputOcr)