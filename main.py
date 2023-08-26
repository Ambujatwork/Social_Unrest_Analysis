
from flask import Flask,render_template, request, jsonify
from social_unrest_check import *
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Load the pre-trained model
# model = joblib.load("social_unrest_check.py")  
# Load your model here
print("OK")
# @app.route('/',methods=['GET'])
# def form():
#     return render_template('./index.html')
@app.route('/', methods=['POST','GET'])
def predict():
    if request.method == 'GET':
        return render_template('index.html')
    keyword = request.form.get('keyword')
    tweets = scrape_caller(keyword)
    print(tweets)
    result = run_analysis(tweets)
    print((result))
    return  render_template('hello.html', result = result)

    # return render_template('index.html')

    # print(data)
    # keyword = "manipur"
    


if __name__ == '__main__':
    app.run(debug=True, port=8080)
    predict()

