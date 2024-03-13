import pandas as pd

data = [1, 2, 3, 4, 5, 1, 2, 3, 4, 1, 2, 3, 1, 2, 1]
r_number = {}
for i in data:
    if i not in r_number:
        r_number[i] = 1
    else:
        r_number[i] += 1
resp = []

r_number = sorted(r_number.items(),key=lambda x:x[1], reverse = True)
for i in r_number[:5]:
    m_id = i[0]
    m_url = '@/movies/hot/%d.jpg' % (m_id)
    re = {'id': m_id, 'url': 'require' + m_url}
    resp.append(re)
print(resp)