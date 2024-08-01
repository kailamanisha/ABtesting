from flask import Flask, request, jsonify
import math
from scipy.stats import norm

app = Flask(__name__)

def calculate_z_score(confidence_level):
    return norm.ppf(confidence_level + (1 - confidence_level) / 2)

def calculate_sample_size(original_rate, uplift, variations, z_score):
    new_rate = original_rate * (1 + uplift / 100)
    p1 = original_rate / 100
    p2 = new_rate / 100
    standard_error = math.sqrt((p1 * (1 - p1)) / 1 + (p2 * (1 - p2)) / 1)
    return ((z_score * standard_error) ** 2) / ((p1 - p2) ** 2)

def calculate_test_duration(sample_size, daily_visitors):
    return sample_size / daily_visitors

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    original_rate = float(data['original_rate'])
    daily_visitors = float(data['daily_visitors'])
    variations = float(data['variations'])
    expected_uplift = float(data['expected_uplift'])
    chance_to_beat_control = float(data['chance_to_beat_control'])

    z_score = calculate_z_score(chance_to_beat_control / 100)
    sample_size = calculate_sample_size(original_rate, expected_uplift, variations, z_score)
    duration = calculate_test_duration(sample_size, daily_visitors)
    duration_days = math.ceil(duration)

    return jsonify({'days': duration_days})

if __name__ == '__main__':
    app.run(debug=True)