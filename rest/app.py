from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for the summaries
summaries = {}
next_id = 1

# Endpoint for getting a summary with a unique ID
@app.route('/summaries/<int:id>', methods=['GET'])
def get_summary(id):
    if id in summaries:
        return jsonify({'content': summaries[id]})
    else:
        return jsonify({'error': 'Summary not found.'}), 404

# Endpoint for posting a summary with a unique ID
@app.route('/summaries', methods=['POST'])
def post_summary():
    global next_id
    id = next_id
    next_id += 1
    summary = request.json['summary']
    summaries[id] = {'summary': summary, 'questions': {}}
    return jsonify({'id': id, 'summary': summary})

# Endpoint for adding questions to a summary
@app.route('/summaries/<int:id>/questions', methods=['POST'])
def add_questions(id):
    if id not in summaries:
        return jsonify({'error': 'Summary not found.'}), 404

    questions = request.json['questions']
    i = 0
    for q in questions:
        if 'question' not in q or 'answer' not in q:
            return jsonify({'error': 'Invalid question format.'}), 400
        summaries[id]['questions'][i] = {'question': q['question'], 'answer': q['answer']}
        i += 1

    return jsonify({'questions': summaries[id]['questions']})

# Custom error handler for 404 errors
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not found.'}), 404

if __name__ == '__main__':
    app.run(port=8000)