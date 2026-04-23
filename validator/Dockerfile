FROM python:3.11-slim

LABEL org.opencontainers.image.title="DOME Registry Schema Validator"
LABEL org.opencontainers.image.description="Validates DOME Registry entry and user JSON files against a versioned schema."
LABEL org.opencontainers.image.source="https://github.com/BioComputingUP/dome-schema"
LABEL org.opencontainers.image.licenses="CC-BY-4.0"

WORKDIR /dome-schema

# Copy schema releases and validator into the image
COPY releases/ ./releases/
COPY validator/requirements.txt ./validator/requirements.txt
COPY validator/validate.py ./validator/validate.py

RUN pip install --no-cache-dir -r ./validator/requirements.txt

# Input files are mounted at /data at runtime
VOLUME ["/data"]

ENTRYPOINT ["python", "/dome-schema/validator/validate.py"]
CMD ["--list-versions"]
