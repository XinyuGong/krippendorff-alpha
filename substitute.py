import re

fname='xml/answers_ez.xml'
target='comment'
f = open(fname, 'r')
records = f.readlines()
f.close()
f = open(fname, 'w')
print(len(records))
t_start='<'+target+'>'
t_end='</'+target+'>'
f.seek(0)
in_block = False
for i in range(len(records)):
    line=records[i]
    start=0
    end=len(line)
    need=False
    if re.search(t_start, line)!=None:
        need=True
        start=re.search(t_start, line).span()[1]
        if re.search(t_end, line)!=None:
            end=re.search(t_end, line).span()[0]
        else:
            in_block=True
            end=re.search('\n', line).span()[0]
    elif re.search(t_end, line)!=None:
        need=True
        in_block=False
        end=re.search(t_end, line).span()[0]
    elif in_block:
        need=True
    if need:
        line=re.sub('&', '&amp;', line[start:end])
        line=re.sub('<', '\'', line)
        line=re.sub('>', '\'', line)
        records[i]=records[i][:start]+line+records[i][end:]
    f.write(records[i])
f.close()