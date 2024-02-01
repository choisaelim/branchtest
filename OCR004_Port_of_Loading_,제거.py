import re
# 필요없는값 제거 == '['
inputOcr = inputOcr.replace('[','')

# split keyword 입력
split_list = [".", ",",":","[","PLACE"]

for i in split_list:
    if i in inputOcr:
        result = inputOcr.split(i)
        field_value = result[0].strip()
        break
    else:
        # 앞뒤 공백 제거
        field_value = inputOcr.strip()