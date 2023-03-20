
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu

from data_page import data_page
from TF_page import TF_page
# from utils import set_page_container_style

from pathlib import Path
Image.MAX_IMAGE_PIXELS = None

max_width_str = f"max-width: 75%;"
st.markdown(f"""
            <style> 
            
            .appview-container .main .block-container{{{max_width_str}}}
            </style>    
            """,
            unsafe_allow_html=True,
            )


page_style = """
        <style>
        #MainMenu {visibility: hidden;}  
        footer  {visibility: hidden;}  
        div.css-1vq4p4l.e1fqkh3o4{padding: 2rem 1rem 1.5rem;}
        div.block-container{padding-top:3rem;}
        </style>
        """
st.markdown(page_style, unsafe_allow_html=True )


mainTitle2idx = {"Data overview": 0,
                 "TF activity analysis": 1,
                 "Protein-TF Correlation": 2
                 }



# def main_page(orisetting, cleanedsetting):
def main_page():

    pages = {
        "Data overview": data_page,
        "TF activity analysis": TF_page
    }

    path_data = Path(f"./data/TFexpressedFALSE_CLR1") 
    # st.write(str(path_data))
    with st.sidebar:
        default_value = st.session_state["main"] if "main" in st.session_state else 0
        # print( "main" in st.session_state)
        choose2 = option_menu("Menu", ["Data overview", "TF activity analysis"],
                            icons=['clipboard-data',
                                    'lightning-charge', ],
                            menu_icon="arrow-return-right", default_index=default_value,
                            styles={
            "container": {"padding": "5!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "18px"},
            "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "orange"},
        }
        )



    # if choose2 == "Protein-TF Correlation":
        
    #     correlation_page(path_data)

    # elif choose2 == "TF Analyses":
        
    #     TF_page(path_data)
    # elif choose2 == "Data Info":
        
    #     data_page(path_data)

    pages[choose2](path_data)
   
    # value = mainTitle2idx[choose2]
    # st.session_state["main"] = value
    
    
main_page()