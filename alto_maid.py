import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime
import datetime
import altair as alt
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objs as go
import re
import seaborn as sns
import warnings
import calendar
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Alto_maid",
    layout = 'wide',
)
st.markdown('# AtMind Group')
st.title('Alto')


uploaded_files = st.file_uploader("Choose a excel file", type='xlsx', accept_multiple_files=True)
if uploaded_files:
    all= []
    all1 = []
    for uploaded_file in uploaded_files:
        try:
            for uploaded_file in uploaded_files:
                df = pd.read_excel(uploaded_file,sheet_name='amenity_records',skiprows=[0])
                df1 = pd.read_excel(uploaded_file,sheet_name='work_orders - work_order',skiprows=[0])
                all.append(df)
                all1.append(df1)
        except Exception as e:
            pass
    amen , perform00,resoures = st.tabs(['**Amenity**','**Performace**','**Resouces**'])
    with amen:
        if all:
            all = pd.concat(all)
            def perform(all) :
                all = all.fillna(0)
                all['time_stamp'] = pd.to_datetime(all['time_stamp'])
                all[['created_at','updated_at']] = all[['created_at','updated_at']].apply(pd.to_datetime)               
                all['time_of_day'] = pd.NA
                all.loc[all['time_stamp'].dt.hour >= 12, 'time_of_day'] = 'Afternoon'
                all.loc[all['time_stamp'].dt.hour < 12, 'time_of_day'] = 'Morning'
                all = all.rename(columns={'amenities_กาแฟ': 'complimentary_กาแฟ',
                            'amenities_น้ำตาล': 'complimentary_น้ำตาล',
                            'amenities_ครีมเทียม': 'complimentary_ครีมเทียม',
                            'amenities_ชา': 'complimentary_ชา'})
                all['Time'] = all['time_stamp'].dt.time
                all['Date'] = all['time_stamp'].dt.date
                all['Month'] = all['time_stamp'].dt.month
                desired_order = ['Date','Time','time_of_day','floor_name','room_name','complimentary_กาแฟ', 'complimentary_น้ำตาล', 'complimentary_ครีมเทียม',
                    'complimentary_ชา', 'amenities_แชมพู', 'amenities_สบู่ล้างมือ', 'amenities_ครีมอาบน้ำ',
                    'amenities_ชุดแปรงฟัน', 'amenities_หมวกคลุมผม', 'amenities_คัทเติ้ลบัช', 'amenities_น้ำดื่ม',
                    'amenities_กระดาษรองแก้ว', 'amenities_ถุงคลุมแก้ว', 'amenities_ดินสอ', 'amenities_สมุดดาษโน๊ต',
                    'amenities_ทิชชูเช็ดหน้า', 'amenities_ทิชชูม้วน', 'amenities_ถุงขยะดำ_18x20', 'linen_ผ้าปูเตียง',
                    'linen_ปลอกผ้าดูเว้', 'linen_ปลอกหมอน', 'linen_ผ้าเช็ดตัว', 'linen_ผ้าเช็ดมือ',
                    'linen_ผ้าเช็ดเท้า', 'linen_เสื้อคลุมอาบน้ำ']
                all = all.set_index('work_order_id')
                all = all.reindex(columns=desired_order)
                all['complimentary_sum'] = all.filter(like='complimentary_').sum(axis=1)
                all['amenities_sum'] = all.filter(like='amenities_').sum(axis=1)
                all['linen_sum'] = all.filter(like='linen_').sum(axis=1)
                return all

            all2 =  perform(all)

            #lis_t =['complimentary_กาแฟ', 'complimentary_น้ำตาล', 'complimentary_ครีมเทียม',
            #     'complimentary_ชา', 'amenities_แชมพู', 'amenities_สบู่ล้างมือ', 'amenities_ครีมอาบน้ำ',
            #     'amenities_ชุดแปรงฟัน', 'amenities_หมวกคลุมผม', 'amenities_คัทเติ้ลบัช', 'amenities_น้ำดื่ม',
            #     'amenities_กระดาษรองแก้ว', 'amenities_ถุงคลุมแก้ว', 'amenities_ดินสอ', 'amenities_สมุดดาษโน๊ต',
            #     'amenities_ทิชชูเช็ดหน้า', 'amenities_ทิชชูม้วน', 'amenities_ถุงขยะดำ_18x20', 'linen_ผ้าปูเตียง',
            #     'linen_ปลอกผ้าดูเว้', 'linen_ปลอกหมอน', 'linen_ผ้าเช็ดตัว', 'linen_ผ้าเช็ดมือ',
            #     'linen_ผ้าเช็ดเท้า', 'linen_เสื้อคลุมอาบน้ำ']
            month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
            col1,col2 = st.columns(2)
            with col1:
                    start_date = st.date_input('Select a start date', value=all2['Date'].min())
            with col2:
                    end_date = st.date_input('Select an end date', value=all2['Date'].max())
            all2 = all2[(all2['Date'] >= pd.Timestamp(start_date)) & (all2['Date'] <= pd.Timestamp(end_date))]
            col1 , col2 = st.columns([1,3])
            with col1 :
                    list1 = ['complimentary_sum', 'amenities_sum', 'linen_sum']
                    grouped_data = []
                    for column in list1:
                        grouped = all2.groupby(all2['floor_name'])[column].sum().reset_index(name='sum')
                        grouped['type'] = column.split('_')[0]
                        grouped_data.append(grouped)
                    concatenated_data = pd.concat(grouped_data)
                    fig = px.bar(concatenated_data, x='floor_name', y='sum', color='type', barmode='stack',text_auto=True)
                    fig.update_layout(title="Floor",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                    st.plotly_chart(fig,use_container_width=True)
            with col2 :
                    weekly,monthly,yearly = st.tabs(['**weekly**','**monthly**','**yearly**'])
                    with weekly:
                        ordered_day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

                        list1 = ['complimentary_sum', 'amenities_sum', 'linen_sum']
                        grouped_data = []
                        for column in list1:
                            all2['Date'] = pd.to_datetime(all2['Date'])
                            grouped = all2.groupby(all2['Date'].dt.day_name().astype(pd.CategoricalDtype(ordered_day_names)))[column].sum().reset_index(name='sum')
                            grouped['type'] = column.split('_')[0]
                            grouped_data.append(grouped)

                        concatenated_data = pd.concat(grouped_data)
                        fig = px.bar(concatenated_data, x='Date', y='sum', color='type', barmode='stack', text_auto=True)
                        fig.update_layout(
                            title="Sum of All Stock",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    with monthly:
                        list1 = ['complimentary_sum', 'amenities_sum', 'linen_sum']
                        grouped_data = []
                        for column in list1:
                            all2['Date'] = pd.to_datetime(all2['Date'])
                            grouped = all2.groupby(all2['Date'])[column].sum().reset_index(name='sum')
                            grouped['type'] = column.split('_')[0]
                            grouped_data.append(grouped)
                        concatenated_data = pd.concat(grouped_data)
                        fig = px.bar(concatenated_data, x='Date', y='sum', color='type', barmode='stack',text_auto=True)
                        fig.update_layout(title="Sum of All stock",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        st.plotly_chart(fig,use_container_width=True)
                    with yearly:
                        list1 = ['complimentary_sum', 'amenities_sum', 'linen_sum']
                        grouped_data = []
                        for column in list1:
                            all2['Date'] = pd.to_datetime(all2['Date'])
                            grouped = all2.groupby(all2['Date'].dt.month_name().astype(pd.CategoricalDtype(month_order)))[column].sum().reset_index(name='sum')
                            grouped['type'] = column.split('_')[0]
                            grouped_data.append(grouped)
                        concatenated_data = pd.concat(grouped_data)
                        fig = px.bar(concatenated_data, x='Date', y='sum', color='type', barmode='stack',text_auto=True)
                        fig.update_layout(title="Sum of All stock",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                        st.plotly_chart(fig,use_container_width=True)
            st.markdown('**CATEGORY**')
            c1,c2,c3 = st.columns(3)
            with c1:
                    lis_t0 =['complimentary_กาแฟ', 'complimentary_น้ำตาล', 'complimentary_ครีมเทียม',
                        'complimentary_ชา']
                    grouped_data = []
                    for column in lis_t0:
                        grouped = all2.groupby(all2['Date'])[column].sum().reset_index(name='counts')
                        grouped['type'] = column.split('_')[1]
                        grouped_data.append(grouped)
                    concatenated_data = pd.concat(grouped_data)
                    fig = px.bar(concatenated_data, x='Date', y='counts', color='type', barmode='stack',text_auto=True)
                    fig.update_layout(title="Complimentary",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                    st.plotly_chart(fig,use_container_width=True)
            with c2 :
                    lis_t000 =['amenities_แชมพู', 'amenities_สบู่ล้างมือ', 'amenities_ครีมอาบน้ำ',
                    'amenities_ชุดแปรงฟัน', 'amenities_หมวกคลุมผม', 'amenities_คัทเติ้ลบัช', 'amenities_น้ำดื่ม',
                    'amenities_กระดาษรองแก้ว', 'amenities_ถุงคลุมแก้ว', 'amenities_ดินสอ', 'amenities_สมุดดาษโน๊ต',
                    'amenities_ทิชชูเช็ดหน้า', 'amenities_ทิชชูม้วน', 'amenities_ถุงขยะดำ_18x20']
                    grouped_data = []
                    for column in lis_t000:
                        grouped = all2.groupby(all2['Date'])[column].sum().reset_index(name='counts')
                        grouped['type'] = column.split('_')[1]
                        grouped_data.append(grouped)
                    concatenated_data = pd.concat(grouped_data)
                    fig = px.bar(concatenated_data, x='Date', y='counts', color='type', barmode='stack',text_auto=True)
                    fig.update_layout(title='Amenities',legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                    st.plotly_chart(fig,use_container_width=True)
            with c3 :
                    lis_t00 =['linen_ผ้าปูเตียง',
                        'linen_ปลอกผ้าดูเว้', 'linen_ปลอกหมอน', 'linen_ผ้าเช็ดตัว', 'linen_ผ้าเช็ดมือ',
                        'linen_ผ้าเช็ดเท้า', 'linen_เสื้อคลุมอาบน้ำ']
                    grouped_data = []
                    for column in lis_t00:
                        grouped = all2.groupby(all2['Date'])[column].sum().reset_index(name='counts')
                        grouped['type'] = column.split('_')[1]
                        grouped_data.append(grouped)
                    concatenated_data = pd.concat(grouped_data)
                    fig = px.bar(concatenated_data, x='Date', y='counts', color='type', barmode='stack',text_auto=True)
                    fig.update_layout(title='Linen')
                    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
                    st.plotly_chart(fig,use_container_width=True)
    with perform00 :
        if all1:
            all1 = pd.concat(all1)
            assigned_by_id_mapping = {
                850.0: 'amberadmin',
                922.0: 'amberadmin',
                1067.0: 'สุภาพร	วรรณคำ',
                1069.0: 'อัญชลี	จันทลิด',
                1070.0: 'ญานี	ศรีบุระ',
                1071.0: 'ยุรนันท์	สุภาแสน',
                1073.0: 'อังสุมาริน	พรมนาง',
                1074.0: 'ศักดิ์ชัย	ประชุมเหล็ก',
                1075.0: 'เพ็ญศรี	เคลื่อนสูงเนิน',
                1076.0: 'นงค์เยาว์	อะเวลา',
                1077.0: 'Pichaya	Chulajarit',
                1078.0: 'Imsupitchaya	Akkharamahawong',
                1079.0: 'Sunipan	Paetha',
                1080.0: 'พรรณวรส	ปรัชญาภูมิ',
                1082.0: 'Imsupitchaya	Akkharamahawong',
                1084.0: 'อัมพร	บุญพรม',
                1085.0: 'อ้มพร	บุญพรม',
                1086.0: 'พิบูล	เสาสี',
                1090.0: 'Pame	Pame',
                1091.0: 'พิบูล	เสาสี',
                1108.0: 'Pichaya	Chulajajrit',
                1131.0: 'Pichaya	HM',
                1185.0: 'Sivapong	Meesang',
                1186.0: 'บัวลื่น	ขันธ์ุเงิน',
                1194.0: 'สุกัญญา	พุฒทรง',
                1195.0: 'ศิริรัตน์	เกิดสวัสดิ์',
                1196.0: 'เชาวลิต	บ่ายกระโทก',
                1198.0: 'SuperUserTest'
            }
            assigned_by_id_values = [850.0,922.0, 1067.0, 1069.0, 1070.0, 1071.0, 1073.0, 1074.0, 1075.0, 1076.0, 1077.0, 1078.0, 1079.0, 1080.0, 1082.0, 1084.0, 1085.0, 1086.0, 1090.0, 1091.0, 1108.0, 1131.0, 1185.0, 1186.0, 1194.0, 1195.0, 1196.0, 1198.0]

            assigned_by_id_mapped = [assigned_by_id_mapping.get(value, value) for value in assigned_by_id_values]

            assigned_by_id_mapping1 = { 850: "Owner",
                922: "Owner",
                1: "Super User",
                924: "Guest",
                926: "Guest",
                1067: "Maid",
                1069: "Maid",
                1070: "Maid",
                1071: "Maid",
                1073: "Maid",
                1074: "Maid",
                1075: "Maid",
                1076: "Maid",
                1077: "Supervisor",
                1078: "Maid",
                1079: "Maid",
                1080: "Maid",
                1082: "Supervisor",
                1084: "Supervisor",
                1085: "Maid",
                1086: "Maid",
                1090: "Maid",
                1091: "Supervisor",
                1108: "Maid",
                1131: "Owner",
                1185: "Maid",
                1186: "Maid",
                1194: "Maid",
                1195: "Maid",
                1196: "Maid",
                1198: "Super User"}
            assigned_by_id_values = [850.0,922.0, 1067.0, 1069.0, 1070.0, 1071.0, 1073.0, 1074.0, 1075.0, 1076.0, 1077.0, 1078.0, 1079.0, 1080.0, 1082.0, 1084.0, 1085.0, 1086.0, 1090.0, 1091.0, 1108.0, 1131.0, 1185.0, 1186.0, 1194.0, 1195.0, 1196.0, 1198.0]

            assigned_by_id_mapped1 = [assigned_by_id_mapping1.get(value, value) for value in assigned_by_id_values]

            def determine_worktype(title):
                if "Touch Up" in title:
                    return "Touch Up", title.split()[-1]
                elif "ทำความสะอาด" in title:
                    return "Cleaning", title.split()[0]
                else:
                    return "Workorder", title
            
            def timetaken(row):
                    if pd.notna(row['continue_at']) and pd.notna(row['pause_at']):
                        if pd.notna(row['cleaning_finished_at']):
                            return (row['cleaning_finished_at'] - (row['continue_at'] - row['pause_at']) - row['started_at']).total_seconds()/60
                        elif pd.notna(row['end_at']):
                            return (row['end_at'] - (row['continue_at'] - row['pause_at']) - row['started_at']).total_seconds()/60
                    elif pd.notna(row['cleaning_finished_at']):
                        return (row['cleaning_finished_at'] - row['started_at']).total_seconds()/60
                    elif pd.notna(row['end_at']):
                        return (row['end_at'] - row['started_at']).total_seconds()/60
                    else:
                        return np.nan
                
            def perform1(all1):
                all1 = all1[['id','assigned_by_id','assigned_to_id','created_by_id','status','report_urgent','title','description','room_id','cleaning_type','started_at','end_at','cleaning_finished_at','continue_at','pause_at','report_type_id']]
                all1[['started_at','end_at','cleaning_finished_at','pause_at','continue_at']] = all1[['started_at','end_at','cleaning_finished_at','pause_at','continue_at']].apply(pd.to_datetime)
                all1['role_created_by'] = all1['created_by_id'].map(assigned_by_id_mapping1)
                all1['role_assigned_by'] = all1['assigned_by_id'].map(assigned_by_id_mapping1)
                all1['role_assigned_to'] = all1['assigned_to_id'].map(assigned_by_id_mapping1)
                all1['assigned_by'] = all1['assigned_by_id'].map(assigned_by_id_mapping)
                all1['assigned_to'] = all1['assigned_to_id'].map(assigned_by_id_mapping)
                all1['created_by'] = all1['created_by_id'].map(assigned_by_id_mapping)
                all1[['assigned_by_id', 'assigned_to_id', 'created_by_id']] = all1[['assigned_by_id', 'assigned_to_id', 'created_by_id']].astype(str).applymap(lambda x: x.replace('\t', ' '))
                all1['worktype'], all1['workdes'] = zip(*all1['title'].apply(lambda x: determine_worktype(x)))
                all1['cleaning_finished_at'] = all1['cleaning_finished_at'].fillna(np.nan)
                all1['timetaken'] = all1.apply(timetaken, axis=1)
                all1 = all1[['id','worktype','workdes','cleaning_type','status','report_urgent','assigned_by','role_assigned_by','assigned_to','role_assigned_to','created_by','role_created_by','timetaken','started_at','pause_at','continue_at','cleaning_finished_at','end_at','report_type_id']]
                all1= all1[all1['timetaken'] > 0]
                all1[['id','report_type_id']] = all1[['id','report_type_id']].astype(str)
                return all1

            all3 =  perform1(all1)
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input('Select a start date', value=pd.to_datetime(all3['started_at'].min()).date())
            with col2:
                end_date = st.date_input('Select an end date', value=pd.to_datetime(all3['started_at'].max()).date())

            start_timestamp = pd.Timestamp(start_date, tz='UTC')
            end_timestamp = pd.Timestamp(end_date, tz='UTC')

            all3 = all3[(all3['started_at'] >= start_timestamp) & (all3['started_at'] <= end_timestamp)]
            st.write(all3)

            total_t,co,od,vc = st.tabs(['**All type**','**C/O**','**OD**','**VC**'])
            with total_t:
                all3_c =all3.copy()
                all3_c['percentile'] = all3_c['timetaken'].rank(pct=True)
                min_val, max_val = float(all3_c['percentile'].min()), float(all3_c['percentile'].max())
                tk_min, tk_max = st.slider('Select a range of Q', min_val, max_val, (min_val, max_val))
                all3_c = all3_c[(all3_c['percentile'] >= tk_min) & (all3_c['percentile'] <= tk_max)]
                fig = px.box(all3_c, x="timetaken", points="all", hover_data=all3_c.columns)
                fig.update_layout(xaxis_title="Cleaning Type", yaxis_title="Time Taken")
                st.plotly_chart(fig, use_container_width=True)
                c1, c2, c3 = st.columns([1, 1.5, 1])
                c2.write(all3_c[['timetaken']].describe().T, use_container_width=True)
            with co:
                co_df = all3.copy()
                co_df = co_df[co_df["cleaning_type"] == "C/O"]
                co_df['percentile'] = co_df['timetaken'].rank(pct=True)
                min_val, max_val = float(co_df['percentile'].min()), float(co_df['percentile'].max())
                tk_min, tk_max = st.slider('Select a range of Q', min_val, max_val, (min_val, max_val))
                co_df = co_df[(co_df['percentile'] >= tk_min) & (co_df['percentile'] <= tk_max)]
                fig = px.box(co_df, x="timetaken", points="all", hover_data=co_df.columns)
                fig.update_layout(xaxis_title="Cleaning Type", yaxis_title="Time Taken")
                st.plotly_chart(fig, use_container_width=True)
                grouped = co_df.groupby(co_df['started_at'].dt.date).size().reset_index(name='count')
                fig = px.bar(grouped, x='started_at', y='count', text_auto=True)
                grouped1 = co_df.groupby(co_df['assigned_to']).size().reset_index(name='count')
                grouped1 = grouped1.sort_values('count', ascending=False)
                fig1 = px.bar(grouped1, x='assigned_to', y='count',color='assigned_to')
                col1,col2 = st.columns(2)
                col1.plotly_chart(fig1, use_container_width=True)
                col2.plotly_chart(fig, use_container_width=True)
                c11,c22,c33 = st.columns([1,1.5,1])
                c22.write((co_df[['timetaken']].describe().T),use_container_width=True)
            with od:
                od_df = all3.copy()
                od_df = od_df[od_df["cleaning_type"] == "OD"]
                od_df['percentile'] = od_df['timetaken'].rank(pct=True)
                min_val, max_val = float(od_df['percentile'].min()), float(od_df['percentile'].max())
                tk_min, tk_max = st.slider('Select a range of Q', min_val, max_val, (min_val, max_val))
                od_df = od_df[(od_df['percentile'] >= tk_min) & (od_df['percentile'] <= tk_max)]
                fig = px.box(od_df, x="timetaken", points="all", hover_data=od_df.columns)
                fig.update_layout(xaxis_title="Cleaning Type", yaxis_title="Time Taken")
                st.plotly_chart(fig, use_container_width=True)
                grouped = od_df.groupby(od_df['started_at'].dt.date).size().reset_index(name='count')
                fig = px.bar(grouped, x='started_at', y='count', text_auto=True)
                grouped1 = od_df.groupby(od_df['assigned_to']).size().reset_index(name='count')
                grouped1 = grouped1.sort_values('count', ascending=False)
                fig1 = px.bar(grouped1, x='assigned_to', y='count',color='assigned_to')
                col1,col2 = st.columns(2)
                col1.plotly_chart(fig1, use_container_width=True)
                col2.plotly_chart(fig, use_container_width=True)
                c11,c22,c33 = st.columns([1,1.5,1])
                c22.write((od_df[['timetaken']].describe().T),use_container_width=True)
            with vc:
                vc_df = all3.copy()
                vc_df = vc_df[vc_df["cleaning_type"] == "VC"]
                vc_df['percentile'] = vc_df['timetaken'].rank(pct=True)
                min_val, max_val = float(vc_df['percentile'].min()), float(vc_df['percentile'].max())
                tk_min, tk_max = st.slider('Select a range of Q', min_val, max_val, (min_val, max_val))
                vc_df = vc_df[(vc_df['percentile'] >= tk_min) & (vc_df['percentile'] <= tk_max)]
                fig = px.box(vc_df, x="timetaken", points="all", hover_data=vc_df.columns)
                fig.update_layout(xaxis_title="Cleaning Type", yaxis_title="Time Taken")
                st.plotly_chart(fig, use_container_width=True)
                grouped = vc_df.groupby(vc_df['started_at'].dt.date).size().reset_index(name='count')
                fig = px.bar(grouped, x='started_at', y='count', text_auto=True)
                grouped1 = vc_df.groupby(vc_df['assigned_to']).size().reset_index(name='count')
                grouped1 = grouped1.sort_values('count', ascending=False)
                fig1 = px.bar(grouped1, x='assigned_to', y='count',color='assigned_to')
                col1,col2 = st.columns(2)
                col1.plotly_chart(fig1, use_container_width=True)
                col2.plotly_chart(fig, use_container_width=True)
                c111,c222,c333 = st.columns([1,1.5,1])
                c222.write((vc_df[['timetaken']].describe().T),use_container_width=True)

            wk,my,yy = st.tabs(['**weekly**','**monthly**','**yearly**'])
            with wk:
                cl,cl1,cl2 = st.columns(3)
                with cl:
                    grouped1 = co_df.groupby(co_df['started_at'].dt.day_name().astype(pd.CategoricalDtype(ordered_day_names)))['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped1, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="C/O")
                    #max = grouped1['mean'].max()
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)
                with cl1 :
                    grouped = od_df.groupby(od_df['started_at'].dt.day_name().astype(pd.CategoricalDtype(ordered_day_names)))['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="OD")
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)
                with cl2:
                    grouped = vc_df.groupby(vc_df['started_at'].dt.day_name().astype(pd.CategoricalDtype(ordered_day_names)))['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="VC")
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)
            with my:
                cl,cl1,cl2 = st.columns(3)
                with cl:
                    grouped11 = co_df.groupby(co_df['started_at'].dt.date)['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped11, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="C/O")
                    #max = grouped11['mean'].max()
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)

                with cl1 :
                    grouped = od_df.groupby(od_df['started_at'].dt.date)['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="OD")
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)

                with cl2:
                    grouped = vc_df.groupby(vc_df['started_at'].dt.date)['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="VC")
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)
            with yy:
                cl,cl1,cl2 = st.columns(3)
                with cl:
                    grouped111 = co_df.groupby(co_df['started_at'].dt.month_name().astype(pd.CategoricalDtype(month_order)))['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped111, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="C/O")
                    #max = grouped111['mean'].max()
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)

                with cl1 :
                    grouped = od_df.groupby(od_df['started_at'].dt.month_name().astype(pd.CategoricalDtype(month_order)))['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="OD")
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)

                with cl2:
                    grouped = vc_df.groupby(vc_df['started_at'].dt.month_name().astype(pd.CategoricalDtype(month_order)))['timetaken'].mean().reset_index(name='mean')
                    fig = px.bar(grouped, x='started_at', y='mean', text_auto=True)
                    fig.update_layout(title="VC")
                    #fig.update_yaxes(range=[0, max+1])
                    st.plotly_chart(fig, use_container_width=True)
            worktype_cl = perform1(all1)
            worktype_cl = worktype_cl[worktype_cl["worktype"] == "Cleaning"]
            grouped = worktype_cl.groupby(worktype_cl['started_at'].dt.date)['status'].value_counts(normalize=True).mul(100).reset_index(name='percent')

            fig = px.bar(grouped, x='started_at', y='percent', color='status', barmode='stack', text='percent')
            fig.update_traces(texttemplate='%{text:.1f}%')
            fig.update_layout(title="Inspect Ratio",legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1))
            fig.update_layout(yaxis=dict(tickformat=".0f"))

            st.plotly_chart(fig, use_container_width=True)
    with resoures:
        resoures_df = perform1(all1)
        col1,col2 = st.columns(2)
        with col1:
                    start_date = st.date_input('Select a start date  ', value=resoures_df['started_at'].min())
        with col2:
                    end_date = st.date_input('Select an end date   ', value=resoures_df['started_at'].max())
        start_timestamp = pd.Timestamp(start_date, tz='UTC')
        end_timestamp = pd.Timestamp(end_date, tz='UTC')
        resoures_df = resoures_df[(resoures_df['started_at'] >= start_timestamp) & (resoures_df['started_at'] <= end_timestamp)]
        resoures_df = resoures_df[resoures_df["cleaning_type"] != "DND"]
        www,mmm,yyy = st.tabs(['**weekly**','**monthly**','**yearly**'])
        with mmm:
            grouped = resoures_df.groupby([resoures_df['started_at'].dt.date,resoures_df['assigned_to']])['timetaken'].mean().reset_index(name='mean')
            fig = px.area(grouped, x='started_at', y='mean',color='assigned_to')
            fig.update_traces(mode='none')
            st.plotly_chart(fig, use_container_width=True)
        with www:
            grouped = resoures_df.groupby([resoures_df['started_at'].dt.day_name().astype(pd.CategoricalDtype(ordered_day_names)),resoures_df['assigned_to']])['timetaken'].mean().reset_index(name='mean')
            fig = px.area(grouped, x='started_at', y='mean',color='assigned_to')
            fig.update_traces(mode='none')
            st.plotly_chart(fig, use_container_width=True)
        with yyy :
            grouped = resoures_df.groupby([resoures_df['started_at'].dt.month_name().astype(pd.CategoricalDtype(month_order)),resoures_df['assigned_to']])['timetaken'].mean().reset_index(name='mean')
            fig = px.area(grouped, x='started_at', y='mean',color='assigned_to')
            fig.update_traces(mode='none')
            st.plotly_chart(fig, use_container_width=True)
        ccc1,ccc2 = st.columns(2)
        with ccc1:
            grouped = resoures_df.groupby(resoures_df['assigned_to'])['timetaken'].sum().reset_index(name='sum timetaken(min)')
            grouped = grouped.sort_values('sum timetaken(min)', ascending=False)
            fig = px.bar(grouped, x='assigned_to', y='sum timetaken(min)',color='assigned_to')
            st.plotly_chart(fig, use_container_width=True)
        with ccc2:
            grouped = pd.crosstab(resoures_df['assigned_to'], resoures_df['cleaning_type'])
            grouped = grouped.stack().reset_index(name='sum cleaning type')
            grouped = grouped.sort_values('sum cleaning type', ascending=False)

            fig = px.bar(grouped, x='assigned_to', y='sum cleaning type', color='cleaning_type')
            st.plotly_chart(fig, use_container_width=True)
             

else:
    st.markdown("**No file uploaded.**")
