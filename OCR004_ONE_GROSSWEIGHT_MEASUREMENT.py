import re

##■■■■■■■■■■■■■■ gross_wight, measurement ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# field_value 딕셔너리 선언
field_value = {}

# 필요한 정보를 잘못 읽을 수 있기 때문에 replace
inputOcr = inputOcr.replace('YGM','KGM')
inputOcr = inputOcr.replace('MTO','MTQ')

# 데이터 추출값 대문자로 변경
inputOcr = inputOcr.upper()

# split_inputOcr 줄바꿈 기준으로 스플릿
split_inputOcr = inputOcr.split('\n')

# 중량 단위 리스트 형태로 저장 (추후 새로운 중량 단위가 나올경우 넣어줘야됨)
GROSS = ["KGS", "LBS", "KGM", "NET"]
MEASUREMENT = ["CBM", "CUM", "MTQ", "M3"]

# 찾은 값들 리스트에 저장하기 위해 사용
GROSS_LIST = []
MEASUREMENT_LIST = []
GROSS_result = []
GROSS_comparison = []

for t in split_inputOcr:
    # 여러개의 객체를 묶어서 동시에 반복
    for g,w in zip(GROSS,MEASUREMENT):
        # GROSS 와 MEASURMENT가 같이 포함될 경우
        if g in t:
            # GROSS에 포함된 단위 찾기
            pattern = r"\d+[,. ]*\d*" + re.escape(g) 
            # 정규식 패턴에 매칭되는 부분을 추출
            match = re.search(pattern, t)
            # match에 값이 존재 할 경우
            if match:
                result = match.group()
                GROSS_LIST.append(result)
        # # GROSS 와 MEASURMENT가 같이 포함될 경우
        # if w in t:
        #     # MEASUREMENT에 포함된 단위 찾기
        #     pattern = r"\d+[,.]*\d*" + re.escape(w)
        #     # 정규식 패턴에 매칭되는 부분을 추출
        #     match = re.search(pattern, t)
        #     # match에 값이 존재 할 경우
        #     if match:
        #         result = match.group()
        #         MEASUREMENT_LIST.append(result)


# 리스트 값들 str 형태로 조인
GROSS_LIST = ','.join(GROSS_LIST)
# MEASUREMENT_LIST = ','.join(MEASUREMENT_LIST)

# 숫자와 ',', '.' 를 제외한 나머지 문자 제거
GROSS_LIST = re.sub(r"[^\d.,]",'',GROSS_LIST)
# MEASUREMENT_LIST = re.sub(r"[^\d.,]",'',MEASUREMENT_LIST)

# GROSS_LIST에서 결과값을 쉼표로 분리하여 리스트로 저장
GROSS_LIST = GROSS_LIST.split(',')

# 첫 번째 글자가 7인 경우 찾기
pattern = r"^7"
for num in GROSS_LIST:
    
    # pattern이 맞으면 '7' 제거 후 중복값 체크
    if re.match(pattern, str(num)):
        num_str = str(num)

        # 값 초기화
        num_without_7 = ''
        num_without_7X = ''

        num_without_7 = num_str[1:]  # '7' 제거
        num_without_7X = num_str[2:]    # '7 + 숫자 하나' 제거

        # 7제거 후 List 값 비교 했을떄 값이 있으면 PASS
        if num_without_7X in GROSS_LIST or num_without_7 in GROSS_LIST:
            GROSS_result.append(num_without_7)
            GROSS_comparison.append(num_without_7X) # 최종 비교한값 추가
            continue
        # 없으면 값 넣기
        else:
            GROSS_result.append(num)

    # Pattern이 없으면 list에 값(num) 추가
    else:
        GROSS_result.append(num)


# 리스트에 중복된거 제거
GROSS_result = list(dict.fromkeys(GROSS_result))

# dict.fromkeys를 사용하여 GROSS_result의 값들로 새로운 딕셔너리 생성
comparison_dict = dict.fromkeys(GROSS_result)

# GROSS_comparison에 있는 값들을 comparison_dict 제거
for num in GROSS_comparison:
    comparison_dict.pop(num, None)      # pop 메서드를 사용해서 중복 값 제거

# 중복이 제거된 리스트로 변환
GROSS_result = list(comparison_dict.keys())


# 딕셔너리 선언
field_value['GROSSWEIGHT'] = GROSS_result
# field_value['MEASUREMENT'] = MEASUREMENT_LIST

MEASUREMENT_LIST = list(dict.fromkeys(MEASUREMENT_LIST))

# ■■■■■■■ Grossweight 에서 나온 결과값을 쉼표로 분리하여 각 요소마다 MEASUREMENT에 "0"을 추가하는 로직 ■■■■■■
# 추후 MEASUREMENT 가 인식이 잘 되었을떄 이부분 제외 후 주석처리 된 내용 다 활성화 필요

# "," 기준 각 요소마다 MEASUREMENT에 "0"을 추가
# MEASUREMENT_LIST = ["0" for gross_weight in MEASUREMENT_LIST]
MEASUREMENT_LIST = ["0" for gross_weight in GROSS_result]

# 다시 쉼표로 분리된 문자열로 조합
# MEASUREMENT_LIST = ','.join(MEASUREMENT_LIST)

# 딕셔너리 선언
field_value['MEASUREMENT'] = MEASUREMENT_LIST

# 추후 MEASUREMENT 가 인식이 잘 되었을떄 이부분 제외 후 주석처리 된 내용 다 활성화 필요
# ■■■■■■■ Grossweight 에서 나온 결과값을 쉼표로 분리하여 각 요소마다 MEASUREMENT에 "0"을 추가하는 로직 ■■■■■■