field_value = {}    # field_value 딕셔너리 선언

Extract_list = []   # 리스트 선언

field_value['01_DESCRIPTION_OF_CHARGES'] = '' # field_value key값 DESCRIPTION
field_value['01_CURR'] = ''  # field_value key값 BASE_ON
field_value['01_EX.RATE'] = ''    # field_value key값 RATE
field_value['01_RATE'] = '' # field_value key값 CUR
field_value['01_QTY'] = ''  # field_value key값 AMOUNT
field_value['01_DEBIT'] = '' # field_value key값 EX-Rate
field_value['01_CREDIT'] = ''


# 필요없는 공백 값이 row에 있을시 그 줄은 제거
i = 0
for line, no, confidence, text, lang, x1, y1, x2, y2, page in inputOcr_list:
    if '' == text and inputOcr_list[i] < inputOcr_list[5]:
        del inputOcr_list[i]
        i += 1
    else:
        i += 1


inputOcr_list[0][3] = re.sub(r'^P/S\s+:.*','P/S :',inputOcr_list[0][3])

if len(inputOcr_list) == 5 :
        try:
            field_value['01_DESCRIPTION_OF_CHARGES'] = inputOcr_list[0][3]
        except:
            field_value['01_DESCRIPTION_OF_CHARGES'] = ''
        try:
            field_value['01_CURR'] = inputOcr_list[1][3]
        except:
            field_value['01_CURR'] = ''
        try:
            field_value['01_EX.RATE'] = inputOcr_list[2][3]
        except:
            field_value['01_EX.RATE'] = ''
        try:
            # 추출값이 같이 나오는 경우 발생
            if ' ' in inputOcr_list[3][3]:
                Extract_value = inputOcr_list[3][3]
                Extract_list = Extract_value.split(' ')
                field_value['01_RATE'] = Extract_list[0]
            else:
                field_value['01_RATE'] = '후처리 에러 입니다.'
        except:
            field_value['01_RATE'] = ''
        try:
            field_value['01_QTY'] = Extract_list[1]
        except:
            field_value['01_QTY'] = ''
        try:
            if '' == inputOcr_list[4][3]:
                field_value['01_DEBIT'] = '0'
            else:
                field_value['01_DEBIT'] = inputOcr_list[4][3].replace(',','') #, 제거
        except:
            field_value['01_DEBIT'] = '0'
        try:
            if '' == inputOcr_list[5][3]:
                field_value['01_CREDIT'] = '0'
            else:
                field_value['01_CREDIT'] = inputOcr_list[5][3].replace(',','') #, 제거
        except:
            field_value['01_CREDIT'] = '0'
    

elif len(inputOcr_list) == 6 :
    try:
        field_value['01_DESCRIPTION_OF_CHARGES'] = inputOcr_list[0][3]
    except:
        field_value['01_DESCRIPTION_OF_CHARGES'] = ''
    try:
        field_value['01_CURR'] = inputOcr_list[1][3]
    except:
        field_value['01_CURR'] = ''
    try:
        field_value['01_EX.RATE'] = inputOcr_list[2][3]
    except:
        field_value['01_EX.RATE'] = ''
    try:
        field_value['01_RATE'] = inputOcr_list[3][3].replace(',','') #, 제거
    except:
        field_value['01_RATE'] = ''
    try:
        field_value['01_QTY'] = inputOcr_list[4][3].replace(',','')
    except:
        field_value['01_QTY'] = ''
    # try:
    #     field_value['01_DEBIT'] = inputOcr_list[5][3]
    # except:
    #     field_value['01_DEBIT'] = ''
    # try:
    #     field_value['01_CREDIT'] = '0'
    # except:
    #     field_value['01_CREDIT'] = '0'
    try:
        if '' == inputOcr_list[5][3]:
            field_value['01_DEBIT'] = '0'
        else:
            field_value['01_DEBIT'] = inputOcr_list[5][3].replace(',','') #, 제거
    except:
        field_value['01_DEBIT'] = '0'
    try:
        if '' == inputOcr_list[6][3]:
            field_value['01_CREDIT'] = '0'
        else:
            field_value['01_CREDIT'] = inputOcr_list[6][3].replace(',','') #, 제거
    except:
        field_value['01_CREDIT'] = '0'

elif len(inputOcr_list) == 7:
    try:
        field_value['01_DESCRIPTION_OF_CHARGES'] = inputOcr_list[0][3]
    except:
        field_value['01_DESCRIPTION_OF_CHARGES'] = ''
    try:
        field_value['01_CURR'] = inputOcr_list[1][3]
    except:
        field_value['01_CURR'] = ''
    try:
        field_value['01_EX.RATE'] = inputOcr_list[2][3]
    except:
        field_value['01_EX.RATE'] = ''
    try:
        field_value['01_RATE'] = inputOcr_list[3][3].replace(',','') #, 제거
    except:
        field_value['01_RATE'] = ''
    try:
        field_value['01_QTY'] = inputOcr_list[4][3].replace(',','')
    except:
        field_value['01_QTY'] = ''
    try:
        if '' == inputOcr_list[5][3]:
            field_value['01_DEBIT'] = '0'
        else:
            field_value['01_DEBIT'] = inputOcr_list[5][3].replace(',','') #, 제거
    except:
        field_value['01_DEBIT'] = '0'
    try:
        if '' == inputOcr_list[6][3]:
            field_value['01_CREDIT'] = '0'
        else:
            field_value['01_CREDIT'] = inputOcr_list[6][3].replace(',','') #, 제거
    except:
        field_value['01_CREDIT'] = '0'


elif len(inputOcr_list) == 8:
    try:
        field_value['01_DESCRIPTION_OF_CHARGES'] = inputOcr_list[0][3]
    except:
        field_value['01_DESCRIPTION_OF_CHARGES'] = ''
    try:
        field_value['01_CURR'] = inputOcr_list[1][3]
    except:
        field_value['01_CURR'] = ''
    try:
        field_value['01_EX.RATE'] = inputOcr_list[2][3]
    except:
        field_value['01_EX.RATE'] = ''
    try:
        field_value['01_RATE'] = inputOcr_list[3][3].replace(',','')
    except:
        field_value['01_RATE'] = ''
    try:
        field_value['01_QTY'] = inputOcr_list[4][3].replace(',','')
    except:
        field_value['01_QTY'] = ''
    try:
        if '' == inputOcr_list[5][3]:
            field_value['01_DEBIT'] = '0'
        else:
            field_value['01_DEBIT'] = inputOcr_list[5][3].replace(',','') #, 제거
    except:
        field_value['01_DEBIT'] = '0'
    try:
        if '' == inputOcr_list[6][3]:
            field_value['01_CREDIT'] = '0'
        else:
            field_value['01_CREDIT'] = inputOcr_list[6][3].replace(',','') #, 제거
    except:
        field_value['01_CREDIT'] = '0'
else:
    field_value['01_DESCRIPTION_OF_CHARGES'] = '후처리 에러 입니다.'
    field_value['01_CURR'] = '후처리 에러 입니다.'  
    field_value['01_EX.RATE'] = '후처리 에러 입니다.'   
    field_value['01_RATE'] = '후처리 에러 입니다.' 
    field_value['01_QTY'] = '후처리 에러 입니다.' 
    field_value['01_DEBIT'] = '후처리 에러 입니다.' 
    field_value['01_CREDIT'] = '후처리 에러 입니다.'