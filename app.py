from flask import Flask, render_template, request, jsonify
import re
import long_responses as long

app = Flask(__name__)

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words))

    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def check_all_messages(message):
    highest_prob_list = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_prob_list
        highest_prob_list[bot_response] = message_probability(message, list_of_words, single_response, required_words)

    response('Hello!', ['hello', 'hi', 'hey', 'sup', 'heyo'], single_response=True)
    response('See you!', ['bye', 'goodbye'], single_response=True)
    response('yes its for all users', ['suitable','advance','users'], required_words=['beginner'])
    response('yes u can do that', ['learn ', 'pace','can','i'], single_response=True)
    response('Thank you!', ['i', 'love', 'code', 'palace'], required_words=['code', 'palace'])
    response('good', ['how ', 'is', 'doubt', 'support'], single_response=True)
    response('NO', ['dsa ', 'good', 'prerequisite', 'course'], single_response=True)
    response('yes u can pay in emi mode', ['emi ', 'pay', 'course'], single_response=True)
    response('only online mode', ['offline ', 'online', 'course'], single_response=True)
    response('yes you will get certificate after completing the course', ['does ', 'certificate', 'offer','course'], single_response=True)
    response('yes', ['market ', 'todays', 'relevant '], single_response=True)
    response('good ', ['how  ', 'is', 'the  ','doubt','support'], single_response=True)
    response('no sorry', ['financial ', 'aid', 'under-previleged '], single_response=True)
    response('there are didicated placement courses u can look for that', ['course  ', 'aid', 'opportunities '], single_response=True)
    response('generally there no such fixed salary it depends upon you', ['how', 'much', 'can ','i','make'], single_response=True)
    response('yes', ['market ', 'todays', 'relevant '], single_response=True)
    response('yes u can for refund if its under refund course but u should fulfill its rules', ['money ', 'refund', 'back '], single_response=True)
    response('NO', ['pre-requirement  ', 'course', 'what '], single_response=True)



    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return long.unknown() if highest_prob_list[best_match] < 1 else best_match

def get_response(user_input):
    split_message = re.split(r'\s+|[,;?!.-]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_input = request.json['user_input']
    response = get_response(user_input)
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
