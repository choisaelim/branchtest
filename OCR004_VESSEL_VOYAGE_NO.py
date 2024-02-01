import re

inputOcr = ''


inputOcr = inputOcr.upper()     # 대문자로 변환
inputOcr = inputOcr.split('\n')     # 각 줄을 split으로 구분

field_value = {}    # field_value 딕셔너리 선언
field_value['VESSEL'] = '' # field_value key값 VESSEL
field_value['VOYAGE_NO'] = ''  # field_value key값 VOYAGE_NO


for i in inputOcr:
    # 하나이상의 공백문자와 숫자가 3개이상이고 nsew가 포함된 수 추출
    Extract_value = re.search(r'^(.*?)\s+(\d{3,}[NSEW])', i) 

    if Extract_value:
        # 정규표현식에 일치하는 값을 찾았을 경우
        result = Extract_value.group()
        Extract_value = re.search(r'^(.*?)\s+(\d{3,}[NSEW])$', result)
        field_value['VESSEL'] = Extract_value.group(1)
        field_value['VOYAGE_NO'] = Extract_value.group(2)
        break

    else:
        continue


if not field_value['VESSEL']:
    field_value['VESSEL'] = '추출할 데이터가 없습니다.'
if not field_value['VOYAGE_NO']:
    field_value['VOYAGE_NO'] = '추출할 데이터가 없습니다.'