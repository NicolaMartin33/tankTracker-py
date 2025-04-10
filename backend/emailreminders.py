import datetime as dt
import json
import smtplib
import time
from datetime import datetime
from email.message import EmailMessage

from backend.config import connection_db, csr_object


class emails:
  def __init__(self):
    self.sent_last = {
      'weekly' : None,
      'fortnight' : None,
      'monthly': None
    }

  #gets emails of people who have parameters that have hit their update email time
  def getemail(self, freq):
    tanks = []
    users = []
    emails = []
    try:
      query = f'SELECT ParameterID FROM parameters WHERE Frequency = ?' #return parameters with the passed frequency
      csr_object.execute(query, (freq,))
      results = csr_object.fetchall()
      
      
      
      for result in results: #retrieving tankcode from parameterids in results
        paramid = result[0] #assigning value to new name 
        query = f'SELECT tank_code From parameterSelection WHERE (ParameterID = ? AND is_Selected = 1)'
        csr_object.execute(query, (paramid,))
        tanks.extend(csr_object.fetchall()) #adds them to the tanks list
        
  
      for tank in tanks: #retrieving userids from the tank codes in tanks
        tankid = tank[0]
        query = f'SELECT UserID From tank WHERE tank_code = ?'
        csr_object.execute(query, (tankid,))
        users.extend(csr_object.fetchall()) #adds them to the users list
        
      
      for user in users: #retrieves email from userids in user
        userid = user[0]
        query = f'SELECT email From user WHERE UserID = ?'
        csr_object.execute(query, (userid,))
        emails.extend(csr_object.fetchall())  #adds them to the emails list
         
      emails_nodupes = list(set(emails)) #making a list a set removes dupicates of emails
      return emails_nodupes
      
    except Exception as e:
      print('error fetching emails:', e)
      return None
      
     
  def datecheck(self): 
    timescale = []
    
    #getting weekly sent last date
    csr_object.execute('SELECT weekly_sent_last FROM configuration ')
    weekly_date = csr_object.fetchone()
    self.sent_last['weekly'] = dt.date.fromisoformat(str(weekly_date).strip("(),'"))
    
    #getting fortnight sent last date
    csr_object.execute('SELECT fortnight_sent_last FROM configuration ')
    fortnight_date = csr_object.fetchone()
    self.sent_last['fortnight'] = dt.date.fromisoformat(str(fortnight_date).strip("(),'"))
    
    #getting monthly sent last date
  
    csr_object.execute('SELECT monthly_sent_last FROM configuration ')
    monthly_date = csr_object.fetchone()
    self.sent_last['monthly'] = dt.date.fromisoformat(str(monthly_date).strip("(),'"))

    
    #this works out if a week has passed (todays date minus stored date put into days)
    print(f"today's date {dt.date.today()}, date last sent {self.sent_last['weekly']}")
    if (dt.date.today() - self.sent_last.get('weekly', dt.date.min)).days >= 7: 
      week_emails = self.getemail('weekly')
      print('it has been a week')
      if week_emails is not None:
        self.email_queue(week_emails, 'weekly')
        self.sent_last['weekly'] = dt.date.today()
        timescale.append('weekly')
    else:
      print("it hasn't been a week yet")
        
    #this works the same way but for months
    print(f"today's date {dt.date.today()}, date last sent {self.sent_last['monthly']}")
    if (dt.date.today()- self.sent_last.get('monthly', dt.date.min)).days >= 30: 
      month_emails = self.getemail('monthly')
      print('it has been a month')
      if month_emails is not None: #if func call returned true
        self.email_queue(month_emails, 'monthly')
        self.sent_last['monthly'] = dt.date.today()
        timescale.append('monthly')
    else:
      print("it hasn't been a month yet")
        
    #this does fortnights
    print(f"today's date {dt.date.today()}, date last sent {self.sent_last['fortnight']}")
    if (dt.date.today() - self.sent_last.get('fortnight', dt.date.min)).days >= 14: 
      fortnight_emails = self.getemail('fortnight')
      print('it has been a fortnight')
      if fortnight_emails is not None: #if func call returned true
        self.email_queue(fortnight_emails, 'fortnight')
        self.sent_last['fortnight'] = dt.date.today()
        timescale.append('fortnight')
    else:
      print("it hasn't been a fortnight yet")
        
    #saves sent_last to db
    for timing in timescale:
      #if timing = weekly weekly_sent_last will updated with todays date
      query = f'UPDATE configuration SET ({timing}_sent_last) = (?)' 
      csr_object.execute(query, (self.sent_last[timing],))
      connection_db.commit()
      
      print('save successful')
    time.sleep(86400) #trys again in a day

  def send_email(self, user, body, subject): #sends email using information passed to it
    try:
      admin_email = ''
      admin_pass = ''
      
      try: #need to have sensitve information in a secure file / not in main code
        with open('sensitive.json') as s:
          admin = json.load(s)
          
        admin_email = admin.get('admin_email')
        admin_pass = admin.get('admin_password')
      except json.JSONDecodeError as e: #if it cant retrieve the password or email
        print(f'error with reading json file {e}')
    
      with smtplib.SMTP ('smtp-mail.outlook.com', 587) as server: #outlook server
        server.starttls()
        server.login(admin_email, admin_pass) #logs in
        msg = EmailMessage()
        msg.set_content(body) #message text
        msg['From'] = admin_email #my email
        msg['To'] = str(user).strip("'(),'") #user email
        msg['Subject'] = subject #subject line
        server.send_message(msg) #sends message
        print('Send Successful')
        return True
    except smtplib.SMTPException as e: #if it fails reason is return
      print('send failed', e)
      return False
      
  #sets values to pass to send_email
  def email_queue(self, users, timing): 
    message = f'Time to update your {timing} levels and dosages!'
    subject = "It's Fish Time!"
    for user in users: # for people who need the email sent as established get_email
      email = user[0]
      self.send_email(email, message, subject)

  