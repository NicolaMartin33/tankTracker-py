
import webbrowser
import tkinter.ttk as ttk
import sqlite3
from backend.config import csr_object


class question_display:
  def __init__(self, menu):
    self.M = menu
    self.data_list = [] #list of dictionaries

  def question_gui(self):
    #creating window
    question_win = self.M.new_window()

    #labels
    heading = ttk.Label(question_win,
                        text = 'Common Questions',
                        background = self.M.dflt_bg,
                        font = self.M.title_font)
    
    
    
    #buttons

    home = ttk.Button(question_win,
      text = 'home',
      style = self.M.dflt_btn,
      width= 7,
      command=lambda: question_win.destroy())

    heading.place(x=0,y=1)

    
    home.place(x=500, y=350)

    self.get_data(question_win) #calls get_data

  def merge(self, left, right, key): #merges the lsit of sorted answers 
    merged = []
    left_index, right_index = 0, 0 

    while left_index < len(left) and right_index < len(right):
      #merging
      if left[left_index][key] < right[right_index][key]: #smallest to largest
        merged.append(left[left_index])
        left_index += 1
      else:
        merged.append(right[right_index])
        right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])

    return merged #called by merge_sort

  def open_url(self, url): #takes entered url and follows link
    try:  
      webbrowser.open_new_tab(url)
    except Exception as e:
      print(f'failed:{e}')
    
  def get_data(self, win):

    try:
      query = "SELECT question_text, title, url, score FROM question"  #retrieving  the values from table question
      csr_object.execute(query,)
      rows = csr_object.fetchall()
      
  
      for row in rows:
        question_text, title, url, score = row #need to be in a row for the dictionary 
        #assigns each available its table value after line is executed
        self.data_list.append({'question_text' : question_text,
                            'title' : title,
                            'url' : url,
                            'score' : score}) 
        
      self.display_data(win)
    except sqlite3.Error as e:
      print(f'Error occurred in table sequence: {e}')

  #display answers
  def answer_gui(self, sorted, question):
    win = self.M.new_window()
    heading = ttk.Label(win,
                        text=question,
                        font = self.M.lbl_font,
                        background = self.M.dflt_bg)
    heading.pack()
    
    processed_ans = set() #avoids dupes
    for entry in sorted:
     
      #ensures there are no duplications
      if entry['question_text'] == question and entry['title'] not in processed_ans: 
        
        #adding title to processed set
        processed_ans.add(entry['title'])
        
        #making and placing question answer elements
        title_lbl = ttk.Label(win,
                            text=entry['title'],
                            font = self.M.reg_font,
                            background = self.M.dflt_bg)
        title_lbl.pack()

        url_btn = ttk.Button(win,
                        text = 'open url',
                         style = self.M.dflt_btn,
                         width = 8,
                         command= lambda url=entry['url']: self.open_url(url)) #opens url
        url_btn.pack()

        score_lbl = ttk.Label(win,
                              text=f'Relevancy Score: {entry["score"]}',
                              font = self.M.reg_font,                                
                              background = self.M.dflt_bg)
        score_lbl.pack()
    #back button on every page
    back = ttk.Button(win,
                      text = 'back',
                      style = self.M.dflt_btn,
                      width= 7,
                      command=lambda: win.destroy())
    back.pack()
    

  
    
  def display_data(self, win):
    #positioning elements 
    #sorted by score lowest to highest
    sorted_data  = self.M.merge_sort(self.data_list, key='score', ) 
    #retrieving questions and removing any duplications from the list
    csr_object.execute("SELECT question_text from question")
    results = csr_object.fetchall()
    
    results_nodupes = list(set(results)) #making a list a set removes duplications

    ypos = [75, 125 ,175] #sets y coords
    
    for index, result in enumerate(results_nodupes): #get an result and a counter(index)
      question_text = result[0]
      question_btn = ttk.Button(win,
                                text=question_text,
                                style = self.M.dflt_btn,
                                width= 50,
                                command=lambda question = question_text: self.answer_gui( sorted_data, question))
      question_btn.place(x=90, y=ypos[index]) #placing three buttons because example solution only has three questions
      
      
      
