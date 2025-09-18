# 北京房价数据分析与爬虫

该项目包含一组用于爬取安居客网站上北京市新房和二手房房源数据，并进行数据清洗、分析与可视化的脚本。

## 项目文件说明

*   `bug_houseprice.py`: 用于爬取**安居客北京新房房源**数据的Scrapy爬虫程序。
*   `bug_sec-hand_house.py`: 用于爬取**安居客北京二手房房源**数据的Scrapy爬虫程序。
*   `python_analysis.ipynb`: Jupyter Notebook文件，用于处理和分析爬取到的房源数据，并进行可视化展示。

## 功能概述

1.  **数据爬取 (`bug_houseprice.py` 和 `bug_sec-hand_house.py`)**
    *   从安居客网站抓取北京新房和二手房的基本信息，如标题、价格、面积、户型、所在区域等。
    *   将爬取的数据保存为结构化文件（如CSV），以供后续分析使用。

2.  **数据分析与可视化 (`python_analysis.ipynb`)**
    *   **数据清洗**: 处理缺失值、重复值和异常值。
    *   **数据分析**: 对房源价格、分布、户型等维度进行统计分析。
    *   **数据可视化**: 利用Matplotlib, Seaborn等库生成图表，如价格分布直方图、区域均价柱状图、热力图等，直观展示北京房地产市场情况。

## 使用方法

### 1. 环境依赖

请确保您的Python环境中安装了以下库：
*   Scrapy
*   Pandas
*   Jupyter Notebook
*   Matplotlib
*   Seaborn

您可以使用以下命令安装所有依赖：
```bash
pip install scrapy pandas jupyter matplotlib seaborn
```

### 2. 运行爬虫

新房爬虫:
```bash
scrapy runspider bug_houseprice.py -o new_houses.csv
```

二手房爬虫:
```bash
scrapy runspider bug_sec-hand_house.py -o second_hand_houses.csv
```

### 3. 运行分析 Notebook

启动Jupyter Notebook服务器：
```bash
jupyter notebook
```

在浏览器中打开生成的链接，然后点击 python_analysis.ipynb 文件。

在Notebook中，逐个运行代码单元以执行数据分析和生成可视化图表。请确保已正确生成爬虫数据文件，并在Notebook中指定正确的文件路径。

## 免责声明

*   本项目仅用于学习和研究目的，请勿用于商业用途或非法用途。

*   爬虫程序应遵守目标网站robots.txt协议的规定，并合理控制请求频率，避免对目标网站服务器造成过大压力。

*   房源数据来源于公开网络，数据的准确性和时效性仅供参考。
