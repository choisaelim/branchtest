# "SHIPPER_NAME,SHIPPER_ADDRESS"

import re

inputOcr = '''
AGRISTO NV
RIDDER DE ! GHELLINCKSTRAAT 9
8710 WIELSBEKE
BELGIUM
'''

inputOcr = inputOcr.upper()     # 대문자로 변환
# shipper 주소, 이름 오인식일시 변환
inputOcr = inputOcr.replace('MILCOBEL DAIRY N.Y.','MILCOBEL DAIRY N.V.')
inputOcr = inputOcr.replace('!','')

#개행문자로 리스트로 변환

field_value={}

pattern = r"LTD\.(?!\\n)"

inputOcr = re.sub(pattern, r"LTD.\n", inputOcr)

pattern = r"td\.(?!\\n)"

inputOcr = re.sub(pattern, r"td.\n", inputOcr)

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
                    addr_value = row
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