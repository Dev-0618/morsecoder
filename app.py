# app.py

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_values.db'
db = SQLAlchemy(app)

class UserValues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(1), unique=True, nullable=False)
    value = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    user_values = UserValues.query.all()
    return render_template('morse_code_app.html', user_values=user_values)

@app.route('/enter_values', methods=['GET', 'POST'])
def enter_values():
    if request.method == 'POST':
        user_values = UserValues.query.all()

        # Split user_values into two lists for two columns
        middle_index = len(user_values) // 2
        user_values_left = user_values[:middle_index]
        user_values_right = user_values[middle_index:]

        # Retrieve values for additional characters
        additional_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 ,.?<>{}[]\\|~!@#$%^&*()_+=-'
        additional_values_left = [UserValues.query.filter_by(letter=char).first() for char in additional_chars]
        additional_values_right = [UserValues.query.filter_by(letter=char).first() for char in additional_chars]

        return render_template(
            'morse_code_app.html',
            user_values_left=user_values_left,
            user_values_right=user_values_right,
            additional_values_left=additional_values_left,
            additional_values_right=additional_values_right
        )

    user_values = UserValues.query.all()
    return render_template('morse_code_app.html', user_values=user_values)


@app.route('/encode', methods=['POST'])
def encode():
    user_input = request.form.get('user_input', '').upper()
    encoded_text = encode_text_with_custom_values(user_input)
    return render_template('morse_code_app.html', user_values=UserValues.query.all(), encoded_text=encoded_text)

@app.route('/decode', methods=['POST'])
def decode():
    morse_input = request.form.get('morse_input', '').upper()
    decoded_text = decode_morse_with_custom_values(morse_input)
    return render_template('morse_code_app.html', user_values=UserValues.query.all(), decoded_text=decoded_text)

def encode_text_with_custom_values(text):
    encoded_text = []
    for char in text:
        user_value = UserValues.query.filter_by(letter=char).first()
        if user_value:
            encoded_text.append(user_value.value)
        else:
            encoded_text.append(char)
    return ' '.join(encoded_text)

def decode_morse_with_custom_values(morse_code):
    morse_list = morse_code.split()
    decoded_text = ''
    for morse in morse_list:
        user_value = UserValues.query.filter_by(value=morse).first()
        if user_value:
            decoded_text += user_value.letter
        else:
            decoded_text += morse
    return decoded_text

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
