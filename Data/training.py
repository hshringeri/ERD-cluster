import os
import numpy as np

from tflite_model_maker.config import QuantizationConfig
from tflite_model_maker.config import ExportFormat
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

from tflite_support import metadata

import tensorflow as tf
assert tf.__version__.startswith('2')


tf.get_logger().setLevel('ERROR')
from absl import logging
logging.set_verbosity(logging.ERROR)

classes = ['entity', 'weakentity', 'relationship', 'weakrelationship', 'attribute']
train_data = object_detector.DataLoader.from_pascal_voc(
    'Data\TrainingData\Images',
    'Data\TrainingData\Annotations',
    label_map={1: 'entity', 2: 'weakentity', 3: 'relationship', 4: 'weakrelationship', 5: 'attribute'}
)

val_data = object_detector.DataLoader.from_pascal_voc(
    'Data\ValidationData\Images',
    'Data\ValidationData\Annotations',
    label_map={1: 'entity', 2: 'weakentity', 3: 'relationship', 4: 'weakrelationship', 5: 'attribute'}
)

test_data = object_detector.DataLoader.from_pascal_voc(
    'Data\TestingData\Images',
    'Data\TestingData\Annotations',
    label_map={1: 'entity', 2: 'weakentity', 3: 'relationship', 4: 'weakrelationship', 5: 'attribute'}
)

spec = model_spec.get('efficientdet_lite4') # can use 0-4, 0 fast but inprecise

model = object_detector.create(train_data, model_spec=spec, batch_size=20, train_whole_model=True, epochs=150, validation_data=val_data)

model.evaluate(test_data)

model.export(export_dir='Data\Models')
