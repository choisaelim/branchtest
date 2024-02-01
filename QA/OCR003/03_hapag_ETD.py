# ETD 구하는 로직

import re

# inputOcr = '10.0CT.2023'
inputOcr = inputOcr.upper()     # 대문자로 변경

inputOcr = inputOcr.replace('0CT', 'OCT') #대문자 O를 숫자 0으로 인식한 경우 치환

# 숫자가 2개 이상 이며 뒤에 ., 포함, 문자가 1개 이상이며 뒤에 ., 포함, 숫자가 4개인 수 ex)25.JUL.2023
pattern = r"(\d{2,}[.,/])+(\w{1,}[.,/])+\d{4}"    #날짜 추출 정규식
split_pattern = r"[.,/]" #날짜 분리 정규식

# 정규식 패턴[0]에 매칭되는 부분을 추출
match = re.search(pattern, inputOcr)


if match is None:
    field_value = ''
else:
    split_array = re.split(split_pattern, match.group())

    month = split_array[1]

    #월 문자열을 숫자로 변환
    if month == "JAN" :
        month = '01'
    elif month == "FEB" :
        month = '02'
    elif month == "MAR" :
        month = '03'
    elif month == "APR" :
        month = '04'
    elif month == "MAY" :
        month = '05'
    elif month == "JUN" :
        month = '06'
    elif month == "JUL" :
        month = '07'
    elif month == "AUG" :
        month = '08'
    elif month == "SEP" :
        month = '09'
    elif month == "OCT" :
        month = '10'
    elif month == "NOV" :
        month = '11'
    elif month == "DEC" :
        month = '12'

    field_value = split_array[2] + month + split_array[0]
    result = ''

