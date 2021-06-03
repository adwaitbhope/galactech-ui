import streamlit as st
from model.model import Pipeline
from spectrum_plotter import get_plots
from state_manager import reset_current_file, get_next_file, get_previous_file
from file_processor import extract_spectra_from_files

st.title('GalacTech')

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

files = st.sidebar.file_uploader("Choose a file", accept_multiple_files=True)

filenames = list(map(lambda file: file.name, files))

reset_state_if_new_uploads(files)

if files:

    spectra = extract_spectra_from_files(files)

    plots = get_plots(spectra)

    predictions, dataframe = get_predictions(filenames, spectra)

    col1, col2, col3 = st.beta_columns([0.55, 1, 0.55])

    index = 0
    
    if col1.button('Previous'):

        index = get_previous_file()

    if col3.button('Next'):

        index = get_next_file()

    col2.subheader(files[index].name)

    st.write(plots[index])

    st.dataframe(dataframe)

    # if spectra:
    #     st.text(spectra)
