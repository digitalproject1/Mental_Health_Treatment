import streamlit as st
import pandas as pd
import io
from pandas.api.types import (
    is_categorical_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from sklearn.preprocessing import LabelEncoder

# import visualization package
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px

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
                 
            }
            .font-small {
                 font-size: middle;
            }
        </style>
        <body>
            <h1 class='font-big'>Data Visualization</h1>
        <body>
        """
@st.cache
def load_data(data):
    df = pd.read_csv(data)
    df = df.iloc[:,1:]
    return df  

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = load_data("Data_Source/survey.csv")
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

def ds_eda_app():
    df = load_data("Data_Source/survey.csv")
    
    # Data Cleansing for Null Value and Unnecessary Features
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
    if submenu == "Visualization":
        st.write(temp_2,unsafe_allow_html=True)
        with st.expander("Treatment Composition "):
                 fig=px.pie(df_clean['treatment'],
                   title="Treatment Composition",
                   names="treatment",
                   color='treatment',
                    color_discrete_map={'Yes':'royalblue','No':'yellow'})
                 st.plotly_chart(fig)
        
        col1,col2= st.columns([2,2])
        organizer_gender()       
        with col1: 
            with st.expander("Comparasion of Total Treatment based on Country "):
                 Treat=df_clean[df_clean['treatment'] == 'Yes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Treatment = ('treatment', 'count'))\
                                              .sort_values(['Treatment'], ascending=False)\
                                              .head(10)
                 NoTreat=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Country'], as_index=True)\
                                              .agg(NoTreatment = ('treatment', 'count'))\
                                              .sort_values(['NoTreatment'], ascending=False)\
                                              .head(10)                           
                 plot_tt_country=Treat.merge(NoTreat,left_on='Country',right_on='Country')
                 st.bar_chart(plot_tt_country)

            with st.expander("Comparison of Total Treatment based on Gender"):
                 Treat=df_clean[df_clean['treatment'] == 'Yes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Treatment = ('treatment', 'count'))\
                                              .sort_values(['Treatment'], ascending=False)
                 NoTreat=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Gender'], as_index=True)\
                                              .agg(NoTreatment = ('treatment', 'count'))\
                                              .sort_values(['NoTreatment'], ascending=False)                         
                 plot_tt_gender=Treat.merge(NoTreat,left_on='Gender',right_on='Gender')
                 st.bar_chart(plot_tt_gender)
                
            with st.expander("Comparasion of Total Treatment based on Age "):
                 Treat=df_clean[df_clean['treatment'] == 'Yes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Treatment = ('treatment', 'count'))\
                                              .sort_values(['Treatment'], ascending=False)                             
                 NoTreat=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Age'], as_index=True)\
                                              .agg(NoTreatment = ('treatment', 'count'))\
                                              .sort_values(['NoTreatment'], ascending=False)                        
                 plot_tt_age=Treat.merge(NoTreat,left_on='Age',right_on='Age')
                 st.bar_chart(plot_tt_age)
        with col2: 
             with st.expander("Comparasion of Work Interferes based on Country"):
                 Often=df_clean[df_clean['work_interfere'] == 'Often'].groupby(by=['Country'], as_index=True)\
                                              .agg(Often = ('work_interfere', 'count'))\
                                              .sort_values(['Often'], ascending=False)\
                                              .head(10)
                 Rarely=df_clean[df_clean['work_interfere'] == 'Rarely'].groupby(by=['Country'], as_index=True)\
                                              .agg(Rarely = ('work_interfere', 'count'))\
                                              .sort_values(['Rarely'], ascending=False)\
                                              .head(10)
                 Never=df_clean[df_clean['work_interfere'] == 'Never'].groupby(by=['Country'], as_index=True)\
                                              .agg(Never = ('work_interfere', 'count'))\
                                              .sort_values(['Never'], ascending=False)\
                                              .head(10)
                 Sometimes=df_clean[df_clean['work_interfere'] == 'Sometimes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Sometimes = ('work_interfere', 'count'))\
                                              .sort_values(['Sometimes'], ascending=False)\
                                              .head(10)     
                 s1=Often.merge(Rarely,left_on='Country',right_on='Country')
                 s2=Never.merge(Sometimes,left_on='Country',right_on='Country')
                 plot_wi_country=s1.merge(s2,left_on='Country',right_on='Country')                       
                 st.bar_chart(plot_wi_country) 
             with st.expander("Comparasion of Work Interferes based on Gender"):
                    Often=df_clean[df_clean['work_interfere'] == 'Often'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Often = ('work_interfere', 'count'))\
                                              .sort_values(['Often'], ascending=False)
                    Rarely=df_clean[df_clean['work_interfere'] == 'Rarely'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Rarely = ('work_interfere', 'count'))\
                                              .sort_values(['Rarely'], ascending=False)
                    Never=df_clean[df_clean['work_interfere'] == 'Never'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Never = ('work_interfere', 'count'))\
                                              .sort_values(['Never'], ascending=False)
                    Sometimes=df_clean[df_clean['work_interfere'] == 'Sometimes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Sometimes = ('work_interfere', 'count'))\
                                              .sort_values(['Sometimes'], ascending=False)                           
                    plot_wi_gender=pd.concat([Often,Rarely,Never,Sometimes],axis='columns')
                    st.bar_chart(plot_wi_gender)
             with st.expander("Comparasion of Work Interferes based on Age"):
                    Often=df_clean[df_clean['work_interfere'] == 'Often'].groupby(by=['Age'], as_index=True)\
                                              .agg(Often = ('work_interfere', 'count'))\
                                              .sort_values(['Often'], ascending=False)
                    Rarely=df_clean[df_clean['work_interfere'] == 'Rarely'].groupby(by=['Age'], as_index=True)\
                                              .agg(Rarely = ('work_interfere', 'count'))\
                                              .sort_values(['Rarely'], ascending=False)
                    Never=df_clean[df_clean['work_interfere'] == 'Never'].groupby(by=['Age'], as_index=True)\
                                              .agg(Never = ('work_interfere', 'count'))\
                                              .sort_values(['Never'], ascending=False)
                    Sometimes=df_clean[df_clean['work_interfere'] == 'Sometimes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Sometimes = ('work_interfere', 'count'))\
                                              .sort_values(['Sometimes'], ascending=False)                           
                    plot_wi_age=pd.concat([Often,Rarely,Never,Sometimes],axis='columns')
                    st.bar_chart(plot_wi_age)
        with st.expander("Supporting Facilities"):            
            top_country = df_clean['Country'].value_counts().idxmax()

            # Filter the data for the top country
            filtered_data = df_clean[df_clean['Country'] == top_country]

            # Group by 'Country' and 'benefits' to calculate the total count of each benefit category for the top country
            supporting_facilities = filtered_data.groupby(by=['Country', 'benefits'], as_index=False) \
                          .agg(TotalBenefits=('benefits', 'count')) \
                          .sort_values(['TotalBenefits'], ascending=False)
            fig=plt.figure(figsize=(15, 10))

            # Variables of Supporting Facilities
            supporting_facilities = ['benefits', 'care_options', 'wellness_program', 'seek_help', 'leave']

            # Create subplots
            for i, variable in enumerate(supporting_facilities, 1):
                plt.subplot(2, 3, i)
                if i <= 3:
                        sns.countplot(data=filtered_data, x=variable, order=filtered_data[variable].value_counts().index, color ='#ec838a')
                else:
                        sns.countplot(data=filtered_data, x=variable, order=filtered_data[variable].value_counts().index, color ='#9b9c9a')
                        plt.title(variable)
                        plt.xticks(rotation=45)

            # Add Bar Label
            for index, value in enumerate(filtered_data[variable].value_counts().values):
                plt.annotate(str(value), xy=(index, value), ha='center', va='bottom')

            # Adjust the layout and display the plot
            plt.tight_layout()
            st.pyplot(fig)
        with st.expander("Transperency and Confidentiatlity"):
             # Transperency and Confidentiality
            transperency_and_confidentiality = ['anonymity', 'mental_health_consequence', 'coworkers', 'supervisor', 'obs_consequence']

            # Create subplots
            for i, variable in enumerate(transperency_and_confidentiality, 1):
                plt.subplot(2, 3, i)
                if i <= 3:
                    sns.countplot(data=filtered_data, x=variable, order=filtered_data[variable].value_counts().index, color ='#ec838a')
                else:
                    sns.countplot(data=filtered_data, x=variable, order=filtered_data[variable].value_counts().index, color ='#9b9c9a')
                    plt.title(variable)
                    plt.xticks(rotation=45)
                   
            # Add Bar Label
            for index, value in enumerate(filtered_data[variable].value_counts().values):
                plt.annotate(str(value), xy=(index, value), ha='center', va='bottom')

            # Adjust the layout and display the plot
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.tight_layout()
            st.pyplot()

        with st.expander("Accesibility"):
             # Accesibility
            accesibility = ['mental_health_interview', 'mental_vs_physical']

             # Create subplots
            for i, variable in enumerate(accesibility, 1):
                plt.subplot(1, 2, i)
                if i == 1:
                    sns.countplot(data=filtered_data, x=variable, order=filtered_data[variable].value_counts().index, color ='#ec838a')
                else:
                    sns.countplot(data=filtered_data, x=variable, order=filtered_data[variable].value_counts().index, color ='#9b9c9a')
                    plt.title(variable)
                    plt.xticks(rotation=45)

            # Add Bar Label
            for index, value in enumerate(filtered_data[variable].value_counts().values):
                plt.annotate(str(value), xy=(index, value), ha='center', va='bottom')

            # Adjust the layout and display the plot
            st.set_option('deprecation.showPyplotGlobalUse', False)
            plt.tight_layout()
            st.pyplot()
        
    elif submenu == "Description":
        st.write(temp_1,unsafe_allow_html=True)
        st.dataframe(filter_dataframe(df))
        
        with st.expander("Dataset Summary"):
            buffer = io.StringIO()
            df_clean.info(buf=buffer)
            x=buffer.getvalue()
            st.text(x)

        with st.expander("Descriptive Summary"):
            st.dataframe(df_clean.describe(include='all').T)
        
        col1,col2,col3 = st.columns([2,2,2])
        organizer_gender()
        with col1: 
            with st.expander("Country Distribution"):
                 st.dataframe(df_clean.groupby(by='Country').agg(Qty=('Country','count')).sort_values('Qty',ascending=False))
        with col2:
            with st.expander("Gender Distribution"):
                     st.dataframe(df_clean.groupby(by='Gender').agg(Qty=('Gender','count')).sort_values(by='Qty',ascending=False))
        with col3:
            with st.expander("Age Distribution"):
                 #age restriction
                 df_clean_age = df_clean[(df['Age'] >= 17) & (df_clean['Age'] <= 99)]
                 st.dataframe(df_clean_age.groupby(by='Age').agg(Qty=('Age','count')).sort_values(by='Qty',ascending=False))

        col1,col2 = st.columns([2,2])
        with col1:
            with st.expander("Total Treatment Comparison based on Country"):
                 Treat=df_clean[df_clean['treatment'] == 'Yes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Treatment = ('treatment', 'count'))\
                                              .sort_values(['Treatment'], ascending=False)\
                                              .head(10)
                 NoTreat=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Country'], as_index=True)\
                                              .agg(NoTreatment = ('treatment', 'count'))\
                                              .sort_values(['NoTreatment'], ascending=False)\
                                              .head(10)                           
                 st.dataframe(Treat.merge(NoTreat,left_on='Country',right_on='Country'))
            with st.expander("Total Treatment Comparison based on Gender"):
                     Treat=df_clean[df_clean['treatment'] == 'Yes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Treatment = ('treatment', 'count'))\
                                              .sort_values(['Treatment'], ascending=False)\
                                              .head(10)
                     NoTreat=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Gender'], as_index=True)\
                                              .agg(NoTreatment = ('treatment', 'count'))\
                                              .sort_values(['NoTreatment'], ascending=False)\
                                              .head(10)                           
                     st.dataframe(Treat.merge(NoTreat,left_on='Gender',right_on='Gender'))
            with st.expander("Total Treatment Comparison based on Age"):
                 Treat=df_clean[df_clean['treatment'] == 'Yes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Treatment = ('treatment', 'count'))\
                                              .sort_values(['Treatment'], ascending=False)
                 NoTreat=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Age'], as_index=True)\
                                              .agg(NoTreatment = ('treatment', 'count'))\
                                              .sort_values(['NoTreatment'], ascending=False)                           
                 st.dataframe(Treat.merge(NoTreat,left_on='Age',right_on='Age'))
            with st.expander("Family History Comparison based on Country"):
                 Positif=df_clean[df_clean['family_history'] == 'Yes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Positif = ('family_history', 'count'))\
                                              .sort_values(['Positif'], ascending=False)\
                                              .head(10)
                 Negatif=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Country'], as_index=True)\
                                              .agg(Negatif = ('family_history', 'count'))\
                                              .sort_values(['Negatif'], ascending=False)\
                                              .head(10)    
                 st.dataframe(Positif.merge(Negatif,left_on='Country',right_on='Country')) 
            with st.expander("Family History Comparison based on Gender"):
                 Positif=df_clean[df_clean['family_history'] == 'Yes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Positif = ('family_history', 'count'))\
                                              .sort_values(['Positif'], ascending=False)\
                                              .head(10)
                 Negatif=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Negatif = ('family_history', 'count'))\
                                              .sort_values(['Negatif'], ascending=False)\
                                              .head(10)    
                 st.dataframe(Positif.merge(Negatif,left_on='Gender',right_on='Gender')) 
            with st.expander("Family History Comparison based on Age"):
                 Positif=df_clean[df_clean['family_history'] == 'Yes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Positif = ('family_history', 'count'))\
                                              .sort_values(['Positif'], ascending=False)
                 Negatif=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Age'], as_index=True)\
                                              .agg(Negatif = ('family_history', 'count'))\
                                              .sort_values(['Negatif'], ascending=False)    
                 st.dataframe(Positif.merge(Negatif,left_on='Age',right_on='Age')) 
            with st.expander("Remote Work Comparison based on Country"):
                 Remotly=df_clean[df_clean['remote_work'] == 'Yes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Remotly = ('remote_work', 'count'))\
                                              .sort_values(['Remotly'], ascending=False)\
                                              .head(10)
                 UnRemotly=df_clean[df_clean['remote_work'] == 'No'].groupby(by=['Country'], as_index=True)\
                                              .agg(UnRemotly = ('remote_work', 'count'))\
                                              .sort_values(['UnRemotly'], ascending=False)\
                                              .head(10)    
                 st.dataframe(Remotly.merge(UnRemotly,left_on='Country',right_on='Country')) 
            with st.expander("Remote Work Comparison based on Gender"):
                 Remotly=df_clean[df_clean['remote_work'] == 'Yes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Remotly = ('remote_work', 'count'))\
                                              .sort_values(['Remotly'], ascending=False)\
                                              .head(10)
                 UnRemotly=df_clean[df_clean['remote_work'] == 'No'].groupby(by=['Gender'], as_index=True)\
                                              .agg(UnRemotly = ('remote_work', 'count'))\
                                              .sort_values(['UnRemotly'], ascending=False)\
                                              .head(10)    
                 st.dataframe(Remotly.merge(UnRemotly,left_on='Gender',right_on='Gender')) 
            with st.expander("Remote Work Comparison based on Age"):
                 Remotly=df_clean[df_clean['remote_work'] == 'Yes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Remotly = ('remote_work', 'count'))\
                                              .sort_values(['Remotly'], ascending=False)
                 UnRemotly=df_clean[df_clean['remote_work'] == 'No'].groupby(by=['Age'], as_index=True)\
                                              .agg(UnRemotly = ('remote_work', 'count'))\
                                              .sort_values(['UnRemotly'], ascending=False)    
                 st.dataframe(Remotly.merge(UnRemotly,left_on='Age',right_on='Age')) 

        with col2: 
            with st.expander("Work Interfere Comparison based on Country"):
                 Often=df_clean[df_clean['work_interfere'] == 'Often'].groupby(by=['Country'], as_index=True)\
                                              .agg(Often = ('work_interfere', 'count'))\
                                              .sort_values(['Often'], ascending=False)\
                                              .head(10)
                 Rarely=df_clean[df_clean['work_interfere'] == 'Rarely'].groupby(by=['Country'], as_index=True)\
                                              .agg(Rarely = ('work_interfere', 'count'))\
                                              .sort_values(['Rarely'], ascending=False)\
                                              .head(10)
                 Never=df_clean[df_clean['work_interfere'] == 'Never'].groupby(by=['Country'], as_index=True)\
                                              .agg(Never = ('work_interfere', 'count'))\
                                              .sort_values(['Never'], ascending=False)\
                                              .head(10)
                 Sometimes=df_clean[df_clean['work_interfere'] == 'Sometimes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Sometimes = ('work_interfere', 'count'))\
                                              .sort_values(['Sometimes'], ascending=False)\
                                              .head(10)
                 s1=Often.merge(Rarely,left_on='Country',right_on='Country')
                 s2=Never.merge(Sometimes,left_on='Country',right_on='Country')
                 st.dataframe(s1.merge(s2,left_on='Country',right_on='Country'))      

            with st.expander("Work Interfere Comparison based on Gender"):
                 Often=df_clean[df_clean['work_interfere'] == 'Often'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Often = ('work_interfere', 'count'))\
                                              .sort_values(['Often'], ascending=False)
                 Rarely=df_clean[df_clean['work_interfere'] == 'Rarely'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Rarely = ('work_interfere', 'count'))\
                                              .sort_values(['Rarely'], ascending=False)
                 Never=df_clean[df_clean['work_interfere'] == 'Never'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Never = ('work_interfere', 'count'))\
                                              .sort_values(['Never'], ascending=False)
                 Sometimes=df_clean[df_clean['work_interfere'] == 'Sometimes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Sometimes = ('work_interfere', 'count'))\
                                              .sort_values(['Sometimes'], ascending=False)
                 s1=Often.merge(Rarely,left_on='Gender',right_on='Gender')
                 s2=Never.merge(Sometimes,left_on='Gender',right_on='Gender')
                 st.dataframe(s1.merge(s2,left_on='Gender',right_on='Gender'))                         
                 
            with st.expander("Work Interfere Comparison based on Age"):
                 Often=df_clean[df_clean['work_interfere'] == 'Often'].groupby(by=['Age'], as_index=True)\
                                              .agg(Often = ('work_interfere', 'count'))\
                                              .sort_values(['Often'], ascending=False)
                 Rarely=df_clean[df_clean['work_interfere'] == 'Rarely'].groupby(by=['Age'], as_index=True)\
                                              .agg(Rarely = ('work_interfere', 'count'))\
                                              .sort_values(['Rarely'], ascending=False)
                 Never=df_clean[df_clean['work_interfere'] == 'Never'].groupby(by=['Age'], as_index=True)\
                                              .agg(Never = ('work_interfere', 'count'))\
                                              .sort_values(['Never'], ascending=False)
                 Sometimes=df_clean[df_clean['work_interfere'] == 'Sometimes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Sometimes = ('work_interfere', 'count'))\
                                              .sort_values(['Sometimes'], ascending=False)                       
                 s1=Often.merge(Rarely,left_on='Age',right_on='Age')
                 s2=Never.merge(Sometimes,left_on='Age',right_on='Age')
                 st.dataframe(s1.merge(s2,left_on='Age',right_on='Age')) 

            with st.expander("Self Employed Status Comp. based on Country"):
                 Self=df_clean[df_clean['self_employed'] == 'Yes'].groupby(by=['Country'], as_index=True)\
                                              .agg(Self = ('self_employed', 'count'))\
                                              .sort_values(['Self'], ascending=False)\
                                              .head(10)
                 NotSelf=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Country'], as_index=True)\
                                              .agg(NotSelf = ('self_employed', 'count'))\
                                              .sort_values(['NotSelf'], ascending=False)\
                                              .head(10)    
                 st.dataframe(Self.merge(NotSelf,left_on='Country',right_on='Country'))  
            with st.expander("Self Employed Status Comp. based on Gender"):
                 Self=df_clean[df_clean['self_employed'] == 'Yes'].groupby(by=['Gender'], as_index=True)\
                                              .agg(Self = ('self_employed', 'count'))\
                                              .sort_values(['Self'], ascending=False)
                 NotSelf=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Gender'], as_index=True)\
                                              .agg(NotSelf = ('self_employed', 'count'))\
                                              .sort_values(['NotSelf'], ascending=False)  
                 st.dataframe(Self.merge(NotSelf,left_on='Gender',right_on='Gender'))
            with st.expander("Self Employed Status Comp. based on Age"):
                 Self=df_clean[df_clean['self_employed'] == 'Yes'].groupby(by=['Age'], as_index=True)\
                                              .agg(Self = ('self_employed', 'count'))\
                                              .sort_values(['Self'], ascending=False)
                 NotSelf=df_clean[df_clean['treatment'] == 'No'].groupby(by=['Age'], as_index=True)\
                                              .agg(NotSelf = ('self_employed', 'count'))\
                                              .sort_values(['NotSelf'], ascending=False)    
                 st.dataframe(Self.merge(NotSelf,left_on='Age',right_on='Age'))
                
if __name__ == "__main__":
    ds_eda_app()
