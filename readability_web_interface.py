from flask import render_template

from flask import request

from flask import url_for

from markupsafe import escape

from flask import Flask

'''
https://pypi.org/project/textstat/
'''

import textstat


score_mapping = {
	"90-100":"Very Easy",
	"80-89":"Easy",
	"70-79":"Fairly Easy",
	"60-69":"Standard",
	"50-59":"Fairly Difficult",
	"30-49":"Difficult",
	"0-29":"Very Confusing"	
	}

def score_to_difficulty(
	score,
	):
	for s in score_mapping:
		l, h = s.split("-")
		l, h = float(l), float(h)

		if score > l and score <= (h+1):
			return score_mapping[s]
	return ''

score_to_difficulty(
	score = 55
	)


textstat.set_lang(
	lang = 'es',
	)

app = Flask(
    __name__
    )


@app.route(
	'/readability',
	methods = [
		'POST',
		'GET',
		])

def readability():
	if request.method == 'POST':
		input_text = request.form['input_text']

		try:
			corrected_text = textstat.fernandez_huerta(input_text)
			score = float(corrected_text)

			difficulty = score_to_difficulty(score)

		except:
			corrected_text = ''
			difficulty = ''

		return render_template(
			"index.html",
			readability = corrected_text,
			difficulty = difficulty,
			input_text = input_text,
			)
	else:
		return render_template(
			"index.html")


'''

# start the service

flask --app readability_web_interface --debug run --host=0.0.0.0 --port=3917 

# user the service 

localhost:3917/readability

'''