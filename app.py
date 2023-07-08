import nltk
import pyodbc
from azure.storage.blob import BlobServiceClient
from cleantext import clean
from flask import Flask
from flask import render_template
from flask import request
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
#deploy2
app = Flask(__name__)
server = 'assignmentservershruthaja.database.windows.net'
database = 'assignemnt3'
username = 'shruthaja'
password = ''
driver = '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
cursor = conn.cursor()

def getbook():
    account_url = "DefaultEndpointsProtocol=https;AccountName=shruthaja;AccountKey=FvxC1NCWJQuBHKf77+JJaniZDHYUsBzqjy9H2o2o4INHFJRAXUTl6E3VB+2wXX3SsjFsMy5Vpm/R+ASto6SosQ==;EndpointSuffix=core.windows.net"
    blob_account_client = BlobServiceClient.from_connection_string(account_url)
    j = blob_account_client.get_container_client("assignment5").download_blob("RomeoJuliet_Shakespere.txt")
    book = str(j.read())
    return book

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == "POST":
        n = request.form['number']
        for i in noun(n):
            result[i[0]]=i[1]
        print(result)
    return render_template('index.html', result=result,d={},total={})


@app.route('/count', methods=['GET', 'POST'])
def count():
    d={}
    dd={}
    total=0
    result={}
    if request.method == "POST":
        n = request.form['letters']
        n=n.split()
        book=getbook()
        book=clean(book,stp_lang='english',stemming=False)
        print(book)
        myFD = nltk.FreqDist(book)
        total = float(sum(myFD.values()))
        for i in n:
            d[i]=float(myFD[i])
        for i in n:
            dd[i]=d[i]/total
        print(d,dd)
    return render_template('index.html', d=d,total=dd,result={})

@app.route('/page2.html', methods=['GET', 'POST'])
def page2():
    result = []
    book=''
    if request.method == "POST":
        replace = request.form['replace']
        toreplace=request.form['toreplace']
        n=request.form['lines']
        book = getbook()
        book=book.replace('b"',"")
        book=clean(book)
        book=book.replace(replace,toreplace)
        book=book.split('.')
        for i in range(int(n)):
            result.append(book[i])
    return render_template('page2.html', result=result)

@app.route('/page3.html', methods=['GET', 'POST'])
def page3():
    result = []
    book=''
    if request.method == "POST":
        name = request.form['name']
        n=int(request.form['lines'])
        book = getbook()
        book=clean(book,replace_with_punct="",strip_lines=True)
        book=book.replace('b"',"")
        book=book.split('.')
        count=0
        for i in range(len(book)):
            print(name)
            if(book[i].__contains__(name) and count<n):
                result.append(book[i])
                count=count+1
            else:
                continue
    return render_template('page3.html', result=result)

def noun(n):
    book = getbook()
    book = clean(book)
    tokens = word_tokenize(book)
    # Filter out stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    # Perform part-of-speech tagging
    tagged_words = pos_tag(filtered_tokens)
    # Extract nouns from tagged words
    nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
    # Calculate the frequency distribution
    freq_dist = FreqDist(nouns)
    return (freq_dist.most_common(int(n)))



if __name__ == '__main__':
    app.run(debug=True)
