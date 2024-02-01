inputOcr = 'HLCUANR230136956'

find_H = inputOcr.find('HLCU') #인덱스 번호
#print(find_H)
replace_find_h = inputOcr.replace(inputOcr[:find_H],'')
#print(replace_find_h)
field_value=replace_find_h