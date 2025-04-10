import tkinter.ttk as ttk


class signup: 
  #composition
  def __init__(self, menu):
    self.M = menu

  #makes signup interface
  def signup_gui(self):
    
    #sign up window
    signup_win = self.M.new_window()
    
    #creating labels
    
    heading = ttk.Label(signup_win,
                        text = 'Sign up',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)
    
    error_label = ttk.Label(signup_win,
                            text = '',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    
    email_label = ttk.Label(signup_win,
                            text = 'Enter an Email:',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    
    pass_label1 = ttk.Label(signup_win,
                            text = 'Enter a Password:', 
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    
    pass_label2 = ttk.Label(signup_win,
                            text = 'Re-Enter the Password:',
                            background = self.M.dflt_bg,
                            font = self.M.reg_font)
    
    fname = ttk.Label(signup_win,
                      text = 'First Name:',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)

    lname = ttk.Label(signup_win,
                      text = 'Last Name:',
                      background = self.M.dflt_bg,
                      font = self.M.reg_font)
    

    #creating entries
    firstnm = ttk.Entry(signup_win, width = 25)
    lastnm = ttk.Entry(signup_win, width = 25)
    useremail = ttk.Entry(signup_win, width = 25)
    passentry1 = ttk.Entry(signup_win, width = 30)
    passentry2 = ttk.Entry(signup_win, width = 30)  

    #creating buttons
    back = ttk.Button(signup_win,
                      text = 'back to log in page',
                      style = self.M.dflt_btn,
                      width= 4,
                      command=lambda: [signup_win.destroy(), self.M.L.login_gui()]) #destroy signup page and take user back to login 
    
    enter = ttk.Button(signup_win,
                       text = 'Enter',
                       style = self.M.dflt_btn,
                       width= 4,
                       command=lambda: self.M.V.new_validation(firstnm, lastnm, useremail, passentry1, passentry2, signup_win, error_label)) #passes on entries to be validated

    

    #placing elements
    heading.place(x=0, y=1)
    fname.place(x=0, y=30)
    firstnm.place(x=0, y=50)
    lname.place(x=0, y=71)
    lastnm.place(x=0, y=89)
    email_label.place(x=140,y=30)
    useremail.place(x=140,y=50)
    pass_label1.place(x=140,y=71)
    passentry1.place(x=140, y=89)
    pass_label2.place(x=140, y=112)
    passentry2.place(x=140, y=130)
    back.place(x=0, y=154)
    enter.place(x=140, y=154)
    
    return signup_win