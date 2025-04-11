import pandas as pd

def remove_outliers_by_segments(df, depth_column, threshold=3, min_segment_length=4):
    """
    Processes the DataFrame to keep only contiguous segments in which every
    consecutive pair of points (in the depth column) has an absolute difference
    <= threshold. Rows that are not part of any valid segment are removed.
    
    Parameters:
        df (pd.DataFrame): The original DataFrame.
        depth_column (str): The name of the column with depth data.
        threshold (float): Maximum allowed difference between consecutive depth values.
        min_segment_length (int): Minimum number of points in a valid segment.
        
    Returns:
        pd.DataFrame: A new DataFrame containing only the rows from valid segments.
    """
    segments = []
    # Start with the first row index
    current_segment = [0]
    
    for i in range(len(df) - 1):
        current_value = df.loc[i, depth_column]
        next_value = df.loc[i+1, depth_column]
        # Check if the absolute difference is within the threshold
        if abs(next_value - current_value) <= threshold:
            current_segment.append(i+1)
        else:
            # End the current segment; only keep if it has at least min_segment_length rows
            if len(current_segment) >= min_segment_length:
                segments.append(current_segment)
            # Reset segment starting with the next index
            current_segment = [i+1]
    
    # Check the final segment
    if len(current_segment) >= min_segment_length:
        segments.append(current_segment)
    
    # Combine all indices from valid segments
    keep_indices = sorted({idx for seg in segments for idx in seg})
    return df.loc[keep_indices].reset_index(drop=True)

if __name__ == '__main__':
    # File paths (update if needed)
    input_file = r'C:\Users\Talha.Khan\OneDrive - South Dakota State University - SDSU (1)\Desktop\SDSU\Thesis\SwineBarn\Data after pigs\3rd Week\d-sensor3.xlsx'
    output_file = r'C:\Users\Talha.Khan\OneDrive - South Dakota State University - SDSU (1)\Desktop\SDSU\Thesis\SwineBarn\Data after pigs\3rd Week\d-sensor3_my_filter_th3_msegl4.xlsx'
    
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Convert the 'depth' column to numeric (coerce errors) and drop rows with NaN in depth
    df['distance'] = pd.to_numeric(df['distance'], errors='coerce')
    df = df.dropna(subset=['distance']).reset_index(drop=True)
    
    # Optionally sort by date and time if these columns exist, to ensure correct time order.
    if 'date' in df.columns and 'time' in df.columns:
        df = df.sort_values(by=['date', 'time']).reset_index(drop=True)
    
    # Remove outliers from the 'depth' column based on contiguous segments
    df_filtered = remove_outliers_by_segments(df, 'distance', threshold=3, min_segment_length=4)
    
    # Save the final filtered data to a new Excel file, preserving all original columns
    df_filtered.to_excel(output_file, index=False)
    print(f"Filtered data saved to {output_file}")
