from flask import Flask,render_template,request
import pickle
import numpy as np

mostPopular_df=pickle.load(open('mostPopular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           bookName=list(mostPopular_df['Book-Title'].values),
                           author=list(mostPopular_df['Book-Author'].values),
                           imageUrl=list(mostPopular_df['Image-URL-M'].values),
                           votes=list(mostPopular_df['Count-Ratings'].values),
                           rating=list(mostPopular_df['Avg-Rating'].values
                           )
                           )


@app.route('/recommend')
def recommend():
  return render_template('recommend.html')

@app.route('/recommend_books',methods=['post']) 
def recommend_books():
   search = request.form.get('search')
   index = np.where(pt.index==search)[0][0]
   similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:5]
    
   data = []
   for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

   return render_template('recommend.html',data=data)
if __name__ == '__main__':
    app.run(debug=True)