from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from utils import hide_table_index, hide_dataframe_index
import os
from PIL import Image


path = "./data"
protein_names = pd.read_csv(Path(path)/"protein_names.csv", index_col=0).T
celltype_names = pd.read_csv(Path(path)/"celltype_names.csv", index_col=0).T


cell_count = pd.read_csv(Path(path)/"celltype_count.csv")
cell_count.index.name = None



def data_page(path_data):

    spartan_data = pd.read_csv(
        Path(path_data)/"celltype_info.csv", index_col=0)

    spartan_data.dropna(inplace=True)
    
    spartan_data.rename(columns={"RNA.rate": "RNA rate", "Protein.rate": "Protein rate"}, inplace=True)

    selected = option_menu(None, ["Data info",  "SPaRTAN data"],
                           icons=["clipboard", "clipboard-plus"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "5!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "22px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#FD5816"},
        # "separator":"."
    })

    if selected == "Data info":

    
        hide_table_index()
        # st.write("Cell types (24):")
        st.markdown('''###### Cell types (24):''')
        st.table(celltype_names)

        # write_text("Proteins (52):", fontsize=10)
        # st.write("")
        st.markdown('''###### Proteins (52):''')
        st.table(protein_names)

        # show_dataframe_index()
        c,_ = st.columns([5,7])
        c.markdown('''###### Cell count:''')
        c.table(cell_count)

    elif selected == "SPaRTAN data":
        st.info("We combined the data by cell-type and trained the SPaRTAN model for each cell-type. The genes and proteins expressed less than 3\% cells were filtered out in each cell-type. Cell-types which have less than 50 cells were not used. \"protein exluded\" field in the following table does not count 5 isotype/lsotype controls (Mouse(IgG1-kisotype), Mouse(IgG2a-kisotype), Mouse(IgG2b-kisotype), Mouse(IgM-kIsotype), Rat(IgG2a-kIsotype).")

        st.table(spartan_data.style.format(
            {'RNArate': '{:.2f}', 'Number of genes': '{:.0f}', 'Number of TFs': '{:.0f}', 'Number of proteins': '{:.0f}',  'RNA rate': '{:.2f}',  'Protein rate': '{:.2f}' }))
        # from st_aggrid import AgGrid
        # AgGrid(spartan_data, height=500, fit_columns_on_grid_load=True)
