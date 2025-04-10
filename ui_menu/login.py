
import random
import tkinter as tk
import tkinter.ttk as ttk

from backend.config import connection_db, csr_object


class login:

  def __init__(self, menu):
    self.M = menu
    self.user_password = None
    self.user_email = None
    self.code = None

  #window for login page
  def login_gui(self):

    login_page = self.M.new_window() #new window

    #entries
    self.user_email = ttk.Entry(login_page,
                                width = 25)

    self.user_password = ttk.Entry(login_page,
                                   width = 30,
                                   show = '*')

    #labels
    heading = ttk.Label(login_page,
                        text='Log in',
                        background= self.M.dflt_bg,
                        font= self.M.title_font)

    field_name1 = ttk.Label(login_page,
                            text= 'Email/UserID:',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)

    field_name2 = ttk.Label(login_page,
                            text= 'Password:',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)

    invalidentries = ttk.Label(login_page,
                               text = 'Password or email is incorrect!',
                               background = self.M.dflt_bg,
                               font =self.M.reg_font )
    #buttons
    show_password = ttk.Button(login_page,
                               text = 'show',
                               style = self.M.dflt_btn,
                               width= 4,
                               command=lambda: self.M.password_show(self.user_password)) #calls show password so the password can be toggled to * and visible

    no_account = ttk.Button(login_page,
                            text = "Don't have an account?",
                            style = self.M.dflt_btn,
                            command=lambda: [login_page.destroy(),
                                             self.M.S.signup_gui()]) #destroys login win create signup win
    forgot_pass = ttk.Button(login_page,
                            text = "Forgot Password",
                            style = self.M.dflt_btn,
                            command=lambda: self.get_email_gui()) #starts sequence to reset passsword opens new page to enter email

    enter = ttk.Button(login_page,
                       text = 'Enter',
                       style = self.M.dflt_btn,
                       width = 4,
                       command=lambda: [ self.M.V.current_validation(self.user_email, self.user_password,invalidentries,login_page)]) #validates login details against system rules
    
    
    #placing elements
    heading.place(x=0, y=1)
    field_name1.place(x=0,y=30)
    self.user_email.place(x=0,y=50)
    field_name2.place(x=0,y=71)
    self.user_password.place(x=0,y=89)
    no_account.place(x=0,y=114)
    forgot_pass.place(x=0,y=148)
    show_password.place(x=250,y=85)
    enter.place(x=160,y=114)
    login_page.mainloop()

    
  #generates random 4 digit code
  def get_code(self):
    self.code = random.randint(0, 9999)
    return self.code

  #sets up gui for get email function
  def get_email_gui(self):
    win = self.M.new_window()
    #placing elements
    heading = ttk.Label(win,
                        text='Enter Email',
                        background= self.M.dflt_bg,
                        font= self.M.title_font)
    heading.place(x=0,y=0)
    
    field_name1 = ttk.Label(win,
                            text= 'Email/UserID:',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    email = tk.Entry(win, width=30)
    field_name1.place(x=0,y=50)
    email.place(x=0,y=80)

    enter = ttk.Button(win,
                       text = 'Enter',
                       style = self.M.dflt_btn,
                       width = 5,
                       command=lambda: self.get_email(win, email.get()) )
    enter.place(x=0,y=120)

    back = ttk.Button(win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width = 4,
                      command=lambda: win.destroy()) 
    back.place(x=50, y=120)

  #retrieves email from db 
  def get_email(self, win, email_entry):
    
    #in case they entered UserID and not their email
    csr_object.execute(f"SELECT email FROM user WHERE (email = '{email_entry}' OR UserID = '{email_entry}')")
    email = csr_object.fetchone()
    
    if email: #if there was a result found 
      print('email found in db')
      self.user_email = str(email).strip('(,)') #removes an of the character in brackets from string
      self.get_code_gui(win) #opens new page
      return True
      
    else:
      print('email not found in db')
      #placing error label
      errorlbl = ttk.Label(win,
                           text = 'Error Finding Email, please re-enter.',
                           font = self.M.reg_font,
                           background= self.M.dflt_bg)
      errorlbl.place(x=0, y=160)

  #sets gui for email code to be entered into
  def get_code_gui(self, win):
    
    #get verfication code
    code = self.get_code()
    #setting email variables
    subject = 'Reset Password'
    body = f'Please use this code to reset your password: {"{:04d}".format(code)}'
    valid = self.M.E.send_email(self.user_email, body, subject) #sending email with above details
    if valid is True: #if email can be sent make new window for entering the code
      win.destroy()
      win = self.M.new_window()
      #placing elements
      title = ttk.Label(win,
                        text= 'please check your email for a code',
                        background = self.M.dflt_bg,
                        font = self.M.reg_font)
      title.pack(side = tk.TOP)
      
      code_lbl = ttk.Label(win,
                           text= 'Code:',
                           background = self.M.dflt_bg,
                           font = self.M.reg_font)
      code_lbl.pack()
      
      entry = ttk.Entry(win,  width = 30)
      entry.pack()
      
      enter = ttk.Button(win,
                         text = 'Enter',
                         style = self.M.dflt_btn,
                         width = 4,
                         command=lambda: self.forgot_pass(win, entry))
      enter.pack()
      
      back = ttk.Button(win,
                        text = 'back',
                        style = self.M.dflt_btn,
                        width = 4,
                        command=lambda: win.destroy())
      back.pack()
    else:
      errorlbl = ttk.Label(win,
                           text = 'Error Sending Email, please retry.',
                           font = self.M.reg_font,
                           background= self.M.dflt_bg)
      errorlbl.place(x=0, y=160)
      
  #gui for new password entry
  def forgot_pass(self, win, entry):
    if str(entry.get()).strip() == str(self.code): #if codes match
      win.destroy()
      win = self.M.new_window()
      #entering new password
      pass_lbl1 = ttk.Label(win,
                            text = 'Enter a New Password:', 
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
      pass1 = ttk.Entry(win, width = 30)
      
      #placing
      pass_lbl1.place(x=0,y=50)
      pass1.place(x=0,y=70)

      pass_lbl2 = ttk.Label(win,
                            text = 'Re-Enter the Password:',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
      pass2 = ttk.Entry(win, width = 30) 
      
      #placing
      pass_lbl2.place(x=0, y=110)
      pass2.place(x=0,y=130)

      #calls userClass' function to validate the password
      enter = ttk.Button(win,
                         text = 'Enter',
                         style = self.M.dflt_btn,
                         width = 4,
                         command=lambda: self.validation(win, pass1, pass2)) #validates new entry against system rules
      
      enter.place(x=0,y=175)
      
      back = ttk.Button(win,
                        text = 'back',
                        style = self.M.dflt_btn,
                        width = 4, 
                        command=lambda: win.destroy()) 
      back.place(x=50,y=175)
      
    else: #if it fails validation error label is placed
      error_lbl = ttk.Label(win,
                            text='Code does not match our records',
                            font = self.M.reg_font,
                            background= self.M.dflt_bg)
      error_lbl.place(x=0, y=160)

  #validates password against system rules
  def validation(self, win, pass1, pass2):
    lbl = ttk.Label(win,
                    text='',
                    font = self.M.reg_font,
                    background= self.M.dflt_bg)
    
    valid = self.M.U.set_user_pass(pass1, pass2) #using userclass' func to validate
    if valid is True:
      try:
   
        query =('UPDATE user SET password = ? WHERE email = ?')
        csr_object.execute(query, (str(pass1.get()).strip("''(),"), str(self.user_email),))
        connection_db.commit()
        print('password saved to db')
        lbl.forget() #remove preexisting error label if its already been placed
        lbl.config(text= 'Password Successfully Changed')
        lbl.place(x=100, y=175)
      except Exception as e:
        print(f'there was an error:{e}')
        connection_db.rollback() #if it gets stopped by error before the commit nothing will get saved
    else: #if it fails validations 
      lbl.forget() #removes previous place
      lbl.config(text= 'Password Invalid, please try again')
      lbl.place(x=100, y=175)
      