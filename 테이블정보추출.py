# inputOcr : OCR이 읽은 초기값 
# inputOcr_list : OCR엔진이 읽은 정보 List[line, no, confidence, text, lang,x1,y1,x2,y2,page_no] 정보,
#field_value:후처리 후 결과 값(반드시 최종 결과 변수로 지정해야 함)
#간단한 sample
#다중 필드 생성시에는 dictionary로 정의 
 #field_value = {}
#field_value['SHIPPER_NAME'] = 'test1' 
#field_value['SHIPPER_ADDRESS'] = 'Seoul,Korea' 
#inputOcr=inputOcr.replace('대줄','대출')
#field_value=inputOcr

import re

#초기화
field_value = {}    # field_value 딕셔너리 선언
field_value['06_DESCRIPTION'] = '' 
field_value['06_UNIT'] = ''  
field_value['06_RATE'] = ''  
field_value['06_QTY'] = '' 
field_value['06_DEBIT'] = '' 
field_value['06_CREDIT'] = '' 

list_size = len(inputOcr_list)  # inputOcr_list의 길이를 list_size에 저장

if list_size > 0:   # list_size가 2보다 클 경우 if문 실행
    for line,no,confidence,text,lang,x1,y1,x2,y2,page_no in inputOcr_list:    # inputOcr_list 인덱스 수 만큼 for문 실행  
        try:   
            if 'TOTAL' in text :
                field_value['06_DESCRIPTION'] = ''
                field_value['06_RATE'] = ''
                field_value['06_QTY'] = ''
                field_value['06_DEBIT'] = ''
                field_value['06_UNIT'] = ''
                field_value['06_CREDIT'] = ''
                break 
            else:
                if line == 4:
                    tmp = str(text)+' '+str(line)+' '+str(no)+' '+str(x1)
                    if no == 0:
                        field_value['06_DESCRIPTION'] = tmp
                    if no == 1:
                        field_value['06_RATE'] = tmp
                    if no == 2:
                        field_value['06_QTY'] = tmp
                    if no == 3:
                        field_value['06_CREDIT'] = tmp
                    if no == 4:
                        field_value['06_DEBIT'] = tmp
                        field_value['06_UNIT'] = 'B/L'

        except:
            field_value['06_DESCRIPTION'] = ''
            field_value['06_RATE'] = ''
            field_value['06_QTY'] = ''
            field_value['06_DEBIT'] = ''
            field_value['06_UNIT'] = ''
            field_value['06_CREDIT'] = ''