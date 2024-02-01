import re

field_value = {}    # field_value 딕셔너리 선언
field_value['06_DESCRIPTION'] = '' 
field_value['06_UNIT'] = ''  
field_value['06_RATE'] = ''  
field_value['06_QTY'] = '' 
field_value['06_DEBIT'] = '' 
field_value['06_CREDIT'] = '' 

test = '1,300'
test = re.sub(r'^P/S\s+:.*','P/S :',test)
test = test.replace(',','') #, 제거

list_size = len(inputOcr_list)  # inputOcr_list의 길이를 list_size에 저장

passline = ''
container_pattern = r"\-\w{3}U\d{7}"
bracket_pattern = r"\s\((.*)\)"
date_pattern = r"\s\w{0,2}\/\w{0,2}\-\w{0,2}\/\w{0,2}"

if list_size > 0:   # list_size가 2보다 클 경우 if문 실행
    for line,no,confidence,text,lang,x1,y1,x2,y2,page_no in inputOcr_list:    # inputOcr_list 인덱스 수 만큼 for문 실행
        if passline != '' and line == passline:
            field_value['06_DESCRIPTION'] = ''
            field_value['06_RATE'] = ''
            field_value['06_QTY'] = ''
            field_value['06_DEBIT'] = ''
            field_value['06_UNIT'] = ''
            field_value['06_CREDIT'] = ''
            continue
        try: 
            if 'TOTAL' in text :
                field_value['06_DESCRIPTION'] = ''
                field_value['06_RATE'] = ''
                field_value['06_QTY'] = ''
                field_value['06_DEBIT'] = ''
                field_value['06_UNIT'] = ''
                field_value['06_CREDIT'] = ''
                break
            elif no == 0: # no가 0일 경우
                passline = ''
                #괄호, 날짜형식, 컨테이너를 치환으로 없앰
                text = re.sub(container_pattern, r"", text)
                text = re.sub(bracket_pattern, r"", text)
                text = re.sub(date_pattern, r"", text)
                if "CONTAINER DRAYAGE FEE" in text or "HANDLING CHARGE TO AGENT" in text or "ISF FILING FEE" in text:
                    passline = line
                    field_value['06_RATE'] = ''
                    field_value['06_QTY'] = ''
                    field_value['06_DEBIT'] = ''
                    field_value['06_UNIT'] = ''
                    field_value['06_CREDIT'] = ''
                    continue
                field_value['06_DESCRIPTION'] = text   # field_value에 text 값 저장
        except:
            field_value['06_DESCRIPTION'] = ''

        try:
            if no == 1:   # no가 1일 경우
                field_value['06_RATE'] = text   # RATE 키에 value 값 저장
        except:
            field_value['06_RATE'] = ''

        try:  
            if no == 2:   # no가 2일 경우
                field_value['06_QTY'] = text  # QTY 키에 value 값 저장
        except:
            field_value['06_QTY'] = ''

        try:  
            if no == 3:   # no가 3일 경우
                if text != 'c': #4번째 열 P/C에서 c가 인식되어야 하는데 아닌 경우 Rate, QTY가 한칸씩 밀린 경우가 있어 수정
                    field_value['06_RATE'] = field_value['06_QTY']
                    field_value['06_QTY'] = text
        except:
            field_value['06_QTY'] = ''

        try:
            if no == 4:   # no가 4일 경우
                field_value['06_DEBIT'] = text   # DEBIT 키에 value 값 저장
                field_value['06_UNIT'] = 'B/L'
                field_value['06_CREDIT'] = '0'
        except:
            field_value['06_DEBIT'] = ''
            field_value['06_UNIT'] = ''
            field_value['06_CREDIT'] = ''