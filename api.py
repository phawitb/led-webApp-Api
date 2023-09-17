# http://localhost:8504/Favorate/?name=joe
import streamlit as st
# import numpy as np
# import extra_streamlit_components as stx
import base64
# import firebase_admin
# from firebase_admin import credentials, firestore
import json
# import time
import pygsheets

#init pygsheets
gc = pygsheets.authorize(service_account_file='led-sheet-47e8afe294c8.json')
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/16dO1zkakREjZxbjB6XFGijHFjjOUDYNpjwoeuUW5gP8/edit?usp=sharing')
worksheet = spreadsheet.sheet1

# def update_sheet(user_id,province,link):
#     df = worksheet.get_as_df()
#     result = df.isin([user_id,province,link]).all(axis=1)
#     if not result.any():
#         cells = worksheet.get_all_values(include_tailing_empty_rows=None, include_tailing_empty=False, returnas='matrix')
#         last_row = len(cells)
#         # print(last_row)
#         worksheet.update_value(f'A{last_row+1}', user_id)
#         worksheet.update_value(f'B{last_row+1}', province)
#         worksheet.update_value(f'C{last_row+1}', link)

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

# cookie_manager = stx.CookieManager()
# person_id = cookie_manager.get(cookie='person_id')
# st.title(person_id)
try:
    url = st.experimental_get_query_params()
    if 'name' in url:
        name = url['name'][0]
    else:
        name = None
    if name:
        name = name[2:-1]
        decoded_bytes = base64.b64decode(name)
        decoded_string = decoded_bytes.decode('utf-8')
        data = json.loads(decoded_string)
        # st.write(data)
        # st.write(data['user_id'])
        # st.write(data['link'])

        update_sheet(data['user_id'],data['province_eng'],data['link'],1)
        

        st.title('Complete add to favorate')

except Exception as e:
    st.title('Error! can not add favorate',e)


# try:
#     cred = credentials.Certificate("led-webapp-752a2-firebase-adminsdk-7je9x-b7d6cf18d0.json")
#     firebase_admin.initialize_app(cred)
# except:
#     pass
# db = firestore.client()
# collection_ref = db.collection('favorate')

# cookie_manager = stx.CookieManager()
# person_id = cookie_manager.get(cookie='person_id')

# province = cookie_manager.get(cookie='province')
# # print('df',df)
# # st.write(province)
# # Get the current URL
# url = st.experimental_get_query_params()

# # Check if the "name" parameter is in the URL
# if 'name' in url:
#     name = url['name'][0]
# else:
#     name = None


# if name:
#     # st.write(name)
    
#     name = name[2:-1]
#     decoded_bytes = base64.b64decode(name)
#     decoded_string = decoded_bytes.decode('utf-8')
#     data = json.loads(decoded_string)
#     print('decoded_string',data)
#     # st.write(data)

#     #update fb link
#     link64 = base64.b64encode(data['link'].encode()).decode()
#     collection_ref = db.collection('links')
#     doc_ref = collection_ref.document(link64)
#     try:
#         doc_ref.update(data)
#     except:
#         doc_ref.set(data)

    
#     #update fb favorate
#     collection_ref = db.collection('favorate')
#     doc_ref = collection_ref.document(person_id)
#     d = {
#         str(time.time()).split('.')[0] :  link64,
#         # link64[-15:] : link64,
#     }
#     try:
#         doc_ref.update(d)
#     except:
#         doc_ref.set(d)

#     #show favorate data
#     doc_snapshot = doc_ref.get()
#     if doc_snapshot.exists:
#         data = doc_snapshot.to_dict()
#         st.write(data)
#     else:
#         pass




#     #     doc_ref.update(d)
#     #     # print("Document data:", data)
#     # else:
#     #     doc_ref.set(d)

#     # print('firsttime',firsttime)
#     # if firsttime:
#     #     firsttime = False
#     #     try:
#     #         doc_ref.update(d)
#     #     except:
#     #         doc_ref.set(d)
    


#     # collection_name = "favorate"
#     # document_id = "legalexecution.app@gmail.com"
#     # doc_ref = db.collection(collection_name).document(document_id)

#     # doc_data = doc_ref.get()
    
#     # print('1111',doc_data)

#     # try:
#     #     doc_data = doc_ref.get()
#     #     doc_ref.update(d)
#     # except:
#     #     doc_ref.set(d)

#     # print('doc_data',doc_data)
#     # if doc_data:
#     #     doc_ref.update(d)
#     #     # print("Document data:", data)
#     # else:
#     #     doc_ref.set(d)



#     # doc_ref.update(d)

#     # try:
#     #     doc_ref.update(d)
#     # except:
#     #     doc_ref.set(d)











#     # st.write(name)
#     # name = name.replace(' ','+')
#     # decoded_bytes = base64.b64decode(name)
#     # decoded_text = decoded_bytes.decode('utf-8')
#     # st.write(decoded_text)


    



# else:
#     st.write(f"please login")



# # tab1, tab2 = st.tabs(["📈 Lists", "🗃 Map"])
# # data = np.random.randn(10, 1)

# # tab1.subheader("A tab with a chart")
# # tab1.line_chart(data)

# # tab2.subheader("A tab with the data")
# # tab2.write(data)

