import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import pandas as pd
import plotly.express as px

st.set_page_config(layout = "wide")

def display(data):
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
#     gb.configure_auto_height(autoHeight = False)
    gb.configure_default_column(min_column_width=10,other_default_column_properties={"wrapText":True, "autoHeight":True})
    gb.configure_side_bar() #Add a sidebar
#     gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
    gridOptions = gb.build()

    grid_response = AgGrid(
        data,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT',
        update_mode='MODEL_CHANGED',
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=True,
        height=700,
        width='100%',
        reload_data=True
    )


def visualize(total_df_melt, dt):
    if dt == "全部":
        fig = px.line(total_df_melt,
            x="日期",
            y="value",
            color="URL",
            markers=True,
            category_orders={'Type':['text','img']},
            line_dash='Type',
            custom_data=['Username', 'Date', 'Headline', 'index'])
    else:
        fig = px.line(total_df_melt[total_df_melt.Date==dt],
            x="日期",
            y="value",
            color="URL",
            markers=True,
            category_orders={'Type':['text','img']},
            line_dash='Type',
            custom_data=['Username', 'Date', 'Headline', 'index'])
    fig.update_layout(
        width=1000,
        height=700,
        showlegend=False
    )
    fig.update_traces(
        hovertemplate="<br>".join([
            "ID: %{customdata[3]}",
            "标题: %{customdata[2]}",
            "作者: %{customdata[0]}",
            "发表日期: %{customdata[1]}",
            "热度: %{y}"
        ])
    )


st.header("一周热度增长（6月20日至6月26日）")
page = st.sidebar.selectbox('选择CP',['GGAD','ADGG'])
if page == 'GGAD':
    total_df= pd.read_csv('total_df_ggad.csv', index_col=0)
    total_df_melt = total_df.melt(id_vars=['URL','Headline', 'Type', 'Username', 'User URL','Date','index'],var_name=['日期']).sort_values('Headline')
    clist = list(total_df['Date'].unique())+["全部"]
    dt = st.selectbox('选择发表日期', clist)
    display(total_df)
    visualize(total_df_melt, dt)
else:
    pass

