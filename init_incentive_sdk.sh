#!/bin/bash

mkdir -p incentive-engine-sdk/{incentive,examples,tests}

touch incentive-engine-sdk/incentive/__init__.py
touch incentive-engine-sdk/incentive/client.py
touch incentive-engine-sdk/incentive/config.py
touch incentive-engine-sdk/incentive/exceptions.py
touch incentive-engine-sdk/incentive/utils.py

touch incentive-engine-sdk/examples/reward_user.py
touch incentive-engine-sdk/tests/test_client.py

touch incentive-engine-sdk/.env.example
touch incentive-engine-sdk/.gitignore
touch incentive-engine-sdk/LICENSE
touch incentive-engine-sdk/pyproject.toml
touch incentive-engine-sdk/setup.cfg
touch incentive-engine-sdk/README.md

echo "✅ SDK scaffold created at incentive-engine-sdk/"



