from flask import Flask, request, jsonify

from solver import Solver

print("Starting API")

app = Flask(__name__)

user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"

solver = Solver(user_agent)
solver.prepare()


@app.route('/solve-captcha', methods=['POST'])
def solve_captcha():
    print("Solving captcha")
    data = request.get_json()
    url_captcha = data.get('url')
    if not url_captcha:
        return jsonify({'error': 'URL is required'}), 400

    session_token = solver.solve(url_captcha)

    if session_token:
        return jsonify({'session_token': session_token}), 200
    else:
        return jsonify({'error': 'Failed to solve captcha'}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
