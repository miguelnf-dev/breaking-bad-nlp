import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from theme.theme_classifier import ThemeClassifier

def get_themes(theme_list, subtitles_path, save_path):
    themes = [theme.strip() for theme in theme_list.split(',') if theme.strip()]
    if not themes:
        st.error("Please enter at least one theme.")
        return None

    theme_classifier = ThemeClassifier(themes)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)
    
    # Sum the scores across all batches
    output_df = output_df[themes].sum().reset_index()
    output_df.columns = ['Theme', 'Score']
    
    # Normalize the scores so that they add up to 1
    total_score = output_df['Score'].sum()
    output_df['Score'] = output_df['Score'] / total_score
    
    return output_df

def main():
    st.set_page_config(
        layout="wide",
        page_title="BB",
        page_icon="🧪"
    )
    
    st.markdown("<h1 style='text-align: center;'>Theme Classification for the Breaking Bad Series</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image("images/bb2.png", width=300)

    st.markdown("<hr>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Input Parameters")
        default_themes = 'love, hope, fear, anger, joy, sadness, betrayal, courage, guilt, redemption'
        
        theme_list = st.text_area(
            "Themes (comma-separated)", 
            key="themes_input", 
            help="Enter themes separated by commas.",
            value=default_themes,
            height=100
        )
        
        subtitles_path = st.text_input("Subtitles or script Path", key="subtitles_input")
        save_path = st.text_input("Save Path", key="save_input")
        
        st.markdown("### Actions")
        if st.button("Get Themes", use_container_width=True):
            if theme_list and subtitles_path and save_path:
                df = get_themes(theme_list, subtitles_path, save_path)
                if df is not None:
                    st.session_state['df'] = df
                    st.session_state['theme_scores'] = df.set_index('Theme')['Score'].to_dict()
                    st.success(f"The themes have been saved to {save_path}")
            else:
                st.error("Please fill in all the fields.")

    with col2:
        st.markdown("### Theme Scores Visualization")
        if 'theme_scores' in st.session_state:
            theme_scores = st.session_state['theme_scores']
            fig, ax = plt.subplots(figsize=(12, 7))
            colors = sns.color_palette("husl", len(theme_scores))
            ax.barh(list(theme_scores.keys()), list(theme_scores.values()), color=colors)
            ax.set_xlabel("Score")
            ax.set_ylabel("Theme")
            ax.set_title("Theme Distribution")
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Graph will appear here after you click 'Get Themes'.")

if __name__ == "__main__":
    main()