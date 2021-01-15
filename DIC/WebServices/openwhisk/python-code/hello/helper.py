def helper(dict):
   if 'name' in dict:
       name = dict['name']
   else:
       name = "stranger"
   greeting = "Hello from helper.py, " + name + "!"
   return {"greeting": greeting}