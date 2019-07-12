FROM python:3.7-slim

# These ARGs values are passed in via the docker build command
ARG BUILD_DATE
ARG VCS_REF
ARG BRANCH=develop

# The BUILD_DATE value seem to bust the docker cache when the timestamp changes, move to
# the end
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url="https://github.com/kbaseIncubator/ui-backend-for-frontend" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.schema-version="1.0.0-rc1" \
      us.kbase.vcs-branch=$BRANCH \
      maintainer="Akiyo Marukawa amarukawa@lbl.gov"

# Set the working directory to /app
WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl -o dockerize-linux-amd64-v0.6.1.tar.gz https://raw.githubusercontent.com/kbase/dockerize/master/dockerize-linux-amd64-v0.6.1.tar.gz && \
    tar -C /usr/local/bin -xvzf dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm dockerize-linux-amd64-v0.6.1.tar.gz && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app

# RUN export PYTHONPATH="${PYTHONPATH}:/app"

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]
# CMD [ "sh", "-x", "scripts/start_server.sh"]
