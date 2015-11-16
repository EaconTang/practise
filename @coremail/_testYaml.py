import yaml


test = '''
name: John Smith
age: 37
spouse:
    name: Jane Smith
    age: 25
children:
    - name: Jimmy Smith
      age: 15
    - name: Jenny Smith
      age: 12
'''

print test

cf_steram = open('LogMiner/Exceptions_all.yaml','r')
print yaml.load(cf_steram)
print yaml.load(test)