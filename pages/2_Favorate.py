import streamlit as st
# import base64
# import json
import pygsheets
import extra_streamlit_components as stx
import requests
import pandas as pd
import io
import pygsheets
import math
import datetime

gc = pygsheets.authorize(service_account_file='led-sheet-47e8afe294c8.json')
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/16dO1zkakREjZxbjB6XFGijHFjjOUDYNpjwoeuUW5gP8/edit?usp=sharing')
worksheet = spreadsheet.sheet1

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'
# st.session_state.sidebar_state = 'expanded'
try:
    st.set_page_config(layout="wide",initial_sidebar_state=st.session_state.sidebar_state)
except:
    pass
def decimal_to_dms(decimal_degrees):
    degrees = int(decimal_degrees)
    decimal_minutes = (decimal_degrees - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = (decimal_minutes - minutes) * 60

    return degrees, minutes, seconds

def format_coordinates(latitude, longitude):
    latitude_dms = decimal_to_dms(latitude)
    longitude_dms = decimal_to_dms(longitude)
    
    latitude_str = f"{latitude_dms[0]}°{latitude_dms[1]}'{latitude_dms[2]:.1f}\"N"
    longitude_str = f"{longitude_dms[0]}°{longitude_dms[1]}'{longitude_dms[2]:.1f}\"E"

    return latitude_str + '+' + longitude_str

def update_sheet(user_id,province,link,sta):
    df = worksheet.get_as_df()
    # result = df.isin([user_id,province,link]).all(axis=1)
    # print(df)
    condition1 = df['user_id'] == user_id
    condition2 = df['province'] == province
    condition3 = df['link'] == link
    df_f = df[condition1 & condition2 & condition3]
    index = list(df_f.index)

    if index:
        print('data exist')
        worksheet.update_value(f'A{index[0]+2}', user_id)
        worksheet.update_value(f'B{index[0]+2}', province)
        worksheet.update_value(f'C{index[0]+2}', sta)
        worksheet.update_value(f'D{index[0]+2}', link)
        
    else:
        print('data not exist')
        cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)

        cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
        last_row = len(cells)
        # print(last_row)
        worksheet.update_value(f'A{last_row+1}', user_id)
        worksheet.update_value(f'B{last_row+1}', province)
        worksheet.update_value(f'C{last_row+1}', sta)
        worksheet.update_value(f'D{last_row+1}', link)

def create_list(df,n_total,p):
 
    for index, row in df.iterrows():
    #     if index ==10:
    #         break
    # for i in range(10):
        COL = st.columns(3)
        # st.divider()
        with COL[0]:
            st.subheader(f":green[{index+1}/{n_total}[{row['sell_order']}]{row['type']}]")

            if not math.isnan(row['lat']):
                decimal_coordinates = (row['lat'], row['lon'])
                print('decimal_coordinates',decimal_coordinates)
                formatted_coordinates = format_coordinates(*decimal_coordinates)
                url = f"https://www.google.com/maps/place/{formatted_coordinates}/@{row['lat']},{row['lon']},17z"
                st.markdown(f"*[{row['tumbon']},{row['aumper']},{row['province']}]({url})*")
            else:
                st.markdown(f"*{row['tumbon']},{row['aumper']},{row['province']}*")

            # st.markdown(f'[Map]({url})')
            
            
            

            area = ''
            a = ['ตร.ว.','งาน','ไร่']
            for i in range(2, -1, -1):
                if isinstance(row[f'size{i}'], int) or isinstance(row[f'size{i}'], float):
                    if row[f'size{i}'] != 0:
                        area += f"{row[f'size{i}']} {a[i]} "
            area = area[:-1]
            st.markdown(f"**:triangular_ruler: {area}**")
            st.markdown(f"วางเงิน {row['pay_down']:,.0f} บาท")
            

            # st.markdown(f"{row['max_price']:,.0f} {row['current_price']:,.0f}")
            try:
                date_object = datetime.strptime(str(int(row['lastSta_date'])), "%Y%m%d")
                formatted_date = date_object.strftime("%d/%m/%y")
            except:
                formatted_date = row['lastSta_date']
            try:
                st.markdown(f":orange[นัด {int(row['bid_time'])} {formatted_date} {row['lastSta_detail']}]")
            except:
                st.markdown(f":orange[นัด -]")

            st.markdown(f":red[{row['status']}]")

            st.subheader(f"[:moneybag: :blue[{row['max_price']:,.0f}]]({row['link']})")

            
            if st.button(f"Delete Favorate",key=f"{p}{index}"):
                st.write('delete favorate complete')
                update_sheet(person_id,p,row['link'],0)
     
            

            

            
            # st.subheader(':green[ที่ดินพร้อมสิ่งปลูกสร้าง]')
            # st.markdown("*บางกรวย,นนทบุรี*")
            # st.markdown("**2 ไร่ 1 งาน 2 ตร.ว.**")
            # st.subheader(":blue[123,456]")
            # st.markdown("****:red[นัด 1 ปลอดการจำนอง]****")
            



            
            # st.markdown("*Streamlit* is **really** ****cool****.")
            # st.text('บางกรวย,นนทบุรี')
            # st.title('This is a title')
            # st.header('This is a header with a divider')
            # st.subheader('_Streamlit_ is :blue[cool] :sunglasses:')
            # st.divider()
            # st.caption('A caption with _italics_ :blue[colors] and emojis :sunglasses:')
            # st.text('This is some text.')
            # hc.info_card(title='Some heading GOOD', content='All good!\n\ndvdvd sd sd sd xzcxynfgdsdcvsrfxgdc edzsbzd', sentiment='good',bar_value=77)

        with COL[1]:
            # st.image("https://www.meridianhomes.net.au/wp-content/uploads/2018/01/Meridian-Homes_Double-Story_Cadence-2-1.jpg", caption=f'{i}Sunrise by the mountains',use_column_width='auto')
            # st.image(row['img0'], caption=f'{i}Sunrise by the mountains',use_column_width='auto')
            st.image(row['img0'],use_column_width='auto')
        
            # if st.button(f'Map{index}'):
            # url = "https://www.google.com/maps/place/13%C2%B054'23.3%22N+101%C2%B010'17.6%22E/@13.9064682,101.1689661,17z"

            # if row['lat']:
            # if not math.isnan(row['lat']):
            #     decimal_coordinates = (row['lat'], row['lon'])
            #     print('decimal_coordinates',decimal_coordinates)
            #     formatted_coordinates = format_coordinates(*decimal_coordinates)


                # url = f"https://www.google.com/maps/place/{formatted_coordinates}/@{row['lat']},{row['lon']},17z"
                # st.markdown(f'[Map]({url})')
            # else:
            #     st.markdown(f'No map')

        with COL[2]:
            

            try:
                st.image(row['img1'],use_column_width='auto')
            except:
                pass
                # webbrowser.open_new_tab(url)

            # st.button('Open link', on_click=open_page("https://www.google.com/maps/place/13%C2%B054'23.3%22N+101%C2%B010'17.6%22E/@13.9064682,101.1689661,17z"))
            # if st.button(f'show map{index}'):
                

                # print("row['lat']",row['lat'],type(row['lat']))
                # # if row['lat'] and row['lon']:
                # if not pd.isna(row['lat']):
                #     random_integer = random.randint(1, 100)
                #     m = folium.Map(location=[row['lat']+random_integer*0.000000001, row['lon']], zoom_start=16)
                #     folium.Marker([row['lat'], row['lon']]).add_to(m)

                #     plugins.Fullscreen(                                                         
                #         position = "topleft",                                   
                #         title = "Open full-screen map",                       
                #         title_cancel = "Close full-screen map",                      
                #         force_separate_button = True,                                         
                #     ).add_to(m) 

                #     satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
                #     folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(m)
                #     # folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(map)
                #     folium.LayerControl(position='topleft').add_to(m)


                #     st_folium(m,use_container_width=True,height=300) # width=400,height=400)
                # else:
                #     print('no location',row['link'])

# def create_list(df,prov):
#     for index, row in df.iterrows():
#         COL = st.columns(3)
#         with COL[0]:
#             st.subheader(f":green[{index+1}/{df.shape[0]}[{row['sell_order']}]{row['type']}]")
#             st.markdown(f"***{row['tumbon']},{row['aumper']},{row['province']}***")

#             area = ''
#             a = ['ตร.ว.','งาน','ไร่']
#             for i in range(2, -1, -1):
#                 if isinstance(row[f'size{i}'], int) or isinstance(row[f'size{i}'], float):
#                     if row[f'size{i}'] != 0:
#                         area += f"{row[f'size{i}']} {a[i]} "
#             area = area[:-1]
#             st.markdown(f"**{area}**")

#             if st.button(f'delete favoare{index}'):
#                 st.write('delete complete!')
#                 update_sheet(person_id,prov,row['link'],0) 

#         with COL[1]:
#             # st.image("https://www.meridianhomes.net.au/wp-content/uploads/2018/01/Meridian-Homes_Double-Story_Cadence-2-1.jpg", caption=f'{i}Sunrise by the mountains',use_column_width='auto')
#             st.image(row['img0'], caption=f'{i}Sunrise by the mountains',use_column_width='auto')
        
#         with COL[2]:
#             # if st.button(f'Map{index}'):
#             url = "https://www.google.com/maps/place/13%C2%B054'23.3%22N+101%C2%B010'17.6%22E/@13.9064682,101.1689661,17z"
#             st.markdown(f'[Visit OpenAI]({url})')
#             try:
#                 st.image(row['img1'],use_column_width='auto')
#             except:
#                 pass
#                 # webbrowser.open_new_tab(url)

       

def get_data(province):
    # province = 'nonthaburi'
    url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/df_{province}.csv'
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df


cookie_manager = stx.CookieManager()
person_id = cookie_manager.get(cookie='person_id')

st.markdown(f'### {person_id}')

#init pygsheets
gc = pygsheets.authorize(service_account_file='led-sheet-47e8afe294c8.json')
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/16dO1zkakREjZxbjB6XFGijHFjjOUDYNpjwoeuUW5gP8/edit?usp=sharing')
worksheet = spreadsheet.sheet1

df_favorate = worksheet.get_as_df()

condition1 = df_favorate['user_id'] == person_id
condition2 = df_favorate['sta'] == 1
df_filter = df_favorate[condition1 & condition2]

# df_filter = df_favorate[df_favorate['user_id']==person_id]

# st.write(df_favorate)
# st.write(df_filter)

# st.write(df_filter['province'].unique())

tabs_list = list(df_filter['province'].unique())




if tabs_list:
    data = []
    for k in tabs_list:
        data.append(stx.TabBarItemData(id=k, title=k, description=""))
    chosen_idM = stx.tab_bar(data = data,default=tabs_list[0])







    # tabs = st.tabs(tabs_list)

    for index,p in enumerate(tabs_list):
        # with tabs[index]:
        if chosen_idM == p:
            df_favorate_province = df_filter[df_filter['province']==p]
            # st.write(df_favorate_province)
            # st.write(list(df_favorate_province['link']))

            df_province = get_data(p)
            # st.write(df_province)

            df = df_province[df_province['link'].isin(list(df_favorate_province['link']))]

            df = df.reset_index()
            #list
            # df = st.session_state["df"]
            # st.write(df)
            n_page = df.shape[0]//10 + 1

            # T = st.tabs([str(i) for i in range(1, n_page+1)])

            T = [str(i) for i in range(1, n_page+1)]

            data = []
            for k in T:
                data.append(stx.TabBarItemData(id=k, title=k, description=""))
            chosen_idMM = stx.tab_bar(data = data,default=T[0])

            for i in range(n_page):
                # with T[i]:
                if chosen_idMM == T[i]:
                    filtered_df = df.iloc[i*10:i*10+10]
                    create_list(filtered_df,df.shape[0],p)
                    # create_list(filtered_df,tabs_list[index])

else:
    st.markdown('#### No favorate property')

# def update_sheet(user_id,link):
#     df = worksheet.get_as_df()
#     result = df.isin([user_id,link]).all(axis=1)
#     if not result.any():
#         cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
#         last_row = len(cells)
#         # print(last_row)
#         worksheet.update_value(f'A{last_row+1}', user_id)
#         worksheet.update_value(f'B{last_row+1}', link)