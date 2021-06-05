import os
import site
import shutil

def fix_bokeh_dark_mode():
    SITE_PACKAGES_DIR = site.getsitepackages()[0]
    BOKEH_SOURCE = 'bokeh_chart.py'
    BOKEH_DEST = os.path.join(SITE_PACKAGES_DIR, 'streamlit', 'elements', 'bokeh_chart.py')
    shutil.copy(BOKEH_SOURCE, BOKEH_DEST)

fix_bokeh_dark_mode()

import streamlit as st
from model.model import Pipeline
from bokeh.themes import built_in_themes
from spectrum_plotter import plot_bokeh_graph
from file_processor import extract_spectra_from_files
from state_manager import reset_current_file, get_next_file, get_previous_file

st.title('GalacTech')
home = st.sidebar.button('Dashboard')
how_to_use = st.sidebar.button('How to use')
files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True)

if how_to_use:
    st.header('How To Use')
    st.text('1. Acquire spectra of astronomical entities in FITS or CSV format.')
    st.text('2. Upload the files one by one or all at once.')
    st.text('3. View the results and play around with the interactive charts.')
    st.text('4. Download results as a CSV.')
    st.stop()

@st.cache(hash_funcs={Pipeline: lambda _: ''})
def load_pipeline():
    return Pipeline.initialize()

pipeline = load_pipeline()

@st.cache
def get_predictions(filenames, spectra):
    # Wrapper for Pipeline.process()
    return pipeline.process(filenames, spectra)

@st.cache
def reset_state_if_new_uploads(files):
    reset_current_file(len(files))

filenames = list(map(lambda file: file.name, files))
reset_state_if_new_uploads(files)

if not files:
    st.stop()

spectra = extract_spectra_from_files(files)
predictions, dataframe, csv = get_predictions(filenames, spectra)

col1, col2, col3 = st.beta_columns([0.55, 1, 0.2])

index = 0

if col1.button('Previous'):
    index = get_previous_file()

if col3.button('Next'):
    index = get_next_file()

col2.subheader(files[index].name)

st.bokeh_chart(plot_bokeh_graph(spectra[index]), use_container_width=True, theme=built_in_themes['dark_minimal'])

_, col2, _ = st.beta_columns([1.2, 1, 0.4])
col2.header(predictions['entity'][index])

if predictions['entity'][index] == 'QSO':
    st.warning('Our QSO classifer is a bit flimsy.')

if predictions['entity'][index] == 'Galaxy':
    col1, _, col3 = st.beta_columns([1, 0.8, 0.6])
    col1.subheader(f'Age: {predictions["age"][index]}')
    col3.subheader(f'Metallicity: {predictions["metallicity"][index]}')

st.table(dataframe)

href = f'<a href="data:file/csv;base64,{csv}" download="results.csv" target="_blank">Download as CSV</a>'
st.markdown(href, unsafe_allow_html=True)
