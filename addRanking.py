import pandas as pd
import numpy as np
import os
import glob

def add_rankings_to_csv(input_file, output_file):
    """
    Add rankings to each subject and composite score in the CSV file and reorganize columns.
    
    Input format: chinese, maths, total, chinese, maths, total (score columns followed by grade columns)
    Output format: score-chinese, score-maths, score-total, grade-chinese, grade-maths, grade-total, rank-chinese, rank-maths, rank-total
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Get the column names
    columns = df.columns.tolist()
    
    # Define columns that should not be ranked (non-numeric identifiers)
    non_ranking_columns = ['ID', '学号', '姓名', 'id', 'student_id', 'name']
    
    # Assuming the first half of columns are scores and second half are grades
    # For the same subjects
    num_columns = len(columns)
    half_point = num_columns // 2
    
    # Separate student info columns from subject columns
    student_info_cols = []
    subject_cols = []
    
    for col in columns:
        base_col = col.split('.')[0]
        if base_col in non_ranking_columns:
            student_info_cols.append(col)
        else:
            subject_cols.append(col)
    
    # Split subject columns into scores and grades
    score_cols = subject_cols[:len(subject_cols)//2]
    grade_cols = subject_cols[len(subject_cols)//2:]
    
    # Create a new dataframe with reorganized columns
    new_df = pd.DataFrame()
    
    # 1. Add student info columns first
    for col in student_info_cols:
        new_df[col] = df[col]
    
    # 2. Add score columns with "score-" prefix
    for col in score_cols:
        base_col = col.split('.')[0]
        new_df[f'score-{base_col}'] = df[col]
    
    # 3. Add grade columns with "grade-" prefix
    for col in grade_cols:
        base_col = col.split('.')[0]
        new_df[f'grade-{base_col}'] = df[col]
    
    # 4. Add ranking columns for each subject
    for col in score_cols:
        base_col = col.split('.')[0]
        
        # Get the values for this column
        values = df[col]
        
        # Remove NaN values for ranking
        valid_values = values.dropna()
        
        if len(valid_values) > 0:
            # Try to convert to numeric for ranking
            try:
                numeric_values = pd.to_numeric(valid_values, errors='coerce')
                # Remove NaN values after conversion
                numeric_values = numeric_values.dropna()
                
                if len(numeric_values) > 0:
                    # Create ranking (same rank for same values)
                    # Use method='min' to handle ties properly - same rank for tied values, skip next rank
                    ranks = numeric_values.rank(method='min', ascending=False).astype(int)
                    
                    # Create a series with the same index as original df
                    ranking_series = pd.Series(index=df.index, dtype='object')
                    ranking_series.loc[numeric_values.index] = ranks
                    
                    # Add to new dataframe
                    new_df[f'rank-{base_col}'] = ranking_series
                else:
                    # If no valid numeric values, add empty column
                    new_df[f'rank-{base_col}'] = np.nan
            except:
                # If conversion fails, add empty column
                new_df[f'rank-{base_col}'] = np.nan
        else:
            # If no valid values, add empty column
            new_df[f'rank-{base_col}'] = np.nan
    
    # Save to output file
    new_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Successfully processed {input_file} -> {output_file}")
    print(f"Input columns: {columns}")
    print(f"Output columns: {new_df.columns.tolist()}")

def process_file(file_number):
    """
    Process a specific file number.
    
    Args:
        file_number (str): The file number (e.g., "13", "27")
    """
    input_file = f"output/lsoutput-{file_number}.csv"
    output_file = f"output/rankingoutput-{file_number}.csv"
    
    if os.path.exists(input_file):
        add_rankings_to_csv(input_file, output_file)
    else:
        print(f"File {input_file} not found!")

def process_all_lsoutput_files():
    """
    Process all lsoutput CSV files in the output directory.
    """
    # Find all lsoutput CSV files
    pattern = "output/lsoutput-*.csv"
    lsoutput_files = glob.glob(pattern)
    
    if not lsoutput_files:
        print("No lsoutput CSV files found in output directory!")
        return
    
    print(f"Found {len(lsoutput_files)} lsoutput CSV files to process:")
    for file_path in lsoutput_files:
        print(f"  - {file_path}")
    
    print("\nProcessing files...")
    
    for file_path in lsoutput_files:
        # Extract file number from filename
        filename = os.path.basename(file_path)
        file_number = filename.replace("lsoutput-", "").replace(".csv", "")
        
        # Create output filename
        output_file = f"output/rankingoutput-{file_number}.csv"
        
        print(f"\nProcessing file {file_number}...")
        add_rankings_to_csv(file_path, output_file)
    
    print(f"\nAll {len(lsoutput_files)} files processed successfully!")

if __name__ == "__main__":
    # Process all lsoutput files automatically
    process_all_lsoutput_files()
