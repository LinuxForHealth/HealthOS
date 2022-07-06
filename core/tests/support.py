import os
from os.path import dirname

# base resource directory for "file fixtures" for tests and sample applications
resources_directory = os.path.join(
    dirname(dirname(os.path.realpath(__file__))), "resources"
)
