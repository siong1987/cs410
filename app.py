import os
import re
import math
import urllib

from readability.readability import Document
from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import and_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class Feature(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  feature = db.Column(db.String(120))
  category = db.Column(db.String(120))
  count = db.Column(db.Integer)

  def __init__(self, feature, category, count):
    self.feature = feature
    self.category = category
    self.count = count

  def __repr__(self):
    return '<Feature %r>' % self.feature

class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  category = db.Column(db.String(120), unique=True)
  count = db.Column(db.Integer)

  def __init__(self, category, count):
    self.category = category
    self.count = count

  def __repr__(self):
    return '<Category %r>' % self.category

def getwords(doc):
  splitter=re.compile('\\W*')
  # Split the words by non-alpha characters
  words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
  # Return the unique set of words only
  return dict([(w,1) for w in words])

class classifier:
  def __init__(self,getfeatures,filename=None):
    # Counts of feature/category combinations
    self.fc={}
    # Counts of documents in each category
    self.cc={}
    self.getfeatures=getfeatures

  def incf(self,f,cat):
    count=self.fcount(f,cat)
    if count==0:
      feature=Feature(f,cat,1)
      db.session.add(feature)
    else:
      feature=Feature.query.filter(and_(Feature.feature==f,Feature.category==cat)).first()
      feature.count=feature.count+1
  
  def fcount(self,f,cat):
    res=Feature.query.filter(and_(Feature.feature==f,Feature.category==cat)).first()
    if res==None: return 0
    else: return float(res.count)

  def incc(self,cat):
    count=self.catcount(cat)
    if count==0:
      category=Category(cat,1)
      db.session.add(category)
    else:
      category=Category.query.filter_by(category=cat).first()
      category.count=category.count+1

  def catcount(self,cat):
    res=Category.query.filter_by(category=cat).first()
    if res==None: return 0
    else: return float(res.count)

  def categories(self):
    cur=Category.query.all()
    return [d.category for d in cur]

  def totalcount(self):
    res=Category.query.all().length();
    if res==None: return 0
    return res[0]

  def train(self,item,cat):
    features=self.getfeatures(item)
    # Increment the count for every feature with this category
    for f in features:
      self.incf(f,cat)

    # Increment the count for this category
    self.incc(cat)
    db.session.commit()

  def fprob(self,f,cat):
    if self.catcount(cat)==0: return 0

    # The total number of times this feature appeared in this 
    # category divided by the total number of items in this category
    return self.fcount(f,cat)/self.catcount(cat)

  def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
    # Calculate current probability
    basicprob=prf(f,cat)

    # Count the number of times this feature has appeared in
    # all categories
    totals=sum([self.fcount(f,c) for c in self.categories()])

    # Calculate the weighted average
    bp=((weight*ap)+(totals*basicprob))/(weight+totals)
    return bp

class naivebayes(classifier):
  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.thresholds={}
  
  def docprob(self,item,cat):
    features=self.getfeatures(item)   

    # Multiply the probabilities of all the features together
    p=1
    for f in features: p*=self.weightedprob(f,cat,self.fprob)
    return p

  def prob(self,item,cat):
    catprob=self.catcount(cat)/self.totalcount()
    docprob=self.docprob(item,cat)
    return docprob*catprob
  
  def setthreshold(self,cat,t):
    self.thresholds[cat]=t
    
  def getthreshold(self,cat):
    if cat not in self.thresholds: return 1.0
    return self.thresholds[cat]
  
  def classify(self,item,default=None):
    probs={}
    # Find the category with the highest probability
    max=0.0
    for cat in self.categories():
      probs[cat]=self.prob(item,cat)
      if probs[cat]>max: 
        max=probs[cat]
        best=cat

    # Make sure the probability exceeds threshold*next best
    for cat in probs:
      if cat==best: continue
      if probs[cat]*self.getthreshold(best)>probs[best]: return default
    return best

class fisherclassifier(classifier):
  def cprob(self,f,cat):
    # The frequency of this feature in this category    
    clf=self.fprob(f,cat)
    if clf==0: return 0

    # The frequency of this feature in all the categories
    freqsum=sum([self.fprob(f,c) for c in self.categories()])

    # The probability is the frequency in this category divided by
    # the overall frequency
    p=clf/(freqsum)
    
    return p

  def fisherprob(self,item,cat):
    # Multiply all the probabilities together
    p=1
    features=self.getfeatures(item)
    for f in features:
      p*=(self.weightedprob(f,cat,self.cprob))

    # Take the natural log and multiply by -2
    fscore=-2*math.log(p)

    # Use the inverse chi2 function to get a probability
    return self.invchi2(fscore,len(features)*2)
  def invchi2(self,chi, df):
    m = chi / 2.0
    sum = term = math.exp(-m)
    for i in range(1, df//2):
        term *= m / i
        sum += term
    return min(sum, 1.0)

  def __init__(self,getfeatures):
    classifier.__init__(self,getfeatures)
    self.minimums={}

  def setminimum(self,cat,min):
    self.minimums[cat]=min
  
  def getminimum(self,cat):
    if cat not in self.minimums: return 0
    return self.minimums[cat]

  def classify(self,item,default=None):
    # Loop through looking for the best result
    best=default
    max=0.0
    for c in self.categories():
      p=self.fisherprob(item,c)
      # Make sure it exceeds its minimum
      if p>self.getminimum(c) and p>max:
        best=c
        max=p
    return best

cl=fisherclassifier(getwords)

@app.route('/')
def hello():
  return 'Welcome to CS410 Smarter App!!!'

@app.route('/parse/link', methods=['POST'])
def parse_link():
  category = request.form['category']
  link = request.form['link']
  html = urllib.urlopen(link).read()
  title = Document(html).short_title()
  cl.train(title, category)
  return '{"title":"%s"}' % title

@app.route('/parse/title', methods=['POST'])
def parse_title():
  category = request.form['category']
  title = request.form['title']
  cl.train(title, category)
  return '{"title":"%s"}' % title

@app.route('/train/link')
def train_link():
  return """
  <html>
  <head></head>
  <body>
  <form action="/parse/link" method="post">
  <p>LINK: <input type="text" name="link" size="100" value="" /></p>
  <p>CATEGORY: <input type="text" name="category" size="100" value="" /></p>
  <p><input type="submit" value="Submit" /></p>	
  </form>
  </body>
  </html>
  """

@app.route('/train/title')
def train_title():
  return """
  <html>
  <head></head>
  <body>
  <form action="/parse/title" method="post">
  <p>TITLE: <input type="text" name="title" size="100" value="" /></p>
  <p>CATEGORY: <input type="text" name="category" size="100" value="" /></p>
  <p><input type="submit" value="Submit" /></p>	
  </form>
  </body>
  </html>
  """

@app.route('/classify/link')
def classify_link():
  return """
  <html>
  <head></head>
  <body>
  <form action="/understand/link" method="post">
  <p>LINK: <input type="text" name="link" size="100" value="" /></p>
  <p><input type="submit" value="Submit" /></p>	
  </form>
  </body>
  </html>
  """

@app.route('/classify/title')
def classify_title():
  return """
  <html>
  <head></head>
  <body>
  <form action="/understand/title" method="post">
  <p>TITLE: <input type="text" name="title" size="100" value="" /></p>
  <p><input type="submit" value="Submit" /></p>	
  </form>
  </body>
  </html>
  """

@app.route('/understand/title', methods=['POST'])
def understand_title():
  title = request.form['title']
  category=cl.classify(title)
  return '{"category":"%s"}' % category

@app.route('/understand/link', methods=['POST'])
def understand_link():
  link = request.form['link']
  html = urllib.urlopen(link).read()
  title = Document(html).short_title()
  category=cl.classify(title)
  return '{"category":"%s"}' % category

if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  app.debug=True
  app.run(host='0.0.0.0', port=port)
