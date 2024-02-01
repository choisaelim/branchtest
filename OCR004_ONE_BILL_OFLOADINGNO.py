import re


split_list = ["EXPORT"]        # 구분자

inputOcr = inputOcr.upper()      # 대문자로 변경
for i in split_list:
    if i in inputOcr:
        result = inputOcr.split(i)
        field_value = result[0].strip()
        break
    else:
        field_value = inputOcr.strip()