import pandas as pd

def validate_and_map_data(data):
    # Define expected columns and their data types
    expected_columns = {
        'job_id': str,
        'company_name': str,
        'position_title': str,
        'location': str,
        'salary_range': str,
        'description': str,
        'post_date': str,
        'status': str
    }

    # Check if all required columns are present
    missing_columns = [col for col in expected_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    # Validate data types
    for column, dtype in expected_columns.items():
        if not all(isinstance(value, dtype) for value in data[column]):
            raise TypeError(f"Column '{column}' should be of type {dtype.__name__}")

    # Map job status to a standardized format
    def map_status(status):
        if pd.isna(status):
            return 'Unknown'
        elif 'open' in status.lower():
            return 'Open'
        elif 'closed' in status.lower() or 'expired' in status.lower():
            return 'Closed'
        else:
            return 'Unknown'

    data['status'] = data['status'].apply(map_status)

    # Remove duplicates
    data.drop_duplicates(inplace=True)

    return data

# Example usage
data = pd.DataFrame({
    'job_id': ['123', '456'],
    'company_name': ['ABC Corp', 'XYZ Inc'],
    'position_title': ['Software Engineer', 'Data Analyst'],
    'location': ['New York, NY', 'San Francisco, CA'],
    'salary_range': ['$80k-$120k', '$70k-$90k'],
    'description': ['Develop software applications.', 'Analyze data and provide insights.'],
    'post_date': ['2023-04-01', '2023-03-15'],
    'status': ['Open', 'Closed']
})

validated_data = validate_and_map_data(data)
print(validated_data)