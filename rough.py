import re
import csv
import operator
print('dummy test')
errors={}
per_user={}
with open('python/algorithms/syslog.log') as f:
    for line in f:

        if 'ERROR' in line:

            u1=re.search('(\(.*\))',line)
            user_name=u1.group()
            user_name=user_name.replace('(','')
            user_name=user_name.replace(')','')
            if user_name not in per_user:
                per_user[user_name]=[0,1]
            else:
                per_user[user_name][1]+=1
            e=re.search("ticky: ERROR.* [^(]",line)

            if e is not None:
                e=e.group()
                e=e.replace('ticky: ERROR ','')
                if e not in errors:
                    errors[e]=1
                else:
                    errors[e]+=1
        else:
            u=re.search('(ticky: INFO .*[^\[]) (\[.*\]) (\(.*\))',line)
            # u=re.search('(ticky: INFO.* [^\[])(\[.*\])(\(.*\))',line)

            info=u.group(1)
            error=u.group(2)
            user_name=u.group(3)
            user_name=user_name.replace('(','')
            user_name=user_name.replace(')','')
            # print(info)
            # print(error)
            # print(user_name)
            if user_name not in per_user:

                per_user[user_name]=[1,0]
            else:
                per_user[user_name][0]+=1

errors=sorted(errors.items(),key=operator.itemgetter(1),reverse=True)
per_user=sorted(per_user.items(),key=operator.itemgetter(0))[:8]

# print(per_user)
f=open('user_statistics.csv','w',newline='\n')
w=csv.writer(f)
w.writerow(["Username", "INFO", "ERROR"])
for key,value in per_user:
    w.writerow([key,value[0],value[1]])
f.close()

with open('error_message.csv','w',newline='\n') as f2:
    w=csv.writer(f2)
    w.writerow(["Error", "Count"])
    for key,value in errors:
        w.writerow([key,value])


