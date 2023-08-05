import streamlit as st
import streamlit.components.v1 as stc

from eda_app import ds_eda_app
from dataprep_app import ds_dataprep_app
from ml_app import ds_ml_app

home_temp = """
            <div style="background-color:#0e0f3f;padding:1px;border-radius:25px">
		    <h2 style="color:white;font-family:calibri;text-align:center;">FINAL PROJECT - DATA SCIENCE </h2>
            </div>
            """
home2_temp = """
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

            <style type="text/css">
                    .left    { text-align: left;}
                    .right   { text-align: right;}
                    .center  { text-align: center;}
                    .justify-italic { text-align: justify;font-style:italic;line-height:1.2;}
                  ul.justify-bullet { text-align: justify;list-style-position: outside;line-height:1.3}
                  ol.justify-numbering { text-align: justify;list-style-position: outside;line-height:1.4}
            </style>
            """
about_temp = """
            <div style="background-color:#0e0f3f;padding:1px;border-radius:25px">
		    <h2 style="color:white;font-family:calibri;text-align:center;">MENTAL HEALTH TREATMENT PREDICTION SYSTEM </h2>
            </div>
            """
desc_about_temp = """
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

                <style type="text/css">
                    .left    { text-align: left;}
                    .right   { text-align: right;}
                    .center  { text-align: center;}
                    .justify-italic { text-align: justify;font-style:italic;line-height:1.2;}
                  ul.justify-bullet { text-align: justify;list-style-position: outside;line-height:1.3}
                  ol.justify-numbering { text-align: justify;list-style-position: outside;line-height:1.4}
                </style>

                <body>
                        <p> Data Source :
                            <a href="https://www.kaggle.com/code/numbrami/mental-health-treatment-prediction#Random-Forest-Classifier" title = "Menuju ke link data source"
                            >https://www.kaggle.com/code</a>
                        </p>
                    <h1 class='font-big'>About Dataset</h1>
                        <p class="justify-italic">"Mental Health in Tech Survey" is the dataset that was collected in 2014. This data is the result of the survey that measures 
                                                    attitude toward mental health and frequency of mental illness disorders in one of the tech workplace.</p>
                    <h1 class='font-big'>Research Question</h1>
                        <p class="left">The aim of our study is to answer the below research questions:</p>
                    <ul class="justify-bullet">
                        <li>How does the frequency of mental illness vary by geographic location ?</li>
                        <li>How does the attitude of the company toward mental health in the highest number of employees having mental disorder country ?</li>
                        <li>What are the strongest predictors of mental health illness or certain attitudes towards mental health in the workplace ?</li>
                    </ul>
                    <h1 class='font-big'>Feature</h1>
                        <p class="left">This dataset contains the following data :</p>
                    <ol class="justify-numbering">
                        <li>Timestamp</li>
                        <li>Age</li>
                        <li>Gender</li>
                        <li>Country</li>
                        <li>State : <i>If you live in the United States, which state or territory do you live in?</i></li>
                        <li>self_employed : <i>Are you self-employed?</i></li>
                        <li>family_history : <i>Do you have a family history of mental illness?</i></li>
                        <li>treatment : <i>Have you sought treatment for a mental health condition?</i></li>
                        <li>work_interfere : <i>If you have a mental health condition, do you feel that it interferes with your work?</i></li>
                        <li>no_employees : <i>How many employees does your company or organization have ?</i></li>
                        <li>remote_work : <i>Do you work remotely (outside of an office) at least 50% of the time ?</i></li>
                        <li>tech_company : <i>Is your employer primarily a tech company/organization ?</i></li>
                        <li>benefits : <i>Does your employer provide mental health benefits ?</i></li>
                        <li>care_options : <i>Do you know the options for mental health care your employer provides ?</i></li>
                        <li>wellness_program : <i>Has your employer ever discussed mental health as part of an employee wellness program ?</i></li>
                        <li>seek_help : <i>Does your employer provide resources to learn more about mental health issues and how to seek help ?</i></li>
                        <li>anonymity : <i>Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources ?</i></li>
                        <li>leave : <i>How easy is it for you to take medical leave for a mental health condition ?</i></li>
                        <li>mental_health_consequence : <i>Do you think that discussing a mental health issue with your employer would have negative consequences ?</i></li>
                        <li>phys_health_consequence : <i>Do you think that discussing a physical health issue with your employer would have negative consequences ?</i></li>
                        <li>coworkers : <i>Would you be willing to discuss a mental health issue with your coworkers ?</i></li>
                        <li>supervisor : <i>Would you be willing to discuss a mental health issue with your direct supervisor(s) ?</i></li>
                        <li>mental_health_interview : <i>Would you bring up a mental health issue with a potential employer in an interview ?</i></li>
                        <li>phys_health_interview : <i>Would you bring up a physical health issue with a potential employer in an interview ?</i></li>
                        <li>mental_vs_physical : <i>Do you feel that your employer takes mental health as seriously as physical health ?</i></li>
                        <li>obs_consequence : <i>Have you heard of or observed negative consequences for coworkers with mental health conditions in your workplace ?</i></li>
                        <li>comments : <i>Any additional notes or comments ?</i></li>
                    </ul>
                </body>
                 """
prep_temp = """
            <div style="background-color:#0e0f3f;padding:1px;border-radius:25px">
		    <h2 style="color:white;font-family:calibri;text-align:center;">DATA PREPROCESSING AND CLEANSING </h2>
            </div>
            """
eda_temp = """
            <div style="background-color:#0e0f3f;padding:1px;border-radius:25px">
		    <h2 style="color:white;font-family:calibri;text-align:center;">EXPLORATORY DATA ANALYSIS (EDA) </h2>
            </div>
            """
ml_temp = """
            <div style="background-color:#0e0f3f;padding:1px;border-radius:25px">
		    <h2 style="color:white;font-family:calibri;text-align:center;">MACHINE LEARNING</h2>
            </div>
            """
def main_section():
     #st.write(home_temp,unsafe_allow_html=True)
     st.write(home2_temp,unsafe_allow_html=True)

     # Create a container to align images side by side
     st.image("Image/logo1.png",  use_column_width=False)
     #images = {
          #"Andi Muhammad Yusuf": "/Data Privasi/laptop/Python/Final Project/image/Andi.jpg"
     #}

     
     #st.sidebar.image(images["Andi Muhammad Yusuf"], width=90,use_column_width=False)
     st.sidebar.write('Created by. Andi Muhammad Yusuf')
     

def main():
    st.set_page_config(page_title="Data Science Bootcamp Final Project", page_icon=":chart_with_upwards_trend:",layout='wide')
    st.sidebar.title("Navigation")
    section = st.sidebar.radio("Go to Menu", ("Home", "About Project","Data Preprocessing & Cleansing","Exploratory Data Analysis", "Machine Learning"))

    if section == "Home":
        main_section()
    elif section == "About Project":
        st.write(about_temp,unsafe_allow_html=True)
        st.write(desc_about_temp,unsafe_allow_html=True)
    elif section == "Data Preprocessing & Cleansing":
        st.write(prep_temp,unsafe_allow_html=True)
        ds_dataprep_clean_app()
    elif section == "Exploratory Data Analysis":
        st.write(eda_temp,unsafe_allow_html=True)
        ds_eda_app()
    elif section == "Machine Learning":
        st.write(ml_temp,unsafe_allow_html=True)
        ds_ml_app()


if __name__ == "__main__":
    main()
