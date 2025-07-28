import streamlit as st
import os
from typing import Optional

def handle_uploaded_file(uploaded_file, save_path: str = 'dataset/') -> str:
    """
    Save the uploaded file to the specified directory.

    Args:
        uploaded_file: Streamlit UploadedFile object
        save_path (str): Directory path to save the uploaded file

    Returns:
        str: Full file path where the file was saved
    """
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def load_file(uploaded_file) -> Optional[str]:
    """
    Load and decode text from an uploaded file.

    Args:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        Optional[str]: Decoded file content as string, or None if not uploaded
    """
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        try:
            text_data = bytes_data.decode("utf-8")
            return text_data
        except UnicodeDecodeError:
            st.error("🚫 File couldn't be decoded. Please upload a valid UTF-8 text file.")
    return None
