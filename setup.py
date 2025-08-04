from setuptools import setup, find_packages

setup(
    name="advisor_copilot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask==3.0.0",
        "google-cloud-bigquery==3.12.0",
        "google-cloud-aiplatform==1.36.0",
        "python-dotenv==1.0.0",
        "gunicorn==21.2.0"
    ],
)
