# jsoner - json db


##CLASS db
    :param file:  -  name of database (like 'xxx.json')
    :param data:  -  data adding into the db in start
            
if you set data - all data in file will be cleared and reloaded 
         don't set data if you would load json file             
     use them once for creating or make file by yourself         
  
###simple example:
*1. adding element 
```python
  import jsoner
  db = jsoner.db('testname.json',{})   # creates db file with {}
  db['test'] = 1                       # creates 'test' in db
  print(db)                            # shows {'test':1}
```

*2. adding ??? 
```python
  import jsoner
  db = jsoner.db('testname.json',{})   # creates db file with {}
  db['test1']['test2']['test3'] = 1    # creates 'test' in db
  print(db)                            # shows {'test1':{'test2':{'test3':1}}}}
```

*3. getting an element
```python
  #ages.json = {"John":30, "Kate":24}
  
  import jsoner
  db = jsoner.db('ages.json')
  print(db['John'])
  print(db)
```


*4. deleting an element
#TODO!
```python
  #ages.json = {"John":30, "Kate":24}
  
  import jsoner
  db = jsoner.db('ages.json')
  
```
