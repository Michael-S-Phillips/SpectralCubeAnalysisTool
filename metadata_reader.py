import logging
from spectral import envi

def read_band_names_from_hdr(image_path):
    """
    Reads band names from the .hdr file associated with a hyperspectral image.
    
    Parameters:
    image_path (str): The file path to the hyperspectral image.
    
    Returns:
    list: A list of band names if available, otherwise returns a list of integers as strings representing band numbers.
    """
    try:
        # Assuming the .hdr file is in the same directory and has the same name as the image file.
        hdr_file_path = image_path + '.hdr'  # INPUT_REQUIRED {Ensure the .hdr file path is correctly formed based on your file naming and directory structure}
        
        # Open the .hdr file using the spectral library
        header = envi.open(hdr_file_path)
        
        # Extract band names if available
        if hasattr(header, 'band_names') and header.band_names:
            logging.info(f"Band names successfully read from {hdr_file_path}.")
            return header.band_names
        else:
            # Fallback to generating band numbers as strings if band names are not available
            logging.warning(f"No band names found in {hdr_file_path}. Falling back to band numbers.")
            return [str(i+1) for i in range(header.nbands)]
    except Exception as e:
        logging.error(f"Error reading band names from HDR file: {hdr_file_path}. Error: {e}", exc_info=True)
        # In case of any error, return an empty list to indicate failure
        return []