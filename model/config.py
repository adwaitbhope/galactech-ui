import os

_MODELS_DIR = os.path.join(os.getcwd(), 'model', 'models')

# GALAXY_CLASSIFIER = os.path.join(_MODELS_DIR, 'Galaxy_model.joblib')
# STAR_CLASSIFIER = os.path.join(_MODELS_DIR, 'Star_model.joblib')
# QSO_CLASSIFIER = os.path.join(_MODELS_DIR, 'QSO_model.joblib')
# ENTITY_CLASSIFICATION_SCALER = os.path.join(_MODELS_DIR, 'scaler.joblib')

ENTITY_CLASSIFIER_ARCH = os.path.join(_MODELS_DIR, 'entity_classifier', 'model_architecture.joblib')
ENTITY_CLASSIFIER_MODEL = os.path.join(_MODELS_DIR, 'entity_classifier', 'weights-00438-0.1345.hdf5')

REGRESSION_MODEL = os.path.join(_MODELS_DIR, 'regressor', 'weights-00996-0.1812.hdf5')
