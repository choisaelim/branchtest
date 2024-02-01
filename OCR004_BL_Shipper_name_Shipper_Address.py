# "SHIPPER_NAME,SHIPPER_ADDRESS"

import re

inputOcr = '''
FIT
2O AVENUE HENRI FREVILLE 35202
RENNES CEDEX 2 -
'''

#개행문자로 리스트로 변환

field_value={}

pattern = r"LTD\.(?!\\n)"

inputOcr = re.sub(pattern, r"LTD.\n", inputOcr)

pattern = r"td\.(?!\\n)"

inputOcr = re.sub(pattern, r"td.\n", inputOcr)

#숫자 형식인데 대문자 O로 인식된 경우 치환하기 위한 정규식
numberMixPattern = r"[\d\s]O[\d\s]"


def replace(text):

    lines = inputOcr.split("\n")

    if "Nombre" in lines[0] or "shipper" in lines[0] or "Shipper" in lines[0]or "SHIPPER" in lines[0] :
        lines = lines[1:]

    inputOcr2 = "\n".join(lines)

    # 개행 문자로 리스트로 전환

    inputOcr_result = list(inputOcr2.split('\n'))

    # 첫 번째 아이템이 공백인 경우 삭제

    if len(inputOcr_result) > 0 and inputOcr_result[0] == '':
        del inputOcr_result[0]


    SHIP_NAME = ''
    addr_value = ''

    for row in inputOcr_result:
        row = row.strip()  # 앞뒤 공백 제거

        if len(row) > 0:
            if SHIP_NAME == '':
                SHIP_NAME = row
            else:
                if addr_value == '':
                    addr_value = row #SHIPPER ADDRESS 첫줄만 나오게 수정
                    match = re.search(numberMixPattern, row)
                    if match is not None:
                        addr_value =re.sub(numberMixPattern, re.sub('O', '0', match.group()),row)
                    break
                else:
                    addr_value += '\n' + row

    field_value = {}

    field_value['SHIPPER_NAME'] = SHIP_NAME
    field_value['SHIPPER_ADDRESS'] = addr_value

    return field_value

def ftR() :

    field_value = {}
    field_value['SHIPPER_NAME'] = "필드 인식에 실패하였습니다."
    field_value['SHIPPER_ADDRESS'] = "필드 인식에 실패하였습니다."

    return field_value


try:
    field_value = replace(inputOcr)
    #print(field_value)

except:
    field_value = ftR()
    #print(field_value)