import sqlite3, time
from colorama import Fore
from datetime import datetime, timedelta
print("Lets break iMessage")

output_file = open(r"output.txt", "w+", encoding="utf-8") 

apple_date = datetime(2001, 1, 1) 


try:
  """
  Find this file in your backup folder found in the Apple folder
  '3d0d7e5fb2ce288813306e4d4636395e047a3d28'
  Copy this folder over and rename it too extracted.db
  """
  print("Please enter phone number of user you would like to retrieve chat history with")
  search_num = int(input("No area codes and no dashes: (ex.0123456789)"))
  start = time.time()
  handle_id = -1
  sqlConnection = sqlite3.connect("extracted.db")
  #Make cursor to access database
  cursor = sqlConnection.cursor()
  print("Setup DB")
  """
  SELECT "_rowid_",* FROM handle WHERE id LIKE '%3916%' ESCAPE '\' LIMIT 0, 49999
  """
  cursor.execute(F"SELECT _rowid_,* FROM handle WHERE id LIKE '%{search_num}%' LIMIT 0, 49999")
  data = cursor.fetchall()
  if len(data) > 1:
    print("uh oh using first of many handles")
    handle_id=data[0][1]
    #print(data)
    #raise ValueError("You have more than one handle for this chat")
    
  else:
    handle_id=data[0][1]
    #print(handle_id)
  print("Fetching your chats...")
  cursor.execute(f"SELECT * FROM message WHERE handle_id = {handle_id}") 
  data = cursor.fetchall()
  texts = [row[2] for row in data]
  seconds_after = [row[15] for row in data]
  is_from_me = [row[21] for row in data] 
  past_messager = 0

  for i in range(len(texts)):
    text = texts[i]
    raw_time = apple_date + timedelta(seconds=seconds_after[i]*0.000000001)
    formatted_time = raw_time.strftime("%H:%M %m-%d-%Y")
    #print(seconds_after[i]*0.000000001)
    print(formatted_time)
    if is_from_me[i] == 1:
      from_me = True
    else:
      from_me = False
    #print(from_me)
    
    if text != None:
      #ADD timestamps, and better readibiltiuy of whos sending what
      if from_me:
        #print("                 "+Fore.BLUE+text+Fore.RESET)
        output_file.write(formatted_time+"                 "+text+"\n")
      else:
        #print(text)
        output_file.write(formatted_time+" "+text+"\n")

except sqlite3.Error as error:
  print(":( uh oh - ", error)

finally:
  output_file.close()
  if sqlConnection:
    sqlConnection.close()
    print("\n----------------------------------------------------\n")
    print("DB connection closed")
  print(f"{round(time.time()-start, 2)}s")
