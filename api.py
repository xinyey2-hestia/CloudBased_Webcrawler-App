from flask import Flask, render_template
from flask import jsonify
from flask import abort
from flask import request
import os.path
import helper

app = Flask(__name__)
path = os.path.dirname(__file__)
dir_data = os.path.join(os.path.abspath(os.path.join(path,os.pardir)), r"Assignment2.1\data.json")
print(dir_data)

bookjson,authorjson = helper.jsonParse(dir_data)


@app.route('/')
def index():
    return "hello user"



@app.route("/books/<string:attr>=<string:attr_value>", methods= ['GET'])
def findbooks(attr, attr_value):
   
    res = []
    if attr not in ['title', 'author', 'similar_book_list']:
        return abort(400)
    for i in bookjson:
        if str(attr_value) in str(i[attr]):
            res.append(i)

    if not res:
        return abort(400)
    else:
        return jsonify({"_HTTP_":200, "results": res})

@app.route("/authors/<string:attr>=<string:attr_val>",methods = ['GET'])
def findauthros(attr,attr_val):
    res = []
    if attr not in ['name', 'book_list']:
        return abort(400)
    for i in authorjson:
        if str(attr_val) in str(i[attr]):
            res.append(i)

    if not res:
        return abort(400)
    else:
        return jsonify({"_HTTP_":200, "results": res})

@app.route("/titles/<string:attr>and<string:attr_val>", methods =['GET'])
def findAndTitle(attr, attr_val):
    res=[]
    for i in bookjson:
        if str(attr) in str(i['title']) and str(attr_val) in str(i['title']):
            res.append(i)
    if not res:
        return abort(400)
    else:
        return jsonify({"_HTTP_": 200, "results": res})

@app.route("/authorname/<string:attr>/or/<string:attr_val>", methods=['GET'])
def findOrAuthor(attr,attr_val):
    res=[]
    for i in authorjson:
        if (str(attr) in str(i['name'])):
            res.append(i)
        if (str(attr_val) in str(i['name'])):
            res.append(i)
    if not res:
        return abort(400)
    else:
        return jsonify({"_HTTP_": 200, "results": res})

@app.route("/books/puts<string:title>", methods=['PUT'])
def putBook(title):
    if (request.json is None):
        abort(400)
    for i in bookjson:
        if i['title'] == title:
            for attr in request.json:
                if attr in i:
                    i[attr] = request.json[attr]
            return jsonify({"_HTTP_":200, "result": i})
        else:
            abort(400)


@app.route("/author?put<string:name>", methods=['PUT'])
def putAuthor(name):
    if (request.json is None):
        abort(400)
    for i in authorjson:
        if i['name'] == name:
            for attr in request.json:
                if attr in i:
                    i[attr] = request.json[attr]
            return jsonify({"_HTTP_": 200, "result": i})
        else:
            abort(400)

@app.route("/book", methods = ['POST'])
def postOneBook():
    if (request.json is None) or (request.json['title'] is None):
        abort(400)
    for i in bookjson:
        if (i['title'] == request.json['title']):
            abort(400)
    bookjson.append(request.json)
    return jsonify({"_HTTP_": 200, "result": "success"})

@app.route("/books", methods = ['POST'])
def postBooks():
    if (request.json is None):
        abort(400)
    for i in bookjson:
        for j in request.json:
            if (i['title'] == j['title']):
                abort(400)
    bookjson.append(request.json)
    return jsonify({"_HTTP_": 200, "result": "success"})


@app.route("/author", methods = ['POST'])
def postOneAuthor():
    if (request.json is None) or (request.json['name'] is None):
        abort(400)
    for i in authorjson:
        if (i['name'] == request.json['name']):
            abort(400)
    authorjson.append(request.json)
    return jsonify({"_HTTP_": 200, "result": "success"})

@app.route("/authors", methods = ['POST'])
def postAuthors():
    if (request.json is None):
        abort(400)
    for i in authorjson:
        for j in request.json:
            if (i['name'] == j['name']):
                abort(400)
    authorjson.append(request.json)
    return jsonify({"_HTTP_": 200, "result": "success"})

#delet book
@app.route("/book?<string:title>", methods=["DELETE"])
def deletBook(title):
    j=0
    for i in bookjson:
        if i["title"]==title:
            del bookjson[j]
            return jsonify({"_HTTP_": 200, "results": bookjson})
        j=j+1
    abort(400)

#delet author
@app.route("/author?<string:name>", methods=["DELETE"])
def deletAuthor(name):
    j=0
    for i in authorjson:
        if i["name"]==name:
            del authorjson[j]
            return jsonify({"_HTTP_": 200, "results": authorjson})
        j=j+1
    abort(400)

#query for most frequent author
@app.route("/query/most-book-authors")
def mapreduceAuthor():
    dict ={}
    for i in bookjson:
        if dict.get(i['author_id']):
            dict[i['author_id']] = dict[i['author_id']]+1
        else:
            dict[i['author_id']] = 1

    return "The author with most Book is" + max(dict, key=dict.get)

#query for  most similar book
@app.route("/query/most-similar-book")
def mapreduceBook():
    dict = {}
    for i in bookjson:
        if i.get('similiar_book_list') is None:
            continue
        dict[i['title']] = len(i['similiar_book_list'])

    return "The book with most similar books are   " + max(dict, key=dict.get)

#visiualization of author rating by chart.js
@app.route("/author_chart")
def chart():
    legend = 'top ranking authors'

    labels=[]
    values=[]
    count = 0
    for i in authorjson:
            labels.append(i['name'])
            values.append(float(i['rating']))

    labels =[x for y, x in sorted(zip(values,labels),reverse=True)]
    values.sort(reverse=True)

    return render_template('chart.html', values=values, labels=labels, legend=legend)

#visulazation for reviews of books
@app.route("/book_chart")
def bookChart():
    legend = 'top reviewed books'

    labels=[]
    values=[]
    count = 0
    for i in bookjson:
            labels.append(i['title'])
            values.append(int(i['review_count']))

    labels =[x for y, x in sorted(zip(values,labels),reverse=True)]
    values.sort(reverse=True)

    return render_template('chart.html', values=values, labels=labels, legend=legend)

# show books in database
@app.route("/GET/books")
def getBook():

    return render_template('GETbook.html')

# show authors in database
@app.route("/GET/authors")
def getAuthor():

    return render_template('GETauthor.html')

if __name__ == "__main__":
    app.run(debug=True)