import os
import pandas as pd
import numpy as np

# Predefined header
predefined_header = [
    "HUPD_Area_cm^2_Pt", "HUPD_rf_cm^2_Pt/cm^2_geo", "HUPD_ECSA_cm^2_Pt/g_Pt",
    "COStrip_Area_cm^2_Pt", "COStrip_rf_cm^2_Pt/cm^2_geo", "COStrip_ECSA_cm^2_Pt/g_Pt",
    "ORR_i_lim_A", "ORR_i_s_A/cm^2_Pt", "ORR_i_m_A/g_Pt", "ORR_i_k_ex_A",
    "ORR_i_s_ex_A/cm^2_Pt", "ORR_i_m_ex_A/g_Pt", "ORR_i_k_ex_eta_A",
    "ORR_i_s_ex_eta_A/cm^2_Pt", "ORR_i_m_ex_eta_A/g_Pt", "ORR_Tafel_slope_mV/dec",
    "ORR_Tafel_intercept", "ORR_Tafel_R", "ORR_Tafel_slope_eta_mV/dec",
    "ORR_Tafel_intercept_eta", "ORR_Tafel_R_eta", "HOR_cathodic_i_0_k_A",
    "HOR_cathodic_i_0_k_eta_A", "HOR_cathodic_i_0_s_µA_cm^2geo",
    "HOR_cathodic_i_0_s_eta_µA_cm^2geo", "HOR_cathodic_i_0_m_A_gPt",
    "HOR_cathodic_i_0_m_eta_A_gPt", "HOR_cathodic_slope", "HOR_cathodic_slope_eta",
    "HOR_cathodic_y_inter", "HOR_cathodic_y_inter_eta", "loading"
]

# Columns to include in the additional set of rows
additional_columns = [
    "HUPD_ECSA_cm^2_Pt/g_Pt", "COStrip_ECSA_cm^2_Pt/g_Pt",
    "ORR_i_m_ex_eta_A_g_Pt", "ORR_Tafel_slope_eta_mV/dec",
    "HOR_cathodic_i_0_m_eta_A_gPt", "loading"
]

def best_match(column_name, predefined_headers):
    best_match = None
    max_len = 0
    for header in predefined_headers:
        if column_name.startswith(header) and len(header) > max_len:
            best_match = header
            max_len = len(header)
    return best_match

def determine_measurement_type(file_name, file_path):
    if 'acidic' in file_name:
        return 'acidic'
    elif 'alkaline' in file_name:
        return 'alkaline'
    else:
        # Check the directory path for "acidic" or "alkaline"
        if 'acidic' in file_path.lower():
            return 'acidic'
        elif 'alkaline' in file_path.lower():
            return 'alkaline'
        else:
            return 'undefined'

def extract_number_and_comment(file_name):
    parts = file_name.split('-')
    number = parts[2] if len(parts) > 2 else None
    comment = parts[3].replace('_results.txt', '') if len(parts) > 3 else None
    return number, comment

def process_files(folder_path, output_csv):
    all_data = []

    # Recursively search for all files in the directory and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith("_results.txt"):
                file_path = os.path.join(root, file_name)

                # Extract the catalyst name, number, and comment from the filename
                catalyst_name = file_name.split('-')[0]
                number, comment = extract_number_and_comment(file_name)

                # Determine the measurement type
                measurement_type = determine_measurement_type(file_name, file_path)

                # Read the file into a dataframe
                df = pd.read_csv(file_path, sep='\t')

                # Create a dictionary to store the matched data, including the catalyst name, measurement type, number, and comment
                data_dict = {
                    'Catalyst': catalyst_name,
                    'Measurement_Type': measurement_type,
                    'Number': number,
                    'Comment': comment
                }
                data_dict.update({col: np.nan for col in predefined_header})

                for col in df.columns:
                    # Find the best matching predefined header
                    matched_col = best_match(col, predefined_header)
                    if matched_col:
                        data_dict[matched_col] = df[col].iloc[0]

                all_data.append(data_dict)

    # Create a dataframe from the aggregated data
    merged_df = pd.DataFrame(all_data)

    # Select only numeric columns for aggregation
    numeric_cols = merged_df.select_dtypes(include=[np.number]).columns.tolist()

    # Calculate the mean, standard deviation, and count for each group
    mean_df = merged_df.groupby(['Catalyst', 'Measurement_Type'])[numeric_cols].mean().reset_index()
    std_df = merged_df.groupby(['Catalyst', 'Measurement_Type'])[numeric_cols].std().reset_index()
    count_df = merged_df.groupby(['Catalyst', 'Measurement_Type']).size().reset_index(name='count')

    # Combine the comments for each group
    combined_comments = merged_df.groupby(['Catalyst', 'Measurement_Type'])['Comment'].apply(lambda x: '; '.join(filter(None, x))).reset_index()
    combined_comments.columns = ['Catalyst', 'Measurement_Type', 'Combined_Comments']

    # Prepare the new header for the combined data
    new_columns = []
    for col in numeric_cols:
        new_columns.append(col + '_mean')
        new_columns.append(col + '_std')

    # Combine the mean, standard deviation, count data, and comments
    combined_data = []
    for i in range(len(mean_df)):
        row = list(mean_df.iloc[i, :2])  # Catalyst and Measurement_Type
        row.append(count_df.iloc[i]['count'])
        row.append(combined_comments.iloc[i]['Combined_Comments'])
        for col in numeric_cols:
            row.append(mean_df.iloc[i][col])
            row.append(std_df.iloc[i][col])

        combined_data.append(row)

    combined_df = pd.DataFrame(combined_data, columns=['Catalyst', 'Measurement_Type'] + ['Measurement_Count', 'Combined_Comments'] + new_columns)

    # Rename columns for better clarity
    combined_df.rename(columns={'Catalyst': 'Catalyst_Average'}, inplace=True)
    combined_df.rename(columns={'Measurement_Type': 'Measurement_Type_Average'}, inplace=True)

    # Select only the specified additional columns
    additional_data = combined_df[['Catalyst_Average', 'Measurement_Type_Average', 'Measurement_Count', 'Combined_Comments']].copy()

    additional_data.rename(columns={'Catalyst_Average': 'Catalyst_Average_short'}, inplace=True)
    additional_data.rename(columns={'Measurement_Type_Average': 'Measurement_Type_Average_short'}, inplace=True)
    additional_data.rename(columns={'Measurement_Count': 'Measurement_Count_short'}, inplace=True)
    additional_data.rename(columns={'Combined_Comments': 'Combined_Comments_short'}, inplace=True)

    for col in additional_columns:
        if col + '_mean' in combined_df.columns and col + '_std' in combined_df.columns:
            additional_data[col + '_mean'] = combined_df[col + '_mean']
            additional_data[col + '_std'] = combined_df[col + '_std']

    # Reset index to ensure unique index values
    merged_df.reset_index(drop=True, inplace=True)
    combined_df.reset_index(drop=True, inplace=True)
    additional_data.reset_index(drop=True, inplace=True)

    # Concatenate the combined mean, standard deviation, and count values side by side with the additional data
    combined_side_by_side = pd.concat([combined_df, additional_data], axis=1)
    final_combined_df = pd.concat([merged_df, combined_side_by_side], axis=1)


    # Save the raw and combined data into separate parts of the final dataframe
    #raw_combined_df = pd.concat([merged_df, combined_df], ignore_index=True)
    #final_combined_df = pd.concat([raw_combined_df, additional_data], axis=1)

    # Save the final dataframe to a CSV file
    final_combined_df.to_csv(output_csv, index=False)
    print(f"All data has been successfully saved to '{output_csv}'")


# Example usage
folder_path = '//10.162.95.1/data/RRDE/RRDE_Data/03_LTCG/LTCG_3' # Replace with the path to your folder containing the result files
output_csv = '//10.162.95.1/data/RRDE/RRDE_Data/03_LTCG/LTCG_3/LTCG_3_results_all.csv' # Replace with your desired output CSV file name

process_files(folder_path, output_csv)
