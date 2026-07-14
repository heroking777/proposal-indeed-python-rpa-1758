import csv
import requests

# Function to delete job postings from Indeed based on a CSV file
def delete_indeed_jobs(csv_file_path):
    # Replace with your Indeed API endpoint and credentials
    api_url = "https://api.indeed.com/employer/v1/delete"
    api_key = "your_api_key_here"

    # Open the CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            job_id = row['job_id']  # Assuming 'job_id' is a column in your CSV

            # Prepare the payload
            payload = {
                "jobId": job_id,
                "apiKey": api_key
            }

            # Make the API request to delete the job posting
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                print(f"Job ID {job_id} deleted successfully.")
            else:
                print(f"Failed to delete Job ID {job_id}. Status code: {response.status_code}, Response: {response.text}")

# Example usage
delete_indeed_jobs('path_to_your_csv_file.csv')
```

Please note that this script assumes you have an Indeed API endpoint and credentials. You will need to replace `"your_api_key_here"` with your actual Indeed API key. Additionally, the CSV file should contain a column named `job_id` which holds the job IDs of the postings you want to delete. Adjust the column name as necessary based on your CSV structure.