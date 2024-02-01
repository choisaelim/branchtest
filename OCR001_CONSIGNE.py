#CONSIGNEE 영역이 넓어서 INCOTERMS 단어가 들어올 경우 INCOTERMS를 떼내고 앞의 값만 갖고 오며,
#해당 값의 앞 뒤 공백을 제거한다(strip)

if 'INCOTERMS' in inputOcr :
    inputOcr_list = inputOcr.split('INCOTERMS')
    field_value = inputOcr_list[0].strip()