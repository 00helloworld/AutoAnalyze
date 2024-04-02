import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import io


class Explorer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        # self.data = pd.read_html('https://en.wikipedia.org/wiki/Economy_of_the_United_States', match='Inflation rate')[0]

        self.cat_cols, self.num_cols = self.check_variables(flag='data')
        buffer = io.StringIO()
        self.data.info(buf=buffer)
        self.info = buffer.getvalue()

    def cast_type(self, type_df):
        """
        Object, Integer, Float, DateTime
        """
        self.cast_data = self.data.copy()
        type_mapping = {
            np.dtype('object'): 'Object',
            np.dtype('int64'): 'Integer',
            np.dtype('float64'): 'Float'
        }
        dtypes = self.data.dtypes.map(type_mapping).tolist()
        columns = type_df['Columns'].values.tolist()
        types = type_df['Data Type'].values.tolist()
        for i, col in enumerate(columns):
            if dtypes[i] != types[i]:
                if dtypes[i] == 'Object' and types[i] in ['Integer', 'Float']:
                    # Object to number
                    self.cast_data[col] = self.cast_data[col] \
                                                .str.replace(',', '') \
                                                .str.replace('%', '') \
                                                .str.replace('$', '') \
                                                .str.replace(' ', '')
                    # 将 data[col] 转换为 Float 类型，同时处理空值
                    self.cast_data[col] = pd.to_numeric(self.cast_data[col], errors='coerce').astype(float)
                    
                elif dtypes[i] in ['Integer', 'Float'] and types[i] == 'Object':
                    # number to object
                    self.cast_data[col] = self.cast_data[col].astype(str)
                elif types[i] == 'DateTime':
                    if dtypes[i] in ['Integer', 'Float']:
                        # number to Datetime
                        self.cast_data[col] = pd.to_datetime(self.cast_data[col], errors='coerce')
                        pass
                    if dtypes[i] == 'Object':
                        # object to Datetime
                        # 将 data[col] 转换为 Datetime 类型
                        self.cast_data[col] = pd.to_datetime(self.cast_data[col], errors='coerce')
                        pass


    def check_variables(self, flag=None):
        if flag == 'data':
            data = self.data
        else:
            data = self.cast_data
        cols = data.columns
        quantitative_cols = data._get_numeric_data().columns
        categorical_cols = list(set(cols) - set(quantitative_cols))
        return categorical_cols, list(set(quantitative_cols))


    def categorical(self, flag=None):
        if flag == 'data':
            data = self.data
        else:
            data = self.cast_data
        figures = []
        cat_cols, num_cols = self.check_variables(flag)
        for col in cat_cols:
            # 创建一个图形和两个子图
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            # 在第一个子图（ax1）中绘制饼图
            data.groupby(col).size().plot(kind='pie', ax=ax1, ylabel=col, autopct='%.2f%%')
            ax1.set_title(f'{col} Pie Chart')
            # 在第二个子图（ax2）中绘制柱状图
            data.groupby(col).size().plot(kind='bar', ax=ax2, rot=0, colormap='Paired')
            ax2.set_title(f'{col} Bar Chart')
            # 调整布局以防止重叠
            plt.tight_layout()
            figures.append(fig)

        return figures

    def numerical(self, flag=None):
        if flag == 'data':
            data = self.data
        else:
            data = self.cast_data
        figures = []
        description_dicts = []
        cat_cols, num_cols = self.check_variables(flag)
        for col in num_cols:
            # description_dict = self.data[col].describe().to_dict()
            description_dict = data[col].describe().to_frame().T
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            sns.histplot(data=data, x=col, ax=ax1, kde=True, color='skyblue')
            sns.boxplot(data=data, y=col, ax=ax2)

            figures.append(fig)
            description_dicts.append(description_dict)
        
        return figures, description_dicts
    

    def corr_heatmap(self, flag=None):
        if flag == 'data':
            data = self.data
        else:
            data = self.cast_data
        fig = plt.figure()
        cat_cols, num_cols = self.check_variables(flag)
        sns.heatmap(data[num_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.title('Correlation Heatmap')
        return fig
    
    def missing_value(self, flag=None):
        if flag == 'data':
            data = self.data
        else:
            data = self.cast_data
        # 检查缺失值
        missing_data = data.isnull().sum()
        data_types = data.dtypes

        # 创建一个 DataFrame 来存储结果
        missing_info = pd.DataFrame({
            'Missing Values': missing_data,
            'Data Type': data_types
        })

        # 过滤出有缺失值的列
        missing_info = missing_info[missing_info['Missing Values'] > 0]

        return missing_info
    
    

    def data_fillna(self, flag=None):
        if flag == 'data':
            data = self.data
        else:
            data = self.cast_data

        pass

