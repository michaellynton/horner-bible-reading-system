from itertools import cycle, zip_longest, count, repeat
import yaml
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
#import pendulum
import streamlit as st




def build_chapters(book_list):
    chapters = []
    for k,v in book_list.items():
        for chap in range(1,v+1):
            reading = f'{k} {chap}'
            chapters.append(reading)
    return chapters


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def main():

    st.title('Professor Grant Horner\'s Bible Reading System', anchor=None)
    #body = """
    #- Read one chapter from each list each day; in one sitting or two. At the end of a book; go to the next book. At the end of the list; start it again. Do it in the order given above.
    #- Read quickly (without “speed-reading”) in order to get the overall sense. Read as fast as you comfortably can with moderate retention. You're not studying deeply or memorizing; shoot for 5-6 minutes per chapter. At the end of a chapter, move immediately to the next list.
    #- GET THROUGH THE TEXT -- no dawdling, back reading, looking up cross-references!
    #- There are different 'kinds' of reading: super-quick skimming, careful moderate-paced, studying the text, deep meditation. You should be between the first and second kind.
    #- Most people decrease their time spent and increase their retention after just two-three weeks! I now read and retain the entire text of Matthew in 35 minutes, Romans in 20, Genesis in one hour!
    #- Don't look up anything you 'don't get' -- real understanding will come through contextualizing by reading a LOT of scripture over time. Get through the text!
    #- If you miss a day or two -- ok, get over it, then keep going. Don't cover yourself in sackcloth and ashes and quit! Move the bookmarks along, to find your place(s) quickly next day.
      #Heb 4:12 & 5:11-14; Eph 5:26 & 6:17; Col 3:16; 2 Tim 3:16; Ps 119; Ezra 8; Prov 3: 1-2, 10:14; Dan 1
    #- If you are wondering why you should read Acts (or Proverbs) all the way through every single month, then -- you've just shown that you NEED to read them that often!  
    #- The goal of this system is simple, and twofold: To know scripture, and to love and obey God more!  
#      
    #SOLI DEO GLORIA
    #"""
    
    body = """
    This is a simple application which will generate the reading plan for you. You may
    enter the starting day and the number of days which you want to generate a reading plan for. 

    For example, if I'm starting, and I want the first 30 days of the plan, I would go with the default. 

    But next month, I mwould come back and use day 31 as my start, and maybe this time I want to generate 60 days 
    of the plan instead of 30 days. 
    """


    #col1, col2 = st.columns(2)
    #with col1:
        #start = st.number_input('Start at day:', value=1)

    counter = 0
    #start = 1
    start = st.sidebar.number_input('Start at day:', value=1)
    #end = 99
    hundred_yrs = 36500
    end = st.sidebar.number_input('Return number of days:', value=31)
    st.sidebar.markdown(body)
    
    reading_plan = []
    books = ['list_1', 
            'list_2',
            'list_3',
            'list_4',
            'list_5',
            'list_6',
            'list_7',
            'list_8',
            'list_9',
            'list_10',]

    with open('lists.yml', 'r') as file:
        lists = yaml.safe_load(file)

    #l1dict, l2dict, l3dict, l4dict, l5dict, l6dict, l7dict, l8dict, l9dict, l10dict = [lists.get(k) for k in books]
    #l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 = [build_chapters(i) for i in (l1dict, l2dict, l3dict, l4dict, l5dict, l6dict, l7dict, l8dict, l9dict, l10dict)]
    
    # Combine the two lines above
    l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 = [build_chapters(i) for i in [lists.get(k) for k in books]]

    for i in zip(count(start), cycle(l1), cycle(l2), cycle(l3), cycle(l4), cycle(l5), cycle(l6), cycle(l7), cycle(l8), cycle(l9), cycle(l10)):
        reading_plan.append(i)
        counter += 1
        #if counter > end-1:
        if counter > hundred_yrs-1:
            break
    
    df = pd.DataFrame(reading_plan, columns = ['Day'] + [b.title().replace('_',' ') for b in books])
    #df = df.reset_index(drop=True)
    #file_dt = pendulum.now().to_date_string()
    #filename = f'reading_{start}_{end}.csv'
    #df.to_csv(filename, index=False)
    df = df.set_index('Day')
    df = df.rename_axis('Day')
    
    
    #df = df[start-1:end]
    filter_list = range(start,end)
    df_filtered = df[df.index.isin(filter_list)]

    csv = convert_df(df_filtered)

    with st.container():
        st.dataframe(df_filtered)  # Same as st.write(df)

        st.download_button(
            label="Download reading plan as CSV",
            data=csv,
            file_name=f'reading_plan__day_{start}_to_{end}.csv',
            mime='text/csv',
        )


# --------------------------------------------------
if __name__ == "__main__":
    main()
