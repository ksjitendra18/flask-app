from flask import Flask, render_template, request
import pandas as pd
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_cors import CORS



app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])

# Load your data into a DataFrame (replace with your data source)
df = pd.read_csv('sales_data.csv')

# Assuming your data is in a DataFrame called 'df'
df['date_of_order'] = pd.to_datetime(df['date_of_order'], format='%d-%m-%Y')
# df['date_of_order'] = pd.to_datetime(df['date_of_order'])
df['month'] = df['date_of_order'].dt.strftime('%Y-%m')


@app.route('/')
def index():
    months = df['month'].unique()
    return render_template('index.html', months=months)


@app.route('/generate_graph', methods=['POST'])
def generate_graph():
    selected_month = request.form.get('selected_month')

    # Generate the graph for date of order vs. number of orders
    selected_data = df[df['month'] == selected_month]
    plt.figure(figsize=(10, 6))
    plt.plot(selected_data['date_of_order'], selected_data['no_of_orders'])
    plt.xlabel('Date of Order')
    plt.ylabel('Number of Orders')
    plt.title(f'Number of Orders for {selected_month}')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Save the graph to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.read()).decode("utf-8")

    # Close the plot to prevent memory leaks
    plt.close()

    return json.dumps({'image_data': image_data})


@app.route('/graph', methods=['POST'])
def gen_graph():
    selected_month = request.form.get('selected_month')
    # selected_month = "2023-03"

    # Generate the graph for date of order vs. number of orders
    selected_data = df[df['month'] == selected_month]
    plt.figure(figsize=(10, 6))
    plt.plot(selected_data['date_of_order'], selected_data['no_of_orders'])
    plt.xlabel('Date of Order')
    plt.ylabel('Number of Orders')
    plt.title(f'Number of Orders for {selected_month}')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

    # Save the graph to a BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format="png")
    image_stream.seek(0)
    image_data = base64.b64encode(image_stream.read()).decode("utf-8")

    # Close the plot to prevent memory leaks
    plt.close()

    return json.dumps({'image_data': image_data})


if __name__ == '__main__':
  app.run(debug=True, port=os.getenv("PORT", default=5000))
