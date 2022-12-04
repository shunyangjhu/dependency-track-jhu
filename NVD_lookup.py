import nvdlib
import pandas as pd


def NVD_lookup(m_name, p_name):
    try:
        # keywordSearch: search on nvd db; key: nvd requested api key => reduce query time from 6s to 0.6s; delay = 6ms
        r = nvdlib.searchCVE(keywordSearch=m_name + " " + p_name, key='4e87454d-320e-498a-b9bc-192caef248c7', delay=6)
    except:
        print("HTTPError: 404 Client Error, Please try again with different manufacture and product name!")
        return
    dic = {"CVE ID": [], 'CPE': [], 'cpeName': [], 'CVSS Version': [], 'Score': [], 'Severity': []}
    for i in range(len(r)):
        dic['CVE ID'].append(r[i].id)
        arr = []
        arr1 = []
        for j in r[i].cpe:
            temp = eval(str(j))['criteria']
            arr.append(temp)
            for k in range(len(temp))[::-1]:
                # if end of ':*'
                if temp[k] == ':' and temp[k - 1] != '*':
                    for z in range(k)[::-1]:
                        if temp[z] == ':':
                            # if just a '-', continue
                            if temp[z + 1:k] == '-':
                                k = z
                                continue
                            # if it include version number, continue
                            if temp[z + 1:k][0].isdigit():
                                continue
                            arr1.append(temp[z + 1:k])
                            break
                    break
        if arr1:
            dic['cpeName'].append(arr1)
        else:
            dic['cpeName'].append(['None'])
        dic['CPE'].append(arr)
        dic['CVSS Version'].append(r[i].score[0])
        dic['Score'].append(r[i].score[1])
        dic['Severity'].append(r[i].score[2])

    def parsing(loc_dic):
        temp_dic = {'group': [], 'name': [], 'cpe': [], 'type': []}
        for i in range(len(loc_dic['CPE'])):
            # one CVE could have more than one corresponding CPE
            for j in range(len(loc_dic['CPE'][i])):
                if loc_dic['CPE'][i][j] not in temp_dic['cpe']:
                    temp_dic['group'].append(m_name)
                    temp_dic['name'].append(loc_dic['cpeName'][i][j])
                    temp_dic['cpe'].append(loc_dic['CPE'][i][j])
                    temp_dic['type'].append('library')
        return temp_dic

    if not dic['CVE ID']:
        print("No venerability found for this product!!")
    else:
        df = pd.DataFrame(dic)
        df.to_csv('output.csv', index=False)
        df = pd.DataFrame(parsing(dic))
        df.to_json('output.json', orient='records')
        # save file in save for now
        f2 = open("output.json", "r")
        save = f2.read()
        # add {"components"
        f2 = open("output.json", "w")
        f2.write("{\"components\":")
        f2 = open("output.json", "a")
        f2.write(save)
        # add }
        f2.write("}")
        f2.close()


# retrieve manufacturer name
f1 = open("manufacturer.txt", "r")
manufacturer = ""
product = ""
temp = f1.read()
f1.close()
for i in range(len(temp)):
    # "\ n " is where the two names separated from
    if temp[i] == "\n":
        manufacturer = temp[:i]
        product = temp[i + 1:]
# pass it to NVD
NVD_lookup(manufacturer, product)
