import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import io


class Explorer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        # self.data = pd.read_html('https://en.wikipedia.org/wiki/Economy_of_the_United_States', match='Inflation rate')[0]

        self.cat_cols, self.num_cols = self.check_variables()
        buffer = io.StringIO()
        self.data.info(buf=buffer)
        self.info = buffer.getvalue()

    def check_variables(self):
        cols = self.data.columns
        quantitative_cols = self.data._get_numeric_data().columns
        categorical_cols = list(set(cols) - set(quantitative_cols))
        return categorical_cols, list(set(quantitative_cols))


    def categorical(self):
        figures = []
        for col in self.cat_cols:
            # 创建一个图形和两个子图
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            # 在第一个子图（ax1）中绘制饼图
            self.data.groupby(col).size().plot(kind='pie', ax=ax1, ylabel=col, autopct='%.2f%%')
            ax1.set_title(f'{col} Pie Chart')
            # 在第二个子图（ax2）中绘制柱状图
            self.data.groupby(col).size().plot(kind='bar', ax=ax2, rot=0, colormap='Paired')
            ax2.set_title(f'{col} Bar Chart')
            # 调整布局以防止重叠
            plt.tight_layout()
            figures.append(fig)

        return figures

    def numerical(self):
        figures = []
        description_dicts = []
        for col in self.num_cols:
            # description_dict = self.data[col].describe().to_dict()
            description_dict = self.data[col].describe().to_frame().T
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
            
            sns.histplot(data=self.data, x=col, ax=ax1, kde=True, color='skyblue')
            sns.boxplot(data=self.data, y=col, ax=ax2)

            figures.append(fig)
            description_dicts.append(description_dict)
        
        return figures, description_dicts
    

    def corr_heatmap(self):
        fig = plt.figure()
        sns.heatmap(self.data[self.num_cols].corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
        plt.title('Correlation Heatmap')
        return fig
    
    def missing_value(self):
        # 检查缺失值
        missing_data = self.data.isnull().sum()
        data_types = self.data.dtypes

        # 创建一个 DataFrame 来存储结果
        missing_info = pd.DataFrame({
            'Missing Values': missing_data,
            'Data Type': data_types
        })

        # 过滤出有缺失值的列
        missing_info = missing_info[missing_info['Missing Values'] > 0]

        return missing_info
