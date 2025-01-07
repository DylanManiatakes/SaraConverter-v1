import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def process_sara_data(file_path):
    # Load CSV file into a pandas DataFrame
    sara_data = pd.read_csv(file_path)
    
    # Ensure critical columns are numeric and clean data
    sara_data['fc2'] = pd.to_numeric(sara_data['fc2'], errors='coerce')
    sara_data['sys_id'] = pd.to_numeric(sara_data['sys_id'], errors='coerce')
    sara_data['xmit_id'] = pd.to_numeric(sara_data['xmit_id'], errors='coerce')
    sara_data = sara_data.dropna(subset=['fc2', 'sys_id', 'xmit_id'])  # Drop rows with missing values

    # Convert to integers and create hex values
    sara_data['fc2'] = sara_data['fc2'].astype(int)
    sara_data['sys_id'] = sara_data['sys_id'].astype(int)
    sara_data['xmit_id'] = sara_data['xmit_id'].astype(int)
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

    # Save the processed data to a CSV file
    output_file = 'processed_arial_data.csv'
    arial_data.to_csv(output_file, index=False)
    return output_file

# GUI Implementation
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            output_file = process_sara_data(file_path)
            messagebox.showinfo("Success", f"File processed successfully. Saved to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Main function to launch the GUI
def main():
    root = tk.Tk()
    root.title("SARA Data Processor")

    tk.Label(root, text="Select a CSV file to process:").pack(pady=10)
    tk.Button(root, text="Browse", command=select_file).pack(pady=10)
    tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()