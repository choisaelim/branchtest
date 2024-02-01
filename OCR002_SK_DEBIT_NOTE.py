field_value = {}    # field_value 딕셔너리 선언
field_value['DESCRIPTION'] = '' # field_value key값 DESCRIPTION
field_value['BASE_ON'] = ''  # field_value key값 BASE_ON
field_value['RATE'] = ''    # field_value key값 RATE
field_value['CUR'] = '' # field_value key값 CUR
field_value['AMOUNT'] = ''  # field_value key값 AMOUNT
field_value['EX-Rate'] = '' # field_value key값 EX-Rate

list_size = len(inputOcr_list)  # inputOcr_list의 길이를 list_size에 저장

if list_size > 6:   # list_size가 2보다 클 경우 if문 실행
    for line,no,confidence,text,lang,x1,y1,x2,y2,page_no in inputOcr_list:    # inputOcr_list 인덱스 수 만큼 for문 실행
        try:    
            if'TOTAL' in text or 'DEBIT' in text :
                field_value['DESCRIPTION'] = ''
                field_value['BASE_ON'] = ''
                field_value['RATE'] = ''
                field_value['CUR'] = ''
                field_value['AMOUNT'] = ''
                field_value['EX-Rate'] = ''
                break
            elif no == 0: # no가 0일 경우
                find_idx = text.find('(')   # text에 '('가 존재시 find_idx로 인덱스 값 저장 없을 경우 -1로 나옴
                if find_idx != -1:  # find_idx값이 -1이 아닐 경우
                    field_value['DESCRIPTION'] = text[0:find_idx]   # field_value['DESCRIPTION']에 text 0부터 find_idx까지의 글자 저장
                else:    
                    field_value['DESCRIPTION'] = text   # field_value에 text 값 저장
        except:
            field_value['DESCRIPTION'] = ''

        try:
            if no == 1:   # no가 1일 경우
                field_value['BASE_ON'] = text   # BASE_ON 키에 value 값 저장
        except:
            field_value['BASE_ON'] = ''

        try:  
            if no == 2:   # no가 2일 경우
                field_value['RATE'] = text  # RATE 키에 value 값 저장
        except:
            field_value['RATE'] = ''

        try:
            if no == 3:   # no가 3일 경우
                field_value['CUR'] = text   # CUR 키에 value 값 저장
        except:
            field_value['CUR'] = ''

        try:
            if no == 4:   # no가 4일 경우
                field_value['AMOUNT'] = text    # AMOUNT 키에 value 값 저장
        except:
            field_value['AMOUNT'] = ''

        try:
            if no == 5:   # no가 5일 경우
                field_value['EX-Rate'] = text   # EX-Rate 키에 value 값 저장
        except:
            field_value['EX-Rate'] = ''