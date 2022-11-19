import nvdlib
import pandas as pd

# keywordSearch: search on nvd db; key: nvd requested api key => reduce query time from 6s to 0.6s; delay = 6ms
r = nvdlib.searchCVE(keywordSearch='Hospira', key='4e87454d-320e-498a-b9bc-192caef248c7', delay=6)
dic = {"CVE ID": [], 'CPE': [], 'CVSS Version': [], 'Score': [], 'Severity': []}

for i in range(len(r)):
    dic['CVE ID'].append(r[i].id)
    arr = []
    for j in r[i].cpe:
        arr.append(eval(str(j))['criteria'])
    dic['CPE'].append(arr)
    dic['CVSS Version'].append(r[i].score[0])
    dic['Score'].append(r[i].score[1])
    dic['Severity'].append(r[i].score[2])

def save_to_file(dic):
    df = pd.DataFrame(dic)
    df.to_csv('/Users/victorliang/desktop/output.csv', index=False)

save_to_file(dic)
