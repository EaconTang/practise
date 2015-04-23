from collections import Counter
import re

list1 = [1,2,3,4,5,4,3,2,1,'a','a','b','a']

list1_Counter = Counter(list1)

print list1_Counter

print "keys:",list1_Counter.keys()
print "values:",list1_Counter.values()

print list1_Counter.most_common(2)

with open("test.txt") as f:
    text = f.read()
    text_list = re.findall(r'\w+',text)
    print Counter(text_list)