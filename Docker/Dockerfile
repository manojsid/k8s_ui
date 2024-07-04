# Use the official Ubuntu base image
FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir /app
# Update the package lists and install necessary tools
RUN apt-get update && \
    apt-get install -y \
    curl \
    python3 \
    python3-pip \
    unzip \
    groff \
    less \
    && rm -rf /var/lib/apt/lists/*


# Install the AWS CLI
RUN curl "https://d1vvhvl2y92vvt.cloudfront.net/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl


RUN aws --version && kubectl version --client

RUN mkdir ~/.kube && touch ~/.kube/config

RUN aws configure --profile read-only-eks set aws_access_key_id KEY && \
    aws configure --profile read-only-eks set aws_secret_access_key KEY && \
    aws configure --profile read-only-eks set region us-east-1

#RUN aws eks update-kubeconfig --name dev-new --region us-east-1 --profile read-only-eks

WORKDIR /app/
ADD app/ /app/
# RUN chmod +x /app/entrypoint.sh
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python3", "/app/app.py"]
