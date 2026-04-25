import pandas as pd


def get_variable_metadata(metadata_df, variable_to_search):
    found_metadata = metadata_df[metadata_df['Variable'] == variable_to_search]

    if found_metadata.empty:
        print(f"Variable '{variable_to_search}' not found in metadata_df.")
        return None

    if 'Descripción' in found_metadata.columns:
        description = found_metadata['Descripción'].iloc[0]
        print(f"\nDescription of '{variable_to_search}': {description}")

    return found_metadata


def get_variable_dictionary(metadata_df, variable_to_search, file_path):
    dict_info = metadata_df[metadata_df['Variable'] == variable_to_search]

    if dict_info.empty:
        print(f"Variable '{variable_to_search}' not found in metadata_df.")
        return None

    sheet_name = dict_info['Diccionario ubicado en la hoja…'].iloc[0]

    if pd.isna(sheet_name):
        print(f"No specific dictionary sheet found for variable '{variable_to_search}'.")
        return None

    print(f"Dictionary for '{variable_to_search}' is located in sheet: '{sheet_name}'")

    try:
        dictionary_sheet_df = pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        print(f"Error loading sheet '{sheet_name}': {e}")
        return None

    variable_code_in_dict = dict_info['Diccionario de la variable'].iloc[0]
    start_row_candidates = dictionary_sheet_df[dictionary_sheet_df.iloc[:, 0] == variable_code_in_dict].index

    if start_row_candidates.empty:
        print(f"Could not find the dictionary section for '{variable_to_search}' (code: '{variable_code_in_dict}') in the sheet.")
        return None

    start_row_idx = start_row_candidates[0]
    header_row_idx = start_row_idx + 1
    dict_headers = dictionary_sheet_df.iloc[header_row_idx, [0, 1]].tolist()

    subsequent_sections = dictionary_sheet_df.iloc[header_row_idx + 1:].iloc[:, 0].astype(str)
    end_candidates = subsequent_sections[
        (subsequent_sections == 'Código') | (subsequent_sections.str.startswith('T', na=False))
    ].index

    end_of_dict_idx = end_candidates[0] if not end_candidates.empty else len(dictionary_sheet_df)

    variable_dict_df = dictionary_sheet_df.iloc[header_row_idx + 1:end_of_dict_idx, [0, 1]].copy()
    variable_dict_df.columns = dict_headers
    variable_dict_df = variable_dict_df.dropna(how='all')

    print(f"\nExtracted dictionary for '{variable_to_search}' (code: '{variable_code_in_dict}'):")

    return variable_dict_df
