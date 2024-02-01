#portofdischarge, voyageNo OCR003, OCR004에서 두 개 공통으로 처리
inputOcr = 'BUSAN PORT,'
#inputOcr = '008E'

inputOcr = inputOcr.upper()      # 대문자로 변경

# 필요없는 값 제거
inputOcr = inputOcr.replace(' ','')
inputOcr = inputOcr.replace('[','')
inputOcr = inputOcr.replace('Voyage-No.:','')
inputOcr = inputOcr.replace('VOYAGA-NO.:','')
inputOcr = inputOcr.replace('VOYAGANO.:','')
split_list = [".",",","(","PORT","PLACE"]        # 구분자

field_value = inputOcr
for i in split_list:
    if i in field_value:
        result = field_value.split(i)
        field_value = result[0].strip()
        #break
    else:
        field_value = field_value.strip()

# 잘못 인식된 값 수정
field_value = field_value.replace('O','0')
field_value = field_value.replace("L","1")
field_value = field_value.replace("I","1")