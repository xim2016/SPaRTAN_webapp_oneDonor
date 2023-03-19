import random
from pathlib import Path

import pandas as pd
import pickle
import streamlit as st
from streamlit_option_menu import option_menu

from utils import convert_df_to_csv, img2buf, load_data, violin_plot
from register_load_widget_state import  persist

ordered_celltypes = [ "LT-HSC.HLF","HSC.HIST1H2AC","HSC.WNT11","HSC.CACNB2","HSC.MYADM-CD97","ST-HSC.PBX1","LMPP.CDK6-FLT3","MPP.SPINK2-CD99","MPP.Ribo-high","pre-MEP","MEP-MKP","ERP","BMCP","ML-Gran","MultiLin-ATAC","pre-Gran.CP","LMPP.PRSSI","LMPP.LSAMP","LMPP.Naive.T-cell"]


my_theme = {'txc_inactive': 'black', 'menu_background': 'white',
            'txc_active': 'white', 'option_active': 'blue'}


def TF_page(path_data):


    # celltype_list_ordered = pd.read_csv(path_data/"celltype_list_ordered.csv")
    # group_order_type = list(celltype_list_ordered["Cell_type"].str.replace(" ", "."))

    @st.cache
    def load_rootdata(path_data):
        fname = str(
            path_data / "celltype_info.csv")
        df_info = pd.read_csv(fname, index_col=0)

        df_ranks_all = pd.read_parquet(path_data/"TFranks_all.parquet.gzip")
        
        with open(path_data/"TFmean_forEachCelltype.pkl", 'rb') as f:
           celltype_TFmean = pickle.load(f)
        
        return ((df_info, df_ranks_all, celltype_TFmean))

    cached_data = load_rootdata(path_data)
    
    df_info = cached_data[0]
    
    df_ranks_all = cached_data[1]
    tfall = df_ranks_all.columns[:-1]
    
    celltype_TFmean = cached_data[2]
    
    celltype_TFcount = {}
    for k in celltype_TFmean.keys():
        celltype_TFcount[k] = len(celltype_TFmean[k])
    
    
    celltypeAll = df_info.index

   
   
    # start menu options
    selected = option_menu(None, ["Analysis by TFs", "Analysis by cell-type"],
                        #    icons=["bi bi-grid-3x3", "bi bi-align-end",
                        #           "bi bi-align-bottom"],
                           menu_icon="cast", default_index=0, orientation="horizontal",
                           styles={
        "container": {"padding": "20!important", "background-color": "#eee"},
        "icon": {"color": "orange", "font-size": "18px"},
        "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#FD5816"},
        "separator": "A"
    })

    datafile = ""
    # if selected == 'TF ranks overview':

    #     st.info('The heatmap shows the sample mean of TF ranks for every TF and every cell type. TFs that rank lower than 0.5(50\%) in all cell types have been removed.')

    #     imgfile = str(
    #         path_data / "TFrank/mean/figure/heatmap_TFrank_celltypeMean_cutoff0.5.png")
    #     imgfile_out = "heatmap_TFrank_celltypeMean.png"

    #     # _, c_img, _ = st.columns([1,100,1])
    #     st.image(imgfile)
    #     datafile = str(path_data / "TFrank/mean/TFrank_celltypeMean.csv")
    #     datafile_out = "TFrank_celltypeMean.csv"

    if selected == 'Analysis by TFs':
        st.info('For each TF, violin plot shows its ranks across cell types. You can select multiple TFs of your interest from TFs list for comparison.')
        # violin plot for selected TFs]]    
        # defaults = st.session_state['1_tf'] if "1_tf" in st.session_state and set(st.session_state['1_tf']).issubset(set(tfall)) and len(set(st.session_state['1_tf']))>0 else [tfall[0]]
    
        if "tfpage_tab1_tf" in st.session_state:
            if not set(st.session_state.tfpage_tab1_tf).issubset(set(tfall)): 
                 st.session_state.tfpage_tab1_tf = list(set(st.session_state.tfpage_tab1_tf) & set(tfall))

        TFs_selected = st.multiselect('TFs', tfall,  default=tfall[0], key=persist("tfpage_tab1_tf"))
        for tf in TFs_selected:
            df_ranks = df_ranks_all.loc[:, [tf, "Celltype"]]

            fig = violin_plot(tf , df_ranks, "Celltype",tf, 25, 4)
            st.pyplot(fig)


        s_TFs = "_".join(TFs_selected)
        s_TFs if len(s_TFs) <= 100 else s_TFs[:100]
        datafile_out = f"TFranks--{s_TFs}.csv"


        df_data = df_ranks_all[['Celltype'] + TFs_selected]

        c_checkbox, _, c_dwdata = st.columns([3, 9, 3])
        cb = c_checkbox.checkbox("Show data", key="TFrank")


        btn_data = c_dwdata.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
            disabled=not cb
        )

        if cb:
            st.dataframe(df_data.style.format(precision=0), use_container_width=True)

        
    elif selected == 'Analysis by cell-type':

        st.info('For each cell type, get the mean expression of every TF. The table is sorted by the TF expression value. The bigger the value, the higher the rank.')
       
        s_celltype = st.selectbox(f'Cell types ({len(celltypeAll)})', celltypeAll,  key=persist("tfpage_tab2_type"),
                                  format_func=lambda x: x + " (Num of TFs: " + str(celltype_TFcount[x])+ ")")
        
        df_data = celltype_TFmean[s_celltype].round(2).to_frame()
        df_data.columns = ["TF expression"]
                
        c0,c1,c,c2 = st.columns([1, 5,1,3])
        
        c1.table(df_data.style
        
            .background_gradient(
                cmap="Blues", #viridis
                axis=0
             )
            .format(
                {'TF rank': '{:.0f}', 'TF expression': '{:.2f}' }
            )
        )
        
        
        datafile_out = f"TFexpression_of_{s_celltype}.csv"
        
        cb = c2.download_button(
            label='📩 '+"Download Data",
            data=convert_df_to_csv(df_data),
            file_name=datafile_out,
            mime="text/csv",
            key='download-csv',
        )
