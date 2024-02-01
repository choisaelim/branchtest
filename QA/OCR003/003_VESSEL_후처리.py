import re

inputOcr = inputOcr.replace(')','')
inputOcr = inputOcr.replace('(','')
inputOcr = inputOcr.replace(' I ',' ')
inputOcr = inputOcr.replace(':','')
inputOcr = inputOcr.replace('  ',' ')
field_value = inputOcr