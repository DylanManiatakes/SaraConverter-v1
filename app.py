from flask import Flask, render_template, request, send_file
import pandas as pd
import os


app = Flask(__name__)
app.run(host='0.0.0.0', port=5000)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change to a strong secret key for production
app = Flask(__name__, static_folder='static')




# Function to process the Sara data
def process_sara_data(file_path):
    # Load the uploaded file
    sara_data = pd.read_csv(file_path)
    
    # Ensure critical columns are numeric and clean data
    sara_data['fc2'] = pd.to_numeric(sara_data['fc2'], errors='coerce')
    sara_data['sys_id'] = pd.to_numeric(sara_data['sys_id'], errors='coerce')
    sara_data['xmit_id'] = pd.to_numeric(sara_data['xmit_id'], errors='coerce')
    
    # Drop rows with missing values in critical fields
    sara_data = sara_data.dropna(subset=['fc2', 'sys_id', 'xmit_id'])
    
    # Convert to integers
    sara_data['fc2'] = sara_data['fc2'].astype(int)
    sara_data['sys_id'] = sara_data['sys_id'].astype(int)
    sara_data['xmit_id'] = sara_data['xmit_id'].astype(int)
    
    # Hex conversion with zero padding for single digits
    sara_data['fc2_hex'] = sara_data['fc2'].apply(lambda x: format(x, 'x').zfill(2))
    sara_data['sys_id_hex'] = sara_data['sys_id'].apply(lambda x: format(x, 'x').zfill(2))
    sara_data['xmit_id_hex'] = sara_data['xmit_id'].apply(lambda x: format(x, 'x').zfill(2))
    
    # Combine hex and convert to decimal
    sara_data['SerialNumber'] = (sara_data['fc2_hex'] +
                                 sara_data['sys_id_hex'] +
                                 sara_data['xmit_id_hex']).apply(lambda x: int(x, 16))
    
    # Filter out rows with SerialNumber == 0
    sara_data = sara_data[sara_data['SerialNumber'] != 0]
    
    # Map alarm_device_type to TypeID
    sara_data['TypeID'] = sara_data['alarm_device_type']
    
    # Select final fields for Arial import
    arial_data = sara_data.rename(columns={
        'alarm_description': 'Description',
        'last_check_in': 'LastCheckIn'
    })[['SerialNumber', 'TypeID', 'Description', 'LastCheckIn']]
    
    # Save the processed data to a temporary file
    output_file = 'processed_arial_data.csv'
    arial_data.to_csv(output_file, index=False)
    return output_file

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded", 400
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400
        
        # Save the uploaded file
        file_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(file_path)
        
        # Process the file
        processed_file = process_sara_data(file_path)
        return send_file(processed_file, as_attachment=True, download_name='Arial_Import.csv')
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
