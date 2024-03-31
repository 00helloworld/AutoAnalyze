import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io
from explorer import Explorer

data_path = 'dev/insurance.csv'



st.header('Data Description')
st.subheader('Raw Data')
data_load_state = st.text('Loading data...')
exp = Explorer(data_path)
data_load_state.text('Loading data...done!')
st.write(exp.data.head())

st.subheader('Data Info')
st.text(exp.info)


st.header('Data Quality Check')
st.text('检查数据类型，转换为设置好的类型')
st.text('检查缺失值，自动处理缺失值')
st.text('数据筛选')



st.header('Categorical Features')
cat_figures = exp.categorical()
for i, fig in enumerate(cat_figures):
    st.subheader(exp.cat_cols[i])
    st.pyplot(fig)


st.header('Numerirical Features')
num_figures, description_dicts = exp.numerical()
for i, fig in enumerate(num_figures):
    st.subheader(exp.num_cols[i])
    # if st.checkbox('Show statistics', key='statistics_'+exp.num_cols[i]):
    st.write(description_dicts[i])
    st.pyplot(fig)


st.header('Correlation')
st.subheader('Heatmap')
fig = exp.corr_heatmap()
st.pyplot(fig)
st.subheader('散点图趋势曲线')