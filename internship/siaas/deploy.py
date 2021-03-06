from flask import Flask
from flask import request
from sysiden.sysiden import *
from io import StringIO


app = Flask(__name__)


@app.route('/', methods=['POST'])
def handle_file():
	if request.method == 'POST':
		if 'trajectories' in request.files.keys():
			f = request.files['trajectories']
		elif 'trajectories' in request.form.keys():
			f = StringIO(request.form['trajectories'])
		else:
			return 'Bad request: the request must provide a file in with the "trajectories" key', 400

		if 'cutoff_value' in request.form.keys():
			cutoff_value = float(request.form['cutoff_value'])
		else:
			return 'Bad request: the request must provide a float cutoff value in the "cutoff_value" data field', 400
		if 'max_degree' in request.form.keys():
			max_degree = int(request.form['max_degree'])
		else:
			max_degree = 3

		if 'derivative' in request.form.keys():
			derivative = request.form['derivative'].lower() in ['true', '1', 't', 'y', 'yes']
		else:
			derivative = False
	else:
		return 'Bad regest: the server only handles POST requests.', 400
	result = identify_system(f, cutoff_value, max_degree, derivative)
	return result, 200

if __name__ == "__main__":
	app.run(debug=True)