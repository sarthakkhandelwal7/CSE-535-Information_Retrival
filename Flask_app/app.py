from flask import Flask, request, jsonify
import json
import urllib.request
from nltk.chat.util  import Chat, reflections
import regex as re
from query_processor import PreProcessor
# from multi_rake import Rake
# rake = Rake()
# keywords = rake.apply(full_text)


app = Flask(__name__)

chit_chat = [[
        r"(.*)my name is (.*)", #request
        ["Hello %2, How are you today ?",] #response
    ],
    [
        r"(.*)i am good(.*)",
        ["That's great. How can I help you?", ]
    ],
    [
        r"(.*)help(.*) ",
        ["I can help you ",]
    ],
     [
        r"(.*) your name ?",
        ["My name is beedo, but you can just call me robot and I'm a chatbot .",]
    ],
    [
        r"(.*)how are you(.*)",
        ["I'm doing very well. What about you", "i am great !"]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind that",]
    ],
    [
        r"i'm (.*) (good|well|okay|ok)",
        ["Nice to hear that","Alright, great !",]
    ],
    [
        r"(hi|hey|hello|hola|holla)(.*)",
        ["Hello", "Hey there",]
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse",]
    ],
    [
        r"(.*)created(.*)",
        ["top secret ;)",]
    ],
    [
        r"(.*) (location|city) ?",
        ['Buffalo, NY',]
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain in the past 4 days here in %2","In %2 there is a 50% chance of rain",]
    ],
    [
        r"how (.*) health (.*)",
        ["Health is very important, but I am a computer, so I don't need to worry about my health ",]
    ],
    [
        r"(.*)favourite (sports|game|sport)(.*)",
        ["I'm a very big fan of Football",]
    ],
    [
        r"who (.*) (Footballer|Player)?",
        ["Leonel Messi"]
    ],
    [
        r"quit",
        ["Bye for now. See you soon :) ","It was nice talking to you. See you soon :)"]
    ],
    [
        r"(.*)",
        ['']
    ],
]
chat = Chat(chit_chat, reflections)
preprocessor = PreProcessor()

@app.route('/', methods=['GET'])
def respond():

    args = request.args
    msg = args.get("query")
    if any(re.match(pre_defined, msg) for pre_defined in [r'(.*)amaze me(.*)', r'(.*)random facts(.*)']): msg = 'facts'
    bot_resp = chat.respond(msg)
    if bot_resp:
        resp = {'message': bot_resp}

    else:
        # msg = ' '.join(preprocessor.pre_process_string(msg))
        query = urllib.parse.quote(msg)
        # url_edismax = f'http://34.68.24.93:8983/solr/project_4/select?defType=edismax&indent=true&q.op=OR&q=body%3A{query}%20subreddit%3A{query}%20parent_body%3A{query}&rows=1&fl=id%2Cscore%2Cbody%2Cparent_body%2Cselftext'
        # url = f'http://34.68.24.93:8983/solr/project_4/select?fl=id%2Cscore%2Cbody%2Cselftext%2Cparent_body&rows=1&indent=true&q.op=OR&q=subreddit%3A{query}%0Aselftext%3A{query}%0Aparent_body%3A{query}'
        # url_lucene = f'http://34.68.24.93:8983/solr/project_4/select?defType=lucene&indent=true&q.op=OR&q=body%3A{query}%20subreddit%3A{query}%20parent_body%3A{query}&rows=1&fl=id%2Cscore%2Cbody%2Cparent_body'
        # urls = [url_edismax, url, url_lucene]
        url = f'http://34.68.24.93:8983/solr/project_4/select?fl=id%2Cscore%2Cbody%2Cselftext%2Cparent_body%2Ctitle%2Ctopic&rows=1&defType=dismax&indent=true&q.op=OR&q=subreddit%3A{query}%0Abody%3A{query}%0Aselftext%3A{query}%0Aparent_body%3A{query}&qf=title%5E1.7%20subreddit%5E1.2%20body%20selftext%5E1.4%20parent_body%20topic'
        data = json.load(urllib.request.urlopen(url))
        # docs = json.load(data)['response']['docs']
        resp = {
                "query": query,
                "maxScore": data['response']['maxScore'],
                "numFound": data['response']['numFound'],
                "message": data['response']['docs']
        }
    
    return jsonify(
       message=resp 
    )
