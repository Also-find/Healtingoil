import pandas as pd
import joblib
import streamlit as st
import altair as alt

# Load MLP model
model_mlp = joblib.load('ann.pkl')

def result(df):
    predicted_columns = ['Insulation','Temperature','Num_Occupants','Avg_Age','Home_Size']
    x1= df[predicted_columns]


    # Linear Regression
    mpl_predict = model_mlp.predict(x1)
    mpl_predict = pd.DataFrame({'Prediction_HeatingOil':mpl_predict}).round(2)
    mpl_predict = pd.concat([df,mpl_predict], sort=False, axis=1)

    st.header('Raw data')
    st.write(mpl_predict)
    # st.download_button(label='Download Data', data=mpl_predict)
    
    scatter_plots = []
    for feature in predicted_columns:
        scatter_plot = alt.Chart(mpl_predict).mark_circle().encode(
            x=alt.X(feature, title=feature),
            y=alt.Y('Prediction_HeatingOil', title='Heating Oil'),
            tooltip=[feature, 'Prediction_HeatingOil']
        ).properties(
            width=200,
            height=200
        )
        
        scatter_plots.append(scatter_plot)

    # print(scatter_plots)
    # Combine scatter plots
    # combined_plots = alt.vconcat(*scatter_plots)
    st.header('Scatterplot')
    col1, col2, = st.columns(2)
    col3, col4, = st.columns(2)
    
    col1.write(scatter_plots[1])
    col2.write(scatter_plots[2])
    col3.write(scatter_plots[3])
    col4.write(scatter_plots[4])

st.set_page_config(
    page_title="Prediction Oil Heating", page_icon="🖼️", initial_sidebar_state="collapsed"
)
st.markdown(
    """
    <style>
    .appview-container {
        background: linear-gradient(to top, #ffdebf, #FFF);
    }

    .background-container {
        position: relative;
        width: 100%;
        height: 300px; /* Adjust height as needed */
        background: url('https://img.freepik.com/free-vector/oil-industry-flat-banner_98292-6928.jpg?w=996&t=st=1707738259~exp=1707738859~hmac=133a76dc18a875a67a2d5c3d77ff86b717dfaa61b85cc8aa5bb905dc24cbba01');
        background-size: cover;
        background-position: center center;
        color: white;
        margin-bottom: 20px;
    }
    .layer {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5); /* Adjust opacity as needed */
    }
    .content {
        position: relative;
        z-index: 1;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }

    .content h1 {
    color: white;
    }
    </style>
    <div class="background-container">
        <div class="layer"></div>
        <div class="content">
            <h1>Prediksi Penggunaan Heating Oil Untuk Kebutuhanmu Dirumah</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

ex1, ex2 = st.columns(2)
data = []
with ex1.expander("Upload Data Source (.csv)"):
    uploaded_file = st.file_uploader("Choose File")

with ex2.expander("Form Input"):
    with st.form("my_form"):
        Insulation = st.slider(
            "Insulasi / Kelembapan",
            10,
            100,
            key="Insulation",
        )
        Temperature = st.slider(
            "Suhu Ruangan",
            10,
            100,
            key="Temperature",
        )
        Num_Occupants = st.slider(
            "Okupansi Rumah",
            10,
            100,
            key="Num_Occupants",
        )
        Avg_Age = st.slider(
            "Rata rata umur penghuni rumah",
            10,
            100,
            key="Avg_Age",
        )
        Home_Size = st.slider(
            "Luas Rumah",
            10,
            100,
            key="Home_Size",
        )

        submitted = st.form_submit_button("Prediksi")
        if submitted:
            uploaded_file = None
            # st.write("slider", slider_val, "checkbox", checkbox_val)
            data.append({'Insulation': Insulation, 'Temperature': Temperature, 'Num_Occupants': Num_Occupants, 'Avg_Age' : Avg_Age, 'Home_Size' : Home_Size})

if uploaded_file is not None:
    df_dataset = pd.read_csv(uploaded_file)
    df=pd.DataFrame(df_dataset)
    result(df)
elif len(data) > 0:
    df=pd.DataFrame(data)
    result(df)