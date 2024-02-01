inputOcr = 'MEDUL9541532'

#■■■■■ sea waybill no, bill of loading no 추출 ■■■■■ 
# 데이터 가공

inputOcr = re.sub(r"[^\d\s\w]", '', inputOcr) # 숫자,공백,문자를 제외한 나머지 다 제거
inputOcr = inputOcr.upper()     # 대문자로 변환
inputOcr = inputOcr.split('\n')     # 각 줄을 split으로 구분

try:
    for i in inputOcr:
        # 하나이상의 숫자가 3개이상이고 nsew가 포함된 수 추출
        Extract_value = re.search(r'(\w{1,}\d{2,})', i) 

        if Extract_value:
            # 정규표현식에 일치하는 값을 찾았을 경우
            result = Extract_value.group()
            result = result.strip() # 양쪽 공백 제거
            break

        else:
            continue
except:
    result = '후처리 에러입니다.'

if len(result) == 0:
    result = '추출할 데이터가 없습니다.'

field_value = result