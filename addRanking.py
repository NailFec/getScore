import pandas as pd
import numpy as np
import os
import glob

def add_rankings_to_csv(input_file, output_file):
    """
    Add rankings to each subject and composite score in the CSV file and reorganize columns.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Get the column names
    columns = df.columns.tolist()
    
    # Define all possible columns that need rankings (subjects, levels, and composite scores)
    ranking_columns = [
        # Regular subjects
        '语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理', '信息',
        # Subject levels (like 物理等级)
        '物理等级', '化学等级', '生物等级', '政治等级', '历史等级', '地理等级', '信息等级',
        # Composite scores
        '语数英总分', '总分', '理科总分', '文科总分', '六门折算总分'
    ]
    
    # Find the positions of score columns and grade columns
    score_cols = []
    grade_cols = []
    
    for i, col in enumerate(columns):
        if col in ranking_columns:
            # Check if this is a score column (numeric values) or grade column (letter grades)
            if i < len(columns) - 1:  # Not the last column
                # Look at the first few non-null values to determine if it's scores or grades
                sample_values = df[col].dropna().head(10)
                if len(sample_values) > 0:
                    # Check if the first value is numeric (score) or string (grade)
                    first_val = str(sample_values.iloc[0])
                    if first_val.replace('.', '').replace('-', '').isdigit() or '.' in first_val:
                        score_cols.append((col, i))
                    else:
                        grade_cols.append((col, i))
    
    # Create a new dataframe with reorganized columns
    new_df = pd.DataFrame()
    
    # Add student info columns (first 3 columns)
    student_info_cols = columns[:3]
    for col in student_info_cols:
        new_df[col] = df[col]
    
    # Add score columns with "score-" prefix
    for col, pos in score_cols:
        new_df[f'score-{col}'] = df[col]
    
    # Add grade columns with "grade-" prefix
    for col, pos in grade_cols:
        new_df[f'grade-{col}'] = df[col]
    
    # Add ranking columns for all ranking columns
    for ranking_col in ranking_columns:
        # Find the score column for this ranking column
        score_col = None
        for col, pos in score_cols:
            if col == ranking_col:
                score_col = col
                break
        
        if score_col:
            # Get the scores for this column
            scores = df[score_col]
            
            # Remove NaN values for ranking
            valid_scores = scores.dropna()
            
            if len(valid_scores) > 0:
                # Create ranking (same rank for same scores)
                # Use method='min' to handle ties properly - same rank for tied scores, skip next rank
                ranks = valid_scores.rank(method='min', ascending=False).astype(int)
                
                # Create a series with the same index as original df
                ranking_series = pd.Series(index=df.index, dtype='object')
                ranking_series.loc[valid_scores.index] = ranks
                
                # Add to new dataframe
                new_df[f'rank-{ranking_col}'] = ranking_series
            else:
                # If no valid scores, add empty column
                new_df[f'rank-{ranking_col}'] = np.nan
    
    # Save to output file
    new_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Successfully processed {input_file} -> {output_file}")

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
