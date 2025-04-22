# incentive/config.py

import os

# Base URL for the Incentive Engine API. Override by setting the environment variable.
API_BASE_URL = os.getenv("INCENTIVE_API_BASE_URL", "https://api.incentiveengine.io")
