from flask import Flask, render_template, request, session, jsonify, redirect
from dotenv import load_dotenv
import os
from app.model import App_class
from user.routes import authentication
from user.model import Session_class
from Prometheus.function import wordapp_home_page_api_calls
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
from app.bookmark import Bookmark, read_bookmark
from app.rec_search import Recent_search


application = Flask(__name__)

word = ""

application.wsgi_app = DispatcherMiddleware(application.wsgi_app, {
    '/metrics': make_wsgi_app()
})

application.register_blueprint(authentication, url_prefix='/user')

load_dotenv()
application.secret_key = os.environ['SECRET_KEY']


@application.route('/')
@application.route('/home')
def home():
    if session.get('name') != None:
        Session_class().session_deletion()
    wordapp_home_page_api_calls.inc()
    return render_template("home.html")



@application.route('/index', methods=['GET', 'POST'])
def index():
    if session.get('name') != None:
        global word 
        if request.method == 'POST':
            word = request.form['word']
            Recent_search().add_recents(word)
            return redirect('/main')
        recent_searches = Recent_search().check_recents()
        return render_template("index.html", words = recent_searches)
    return redirect('/home')



@application.route("/main")
def main():
    if session.get('name') != None:
        global word
        if(Bookmark().check_bookmark(word)):
            is_bookmark = True
        else:
            is_bookmark = False
        html_word = word.upper()
        name = session.get('name')
        if word == "":
            return redirect('/index')
        return render_template("main.html", word = html_word, is_bookmark = is_bookmark, name = name )
    return redirect('/home')




#######################################################################################################################
################################################## Bookmark functions #################################################


@application.route('/add-bookmark')
def addbookmark():
    global word
    word.lower()
    Bookmark().add_bookmark(word)
    return jsonify({'status' : 200 })


@application.route("/remove-bookmark")
def removebookmark():
    global word
    Bookmark().remove_bookmark(word)
    return jsonify({'status': 200})


@application.route('/get-bookmarks')
def get_bookmarks():
    temp = read_bookmark()
    data = temp['bookmarks']
    return jsonify({'status':200, 'bookmarks' : data})

@application.route('/change-word-by-bookmark', methods = ['GET', 'POST'])
def change_word_by_bookmark():
    global word
    data = request.get_json()
    word = data['word']
    return jsonify({'status':200})


#######################################################################################################################
############################################### Profile ###############################################################


@application.route("/profile")
def profile():
    name = session['name']
    email = session['email']
    phone_no = session['phoneno']
    return jsonify({'name': name, 'email': email, 'phone_no': phone_no})




#######################################################################################################################
############################################### Recent Search# ########################################################


@application.route('/recent-search', methods = ['GET', 'POST'])
def recent_search_response():
    data = request.get_json()
    global word
    word = data['word']
    return jsonify({'status':200})


#######################################################################################################################
############################################### Word functions ########################################################

@application.route("/synonyms")
def synonyms():
    global word
    return jsonify(App_class().synonyms(word))


@application.route("/antonyms")
def antonyms():
    global word
    return jsonify(App_class().antonyms(word))

@application.route("/definitions")
def definitions():
    global word
    return jsonify(App_class().definitions(word))


@application.route("/examples")
def examples():
    global word
    return jsonify(App_class().examples(word))


@application.route("/rhymes")
def rhymes():
    global word
    return jsonify(App_class().rhymes(word))


@application.route("/pronunciation")
def pronunciation():
    global word
    return jsonify(App_class().pronunciation(word))


@application.route("/syllables")
def syllables():
    global word
    return jsonify(App_class().syllables(word))


@application.route("/frequency")
def frequency():
    global word
    return jsonify(App_class().frequency(word))

@application.route("/typeOf")
def typeOf():
    global word
    return jsonify(App_class().typeOf(word))


@application.route("/hasTypes")
def hasTypes():
    global word
    return jsonify(App_class().hasTypes(word))


@application.route("/partOf")
def partOf():
    global word
    return jsonify(App_class().partOf(word))


@application.route("/hasParts")
def hasParts():
    global word
    return jsonify(App_class().hasParts(word))


@application.route("/instanceOf")
def instanceOf():
    global word
    return jsonify(App_class().instanceOf(word))


@application.route("/hasInstances")
def hasInstances():
    global word
    return jsonify(App_class().hasInstances(word))


@application.route("/similarTo")
def similarTo():
    global word
    return jsonify(App_class().similarTo(word))


@application.route("/also")
def also():
    global word
    return jsonify(App_class().also(word))


@application.route("/entails")
def entails():
    global word
    return jsonify(App_class().entails(word))


@application.route("/memberOf")
def memberOf():
    global word
    return jsonify(App_class().memberOf(word))


@application.route("/hasMembers")
def hasMembers():
    global word
    return jsonify(App_class().hasMembers(word))


@application.route("/substanceOf")
def substanceOf():
    global word
    return jsonify(App_class().substanceOf(word))


@application.route("/hasSubstances")
def hasSubstances():
    global word
    return jsonify(App_class().hasSubstances(word))


@application.route("/inCategory")
def inCategory():
    global word
    return jsonify(App_class().inCategory(word))


@application.route("/hasCategories")
def hasCategories():
    global word
    return jsonify(App_class().hasCategories(word))


@application.route("/usageOf")
def usageOf():
    global word
    return jsonify(App_class().usageOf(word))


@application.route("/hasUsages")
def hasUsages():
    global word
    return jsonify(App_class().hasUsages(word))


@application.route("/inRegion")
def inRegion():
    global word
    return jsonify(App_class().inRegion(word))


@application.route("/regionOf")
def regionOf():
    global word
    return jsonify(App_class().regionOf(word))


@application.route("/pertainsTo")
def pertainsTo():
    global word
    return jsonify(App_class().pertainsTo(word))


if __name__ == '__main__':
    application.run( debug=True, host='0.0.0.0', port=4000 )