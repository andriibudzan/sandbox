import re

pat2 = re.compile("(\w+\s{1}\w+)|([a-zA-Z0-9]+:)|(\s+)")
pat = re.compile("(\w+.exe)|([pid]{3}:\s\d+)|([A-C0-9]{3}:\s{1}\D:.+)")


def extract_matched(m):
    s = list()
    for match in m:
        x = [x for x in match if x != '']
        s.extend(x)
    return s


with open('processes.txt', 'r') as f_in:
    with open('processed.csv', 'w') as f_out:
        data = f_in.readlines()
        while data:
            s = data.pop(0)
            if s == '\n':
                continue
            match = re.findall(pat, s)
            s2 = ';'.join(extract_matched(match))
            f_out.write(s2 + '\n')
            continue

# import pandas as pd
# from pprint import pprint as pp
# df = pd.read_csv('processed.csv', sep=';', header=None)
# pp(df.head())
