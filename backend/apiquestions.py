
import requests


class apiQuestion_retrevial:
  def __init__(self, menu) -> None:
    self.auth_token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlNIQTI1NjpzS3dsMnlsV0VtMjVmcXhwTU40cWY4MXE2OWFFdWFyMnpLMUdhVGxjdWNZIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxNzA4NDc1MTAwLjE3MjgxMywiaWF0IjoxNzA4Mzg4NzAwLjE3MjgxMywianRpIjoiZHU1RF9lNS1PMTRaVERlaGJCUVkzWDZfd3hiNVZ3IiwiY2lkIjoiTjVVODRQaHlLWlVuRTZ5VXpFWGxyZyIsImxpZCI6InQyX2IwbjhkZTF6IiwiYWlkIjoidDJfYjBuOGRlMXoiLCJsY2EiOjE2MTYxOTE5MDYwMDAsInNjcCI6ImVKeUtWdEpTaWdVRUFBRF9fd056QVNjIiwiZmxvIjo5fQ.ok6Fobd4krPJPCIgA5_-86xCofV8KHHG2hYk_YGU2kFiNPKRIllRT6bWV3FYrg3-ZY32b6fZjJszq4VEA0WZVSpCXz0pwtJ74eSVqkWBICMR3TYGWx8UPDUgvV-W0ZTzDqlBXtS4x2SpeuNqPWkgVesBDVgczakfMk-2whuJ4uCqsSnujWJv1XEQjiGHCBfHpRKtYqrtBGl0Gd_h5WTzjj3-rTvTJu0zU7D7nrkP924X0gahlB4H3H2XkeQqzPng0hz2JlBpM0icRLLza8DYIcstZM7kL3Q3_V6YUZFt7ntF16VUca9Wkor7wiTtXm8GRVuVDlI-YxwuOiw9HnF0Pg'

    self.question_dict =  {
      "Which Fish are the Most Territorial?" : "3",
      "How do I Acclimatise my Fish?" : "4",
      "How Often Should I do a Water Change?" : "4"
    } #example set of questions 
    self.subreddit = 'Aquariums'
    self.M = menu

  #calls the reddit api to trawl for answers
  def answer_retrieval(self, question, limit): #limit is how amny results to find, is defined in self.question_dict
    parameters = {"q" : question,
                  "limit" : limit,
                  "restrict_sr" : "on",
                  "sort" : "relevance"
                 } #sets params for search
    print(parameters)
    search_url = f'https://oauth.reddit.com/r/{self.subreddit}/search/' #subreddit url getting searched

    response = requests.get(search_url, params = parameters, headers = {'User-Agent' : 'FishProject/1.0', 'Authorization': f'Bearer {self.auth_token}'}) #requestiong answers from reddit 
    
    if response.status_code == 200: #valid status code, result was returned
      content_type = response.headers.get('Content-Type', '')
      if 'application/json' in content_type: #if the content returned by request is in the form of json
        #get answers
        answer_json = response.json()
        
        relevant = [] #store the dictionaries for each question
  
        for post in answer_json['data']['children']: #adding correct information to relevant
          post_data =  post['data']
          relevant.append({
            'title' : post_data['title'],
            'url' : post_data['url'],
            'score' : post_data['score']
          }) #adding dctionary to the list
  
        return relevant
          
      else:
          print('Unexpected content type:', content_type) #if it isnt a json file returns error
          return None
    else:
      print('failed to get posts:', response.status_code) #if it runs into an error unpacking json or saving dictionaries returns error
      return None #returns none to alert that nothing was found

  #saves reult for each question in the table
  def get_question(self):
    try:
      for question, limit in self.question_dict.items(): 
          results = self.answer_retrieval(question, limit)
          if results is None:
            return False #if error occurred it does not attempt to save
          else:
            for post in results: #for dictionary in relevant []
              title = (post['title']) 
              url = (post['url']) 
              score = (post['score']) 
              self.M.Q.save(question, title, url, score) #then saved to the question table
      return True
    except Exception as e:
      print(f'error occurred {e}')
    
