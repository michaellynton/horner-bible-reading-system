import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.title('Professor Grant Horner\'s Bible Reading System', anchor=None)

st.write(
    """This is a simple app to generate the reading plan for you. You can
    enter the starting and ending day which you want to generate a reading plan for. 
    For example, if I'm starting, and I want the first 30 days of the plan, I would go with the default. 
    Next month, I can come back and download days 31 to 60.
    Read the full [PDF](http://github.com/raw/...professor-grant-horners-bible-reading-system.pdf)
    """
)



@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')


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
        #to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        to_filter_columns = ['Day']

        for column in to_filter_columns:
            left, right, outer = st.columns((1, 20, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if 'Day' in column:
                user_num_input_start = right.number_input(
                    f"Starting {column}", value = 1
                )
                user_num_input_end = outer.number_input(
                    f"Ending {column}", value = 30
                )
                user_num_input = (user_num_input_start, user_num_input_end)
                df = df[df[column].between(*user_num_input)]
            
            elif is_categorical_dtype(df[column]) or df[column].nunique() < 10:
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
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )

                user_num_input_start = right.number_input(
                    f"Starting {column}", value = 1
                )
                user_num_input_end = middle.number_input(
                    f"Ending {column}", value = 30
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
            elif 'List' in  column:
                pass # return list of discete books to filter on
                #df['List 1'].str.extract('(\D+)')
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

        # Download data
        _min = int(df['Day'].min())
        _max = int(df['Day'].max())
        st.download_button(
            label="Download reading plan as CSV",
            #data=df.to_csv().encode('utf-8'),
            data=convert_df(df),
            file_name=f'reading_plan__day_{_min}_to_{_max}.csv',
            mime='text/csv',
        )

    return df


df = pd.read_csv(
    "reading_plan.csv"
)
st.dataframe(filter_dataframe(df))