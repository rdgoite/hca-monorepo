FROM humancellatlas/upload-validator-base-alpine

RUN mkdir -p /opt/fastq-validator/common /opt/fastq-validator/validator
COPY common/*.py /opt/fastq-validator/common/
COPY validator/*.py /opt/fastq-validator/validator/
COPY script/fastq.py /opt/fastq-validator/

COPY validator.sh /validator
RUN chmod +x /validator