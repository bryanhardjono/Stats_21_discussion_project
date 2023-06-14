import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import io
import numpy as np

web_apps = st.sidebar.selectbox("Select Web Apps",
                                ("Exploratory Data Analysis", "Distributions"))


if web_apps == "Exploratory Data Analysis":

  uploaded_file = st.sidebar.file_uploader("Choose a file")

  if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    df = pd.read_csv(uploaded_file)
    show_df = st.checkbox("Show Data Frame", key="disabled")

    if show_df:
      st.write(df)
    number_rows = len(df)
    number_columns = len(df)

    # Count of categorical, numerical, and boolean variables
    categorical_var = len(df.select_dtypes(include='object').columns)
    numerical_var = len(df.select_dtypes(include=['int', 'float']).columns)
    bool_var = len(df.select_dtypes(include='bool').columns)

    # Display the statistics
    st.write(f"Number of rows: {number_rows}")
    st.write(f"Number of columns: {number_columns}")
    st.write(f"Number of categorical variables: {categorical_var}")
    st.write(f"Number of numerical variables: {numerical_var}")
    st.write(f"Number of boolean variables: {bool_var}")
    column_type = st.sidebar.selectbox('Select Data Type',
                                       ("Numerical", "Categorical", "Bool", "Date"))
    
    

    if column_type == "Numerical":
      numerical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['int64', 'float64']).columns)

      # histogram
      choose_color = st.color_picker('Pick a Color', "#69b3a2")
      choose_opacity = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.0, step=0.05)

      hist_bins = st.slider('Number of bins', min_value=5,
                            max_value=150, value=30)
      hist_title = st.text_input('Set Title', 'Histogram')
      hist_xtitle = st.text_input('Set x-axis Title', numerical_column)

      fig, ax = plt.subplots()
      ax.hist(df[numerical_column], bins=hist_bins,
              edgecolor="black", color=choose_color, alpha=choose_opacity)
      ax.set_title(hist_title)
      ax.set_xlabel(hist_xtitle)
      ax.set_ylabel('Count')

      st.pyplot(fig)
      filename = "plot.png"
      fig.savefig(filename,dpi = 300)

      # Display the download button
      with open("plot.png", "rb") as file:
        btn = st.download_button(
            label="Download image",
            data=file,
            file_name="flower.png",
            mime="image/png"
        )

      five_num_summary = df[numerical_column].describe().loc[['min', '25%', '50%', '75%', 'max']]
      st.write(five_num_summary)

    if column_type == "Categorical":
      categorical_column = st.sidebar.selectbox(
          'Select a Column', df.select_dtypes(include=['object']).columns)
      df2 = df
      category_counts = df2[categorical_column].value_counts()

      choose_color2 = st.color_picker('Choose a Color', "#6990B3")
      choose_opacity2 = st.slider(
          'Color Opacity', min_value=0.0, max_value=1.5, step=0.1)

      fig, ax = plt.subplots()
      plt.bar(category_counts.index, category_counts.values,
               color=choose_color2, alpha=choose_opacity2)

      st.pyplot(fig)

      category_proportions = category_counts / len(category_counts)
      category_table = pd.DataFrame({'Category': category_proportions.index, 'Proportion': category_proportions.values})
      st.write(category_table)