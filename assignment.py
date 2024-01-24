from flask import Flask, request, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)

def calculate_volatility(df):
    # Ensure the 'Date' column is in the correct datetime format
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')

    # Sort the DataFrame by 'Date' to ensure correct calculation of returns
    df.sort_values('Date', inplace=True)

    # Calculate daily returns
    df['Daily_Returns'] = df['Close'].pct_change()

    # Calculate daily volatility
    daily_volatility = np.std(df['Daily_Returns'].dropna())

    # Calculate annualized volatility
    annualized_volatility = daily_volatility * np.sqrt(len(df))

    return daily_volatility, annualized_volatility

@app.route('/calculate_volatility', methods=['POST'])
def calculate_volatility_endpoint():
    try:
        # Check if the 'file' key is in the request files
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        # Check if the file is of CSV type
        if file and file.filename.endswith(".csv"):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file)

            # Calculate volatilities
            daily_volatility, annualized_volatility = calculate_volatility(df)

            # Return the results
            return jsonify({
                "daily_volatility": daily_volatility,
                "annualized_volatility": annualized_volatility
            })

        else:
            return jsonify({"error": "Invalid file format. Please provide a CSV file"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
