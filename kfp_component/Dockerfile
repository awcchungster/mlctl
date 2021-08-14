FROM python:3.8-slim

# Define image entry
ENTRYPOINT ["python", "./entrypoint.py"]

# Set up environment
ENV PIP_INDEX_URL="" \
    PIP_TRUSTED_HOST="" \
    PIP_EXTRA_INDEX_URL=""

COPY ./* /mlctl/
RUN pip install /mlctl

COPY kfp_component/entrypoint.py /entrypoint.py