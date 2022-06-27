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
            x="记录日期",
            y="value",
            color="URL",
            markers=True,
            category_orders={'Type':['text','img']},
            line_dash='Type',
            custom_data=['Username', 'Date', 'Headline', 'index'])
    else:
        fig = px.line(total_df_melt[total_df_melt.Date==dt],
            x="记录日期",
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
    st.plotly_chart(fig)


st.header("一周热度增长（6月20日至6月26日）")
page = st.sidebar.selectbox('选择CP',['GGAD','ADGG'])
if page == 'GGAD':
    total_df = pd.read_csv('total_df_ggad.csv', index_col=0)
    total_df = total_df[['index', 'Headline', 'Type', 'Username', 'URL', 'User URL', 'Date', '2022-06-20',
       '2022-06-21', '2022-06-22', '2022-06-23', '2022-06-24', '2022-06-25',
       '2022-06-26', 'total_change', 'change1', 'change2', 'change3', 'change4',
       'change5', 'change6']]
    total_df_melt = total_df.iloc[:,:-7].melt(id_vars=['index','URL','Headline', 'Type', 'Username', 'User URL','Date'],var_name=['记录日期']).sort_values('Headline')
    total_df_melt['记录日期'] = pd.to_datetime(total_df_melt['记录日期'])
    total_df_melt.sort_values(['value','记录日期'], ascending=False, inplace=True)
    clist = ["全部"]+list(total_df['Date'].unique())
    dt = st.selectbox('选择发表日期', clist)
    status = st.radio ("筛选", ("全部","仅文字","仅图片"))
    if status == '全部':
        if dt == "全部":
            display(total_df)
        else:
            display(total_df[total_df.Date==dt])
    elif status == '仅文字':
        if dt == "全部":
            display(total_df[total_df.Type=='text'])
        else:
            display(total_df[(total_df.Date==dt)&(total_df.Type=='text')])
    else:
        if dt == "全部":
            display(total_df[total_df.Type=='img'])
        else:
            display(total_df[(total_df.Date==dt)&(total_df.Type=='img')])
    if status == '全部':
        visualize(total_df_melt, dt)
    elif status == '仅文字':
        visualize(total_df_melt[total_df_melt.Type=='text'], dt)
    else:
        visualize(total_df_melt[total_df_melt.Type=='img'], dt)
    
    comment_df = pd.read_csv('comment_df_ggad.csv', index_col=0)
    comment_df = comment_df[['index', 'Headline', 'Type', 'Username', 'URL', 'User URL', 'Date', '2022-06-20',
       '2022-06-21', '2022-06-22', '2022-06-23', '2022-06-24', '2022-06-25',
       '2022-06-26', 'total_change', 'change1', 'change2', 'change3', 'change4',
       'change5', 'change6']]
    comment_df_melt = comment_df.iloc[:,:-7].melt(id_vars=['index','URL','Headline', 'Type', 'Username', 'User URL','Date'],var_name=['记录日期']).sort_values('Headline')
    comment_df_melt['记录日期'] = pd.to_datetime(comment_df_melt['记录日期'])
    comment_df_melt.sort_values(['value','记录日期'], ascending=False, inplace=True)
    if status == '全部':
        if dt == "全部":
            display(comment_df)
        else:
            display(comment_df[comment_df.Date==dt])
    elif status == '仅文字':
        if dt == "全部":
            display(comment_df[comment_df.Type=='text'])
        else:
            display(comment_df[(comment_df.Date==dt)&(comment_df.Type=='text')])
    else:
        if dt == "全部":
            display(comment_df[comment_df.Type=='img'])
        else:
            display(comment_df[(comment_df.Date==dt)&(comment_df.Type=='img')])
    if status == '全部':
        visualize(comment_df_melt, dt)
    elif status == '仅文字':
        visualize(comment_df_melt[comment_df_melt.Type=='text'], dt)
    else:
        visualize(comment_df_melt[comment_df_melt.Type=='img'], dt)
else:
    total_df = pd.read_csv('total_df_adgg.csv', index_col=0)
    total_df = total_df[['index', 'Headline', 'Type', 'Username', 'URL', 'User URL', 'Date', '2022-06-20',
       '2022-06-21', '2022-06-22', '2022-06-23', '2022-06-24', '2022-06-25',
       '2022-06-26', 'total_change', 'change1', 'change2', 'change3', 'change4',
       'change5', 'change6']]
    total_df_melt = total_df.iloc[:,:-7].melt(id_vars=['index','URL','Headline', 'Type', 'Username', 'User URL','Date'],var_name=['记录日期']).sort_values('Headline')
    total_df_melt['记录日期'] = pd.to_datetime(total_df_melt['记录日期'])
    total_df_melt.sort_values(['value','记录日期'], ascending=False, inplace=True)
    clist = ["全部"]+list(total_df['Date'].unique())
    dt = st.selectbox('选择发表日期', clist)
    status = st.radio ("筛选", ("全部","仅文字","仅图片"))
    if status == '全部':
        if dt == "全部":
            display(total_df)
        else:
            display(total_df[total_df.Date==dt])
    elif status == '仅文字':
        if dt == "全部":
            display(total_df[total_df.Type=='text'])
        else:
            display(total_df[(total_df.Date==dt)&(total_df.Type=='text')])
    else:
        if dt == "全部":
            display(total_df[total_df.Type=='img'])
        else:
            display(total_df[(total_df.Date==dt)&(total_df.Type=='img')])
    if status == '全部':
        visualize(total_df_melt, dt)
    elif status == '仅文字':
        visualize(total_df_melt[total_df_melt.Type=='text'], dt)
    else:
        visualize(total_df_melt[total_df_melt.Type=='img'], dt)
    
    comment_df = pd.read_csv('comment_df_adgg.csv', index_col=0)
    comment_df = comment_df[['index', 'Headline', 'Type', 'Username', 'URL', 'User URL', 'Date', '2022-06-20',
       '2022-06-21', '2022-06-22', '2022-06-23', '2022-06-24', '2022-06-25',
       '2022-06-26', 'total_change', 'change1', 'change2', 'change3', 'change4',
       'change5', 'change6']]
    comment_df_melt = comment_df.iloc[:,:-7].melt(id_vars=['index','URL','Headline', 'Type', 'Username', 'User URL','Date'],var_name=['记录日期']).sort_values('Headline')
    comment_df_melt['记录日期'] = pd.to_datetime(comment_df_melt['记录日期'])
    comment_df_melt.sort_values(['value','记录日期'], ascending=False, inplace=True)
    if status == '全部':
        if dt == "全部":
            display(comment_df)
        else:
            display(comment_df[comment_df.Date==dt])
    elif status == '仅文字':
        if dt == "全部":
            display(comment_df[comment_df.Type=='text'])
        else:
            display(comment_df[(comment_df.Date==dt)&(comment_df.Type=='text')])
    else:
        if dt == "全部":
            display(comment_df[comment_df.Type=='img'])
        else:
            display(comment_df[(comment_df.Date==dt)&(comment_df.Type=='img')])
    if status == '全部':
        visualize(comment_df_melt, dt)
    elif status == '仅文字':
        visualize(comment_df_melt[comment_df_melt.Type=='text'], dt)
    else:
        visualize(comment_df_melt[comment_df_melt.Type=='img'], dt)

