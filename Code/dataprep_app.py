import streamlit as st
import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

temp_1 = """
        <style>
            h1 {
                font-size: 18px;
                color: white;
            }
            .font-big {
                 font-size: large;
            }
            .font-small {
                 font-size: middle;
            }
        </style>
        <body>
            <h1 class='font-big'>Dataset Preview</h1>
        <body>
        """
temp_2 = """
        <style>
            h1 {
                font-size: 18px;
                color: white;
            }
            .font-big {
                 font-size: large;
                 font-
            }
            .font-small {
                 font-size: middle;
            }
        </style>
        <body>
            <h1 class='font-big'>Data Visualization</h1>
        <body>
        """
@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    df = df.iloc[:,1:]
    return df  
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = load_data("/Data Privasi/laptop\Python/Final Project/Code/survey.csv")
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
                _min = int(17)
                _max = int(99)
                step = (1)
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

def run_dataprep_app():
    df = load_data("/Data Privasi/laptop\Python/Final Project/Code/survey.csv")
    
    # Data Cleansing for Null Value, Unnecessary Features 
    columns_to_drop = ['state', 'comments', 'Timestamp']
    df_clean = df.drop(columns=[col for col in columns_to_drop if col in df])
    df_clean['work_interfere'].fillna(df_clean['work_interfere'].mode()[0], inplace=True)
    df_clean['self_employed'].fillna(df_clean['self_employed'].mode()[0], inplace=True)
    
    def organizer_gender():
        organize_genders = {
                    'Male ': 'Male',
                    'male': 'Male',
                    'M': 'Male',
                    'm': 'Male',
                    'Male': 'Male',
                    'Cis Male': 'Male',
                    'Man': 'Male',
                    'cis male': 'Male',
                    'Mail': 'Male',
                    'Male-ish': 'Male',
                    'Male (CIS)': 'Male',
                    'Cis Man': 'Male',
                    'msle': 'Male',
                    'Malr': 'Male',
                    'Mal': 'Male',
                    'maile': 'Male',
                    'Make': 'Male',
                    'Female ': 'Female',
                    'female': 'Female',
                    'F': 'Female',
                    'f': 'Female',
                    'Woman': 'Female',
                    'Female': 'Female',
                    'femail': 'Female',
                    'Cis Female': 'Female',
                    'cis-female/femme': 'Female',
                    'Femake': 'Female',
                    'Female (cis)': 'Female',
                    'woman': 'Female',
                    'Female (trans)': 'Other',
                    'queer/she/they': 'Other',
                    'non-binary': 'Other',
                    'fluid': 'Other',
                    'queer': 'Other',
                    'Androgyne': 'Other',
                    'Trans-female': 'Other',
                    'male leaning androgynous': 'Other',
                    'Agender': 'Other',
                    'A little about you': 'Other',
                    'Nah': 'Other',
                    'All': 'Other',
                    'ostensibly male, unsure what that really means': 'Other',
                    'Genderqueer': 'Other',
                    'Enby': 'Other',
                    'p': 'Other',
                    'Neuter': 'Other',
                    'something kinda male?': 'Other',
                    'Guy (-ish) ^_^': 'Other',
                    'Trans woman': 'Other'
                    }               
        df_clean['Gender'].replace(organize_genders,inplace=True)
    

    submenu = st.sidebar.selectbox("SubMenu",["Visualization","Description"])
    organizer_gender()
    if submenu == "Visualization":
        st.write(temp_2,unsafe_allow_html=True)
        
        df_clean_age = df_clean[(df['Age'] >= 17) & (df_clean['Age'] <= 99)]
        work_interfere_b=df['work_interfere'].value_counts()
        work_interfere_a=df_clean['work_interfere'].value_counts()
        self_employed_b=df['self_employed'].value_counts()
        self_employed_a=df_clean['self_employed'].value_counts()

        col1,col2=st.columns([2,2])
        
        col1.write("Data Plot Work Interfere Before Cleansing")
        col1.bar_chart(work_interfere_b)
        col1.write("Data Plot Self Employed Before Cleansing")
        col1.bar_chart(self_employed_b)
        col1.write('Data Plot Genders Before Cleansing and New Categorizing')   
        col1.bar_chart(df['Gender'].value_counts())    
        col1.write('Data Plot Age Before Age Restriction')  
        col1.bar_chart(df['Age'].value_counts())    
                
        col2.write("Data Plot Work Interfere After Cleansing")
        col2.bar_chart(work_interfere_a) 
        col2.write("Data Plot Self Employed After Cleansing")
        col2.bar_chart(self_employed_a)
        col2.write('Data Plot Genders After cleansing and New Categorizing')   
        col2.bar_chart(df_clean['Gender'].value_counts())
        col2.write('Data Plot Age After Age Restriction')   
        col2.bar_chart(df_clean_age['Age'].value_counts())


    elif submenu == "Description":
        st.write(temp_1,unsafe_allow_html=True)
        st.dataframe(filter_dataframe(df))
        col1,col2=st.columns([2,2])
        with col1:          
            with st.expander("Check Data Null Value Before Cleansing"):
                st.dataframe(df.isnull().sum())
            with st.expander("Check Data Unique Gender Before Cleansing"):
                 st.dataframe(df.groupby(by='Gender').agg(Qty=('Gender','count')).sort_values(by='Qty',ascending=False))
                 st.text('%s%s' % (df['Gender'].nunique(),' data')) 
            with st.expander("Check Data Unique Age Before Cleansing"):
                 st.dataframe(df.groupby(by='Age').agg(Qty=('Age','count')).sort_values(by='Qty',ascending=False))
                 st.text('%s%s' % (df['Age'].nunique(),' data'))
        with col2:
            with st.expander("Check Data Null Value After Cleansing"):
                st.dataframe(df_clean.isnull().sum())
            with st.expander("Check Data Unique Gender After Cleansing"):
                 st.dataframe(df_clean.groupby(by='Gender').agg(Qty=('Gender','count')).sort_values(by='Qty',ascending=False))
                 st.text('%s%s' % (df_clean['Gender'].nunique(),' data'))
            with st.expander("Check Data Unique Age After Cleansing"):
                 #age restriction
                 df_clean_age = df_clean[(df['Age'] >= 17) & (df_clean['Age'] <= 99)]

                 st.dataframe(df_clean_age.groupby(by='Age').agg(Qty=('Age','count')).sort_values(by='Qty',ascending=False))
                 st.text('%s%s' % (df_clean_age['Age'].nunique(),' data'))
if __name__ == "__main__":
    run_ds_dataprep_clean_app()
