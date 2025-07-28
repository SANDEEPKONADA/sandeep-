import streamlit as st
import pandas as pd
from typing import Optional

def convert_df_to_csv(df: pd.DataFrame) -> bytes:
    """Convert DataFrame to CSV in bytes format."""
    return df.to_csv(index=False).encode('utf-8')

def download_button(df: pd.DataFrame, filename: Optional[str] = 'chat_export.csv') -> None:
    """Render a Streamlit download button for the CSV."""
    if df is not None and not df.empty:
        csv_data = convert_df_to_csv(df)
        st.download_button(
            label="📥 Download Chat Data as CSV",
            data=csv_data,
            file_name=filename,
            mime='text/csv',
        )
    else:
        st.warning("⚠️ No data available to download.")
