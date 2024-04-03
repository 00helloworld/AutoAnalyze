import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
from src.explorer import Explorer


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)



# Initialize status
if 'upload_file' not in st.session_state:
    st.session_state['upload_file'] = False
if 'confirm_type' not in st.session_state:
    st.session_state.confirm_type = False
if 'start_process' not in st.session_state:
    st.session_state.start_process = False

def init_session_state():
    st.session_state['upload_file'] = False
    st.session_state.confirm_type = False
    st.session_state.start_process = False

# print('st.session_state.upload_file: ', st.session_state.upload_file)
# print('st.session_state.confirm_type: ', st.session_state.confirm_type)
# print('st.session_state.start_process: ', st.session_state.start_process)


# Uploade File
st.header('Upload Data File')
uploader = st.file_uploader('please choose a file', type=['csv'], on_change=init_session_state)
if not uploader:
    st.write('**Step 1: Upload a file**')
    st.write('**Step 2: Confirm Data Information**')
    st.write('**Step 3: Automatically perform analysis and visaulization**')
    pass

else:
    st.header('Data Description')
    st.subheader('Raw Data')
    data_load_state = st.text('Loading data...')
    exp = Explorer(uploader)
    data_load_state.text('Loading data...done!')
    st.write(exp.data.head())

    st.subheader('Data Info')
    st.text(exp.info)

    st.header('Please Confirm Data Type')
    with st.form('select box'):
        layout_left, layout_right = st.columns(2)
        with layout_left:
            type_mapping = {
                np.dtype('object'): 'Object',
                np.dtype('int64'): 'Integer',
                np.dtype('float64'): 'Float'
            }
            types = exp.data.dtypes.map(type_mapping).tolist()
            
            type_df = pd.DataFrame(
                {
                    "Columns": exp.data.columns,
                    "Data Type": types
                }
            )

            edited_type_df = st.data_editor(
                type_df,
                column_config={
                    "Data Type": st.column_config.SelectboxColumn(
                        width="medium",
                        options=[
                            "Object",
                            "Integer",
                            "Float",
                            "DateTime",
                        ],
                        required=True,
                    )
                },
                hide_index=True,
            )
        with layout_right:
            st.write('Please confirm every data type')
            st.write('If you want to change data type, just double-click type and chose which you want.')
            st.write('If there is a Datetime, it will plot line plot based on the Datetime.')
            st.write('If everyting is ready, click Confirm.')
            confirm = st.form_submit_button("Confirm")
            if confirm:
                st.session_state.confirm_type = True
    if st.session_state.confirm_type:
        st.write("Data Type Confirmed!")
        st.write("Now You Can Start The Process!")
        start = st.button("Get Started!")
        if start:
            st.session_state.start_process = True
        # print(edited_type_df)  # pass it to exp object


    if st.session_state.start_process:
        # TODO: 先处理缺失值还是先处理数据类型，还是先展示数据？
        # Check and cast data types
        exp.cast_type(edited_type_df)

        # Check data quality
        st.header('Data Quality Check')
        st.subheader('Missing Value Check')
        missing_info = exp.missing_value()
        st.write(missing_info)
        st.text('检查缺失值，自动处理缺失值')
        st.text('数据筛选')


        # Visualize Categorical Features
        st.header('Categorical Features')
        cat_figures = exp.categorical()
        for i, fig in enumerate(cat_figures):
            st.subheader(exp.cat_cols[i])
            st.pyplot(fig)

        # Visualize Numerical Features
        st.header('Numerirical Features')
        num_figures, description_dicts = exp.numerical()
        for i, fig in enumerate(num_figures):
            st.subheader(exp.num_cols[i])
            # if st.checkbox('Show statistics', key='statistics_'+exp.num_cols[i]):
            st.write(description_dicts[i])
            st.pyplot(fig)

        # Correlation Heat Map
        st.header('Correlation')
        st.subheader('Heatmap')
        fig = exp.corr_heatmap()
        st.pyplot(fig)
        st.header('To be continued..')