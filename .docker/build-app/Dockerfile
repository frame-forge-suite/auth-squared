##############################################################################################
# IMPORTANT NOTE: This file is used to build the application image
# The context for the build is the root of the repository
##############################################################################################

# ------------------------------------------------------------------------------------------ #
# Pre-stage: Arguments
# ------------------------------------------------------------------------------------------ #

# * Set the default arguments
ARG PRJ_NAME=auth-squared
ARG RSC_DIR=resources
ARG POETRY_VERSION=1.8.2
ARG UID=1000
ARG GID=${UID}
ARG USR_NAME=app-runner
ARG GRP_NAME=${USR_NAME}
ARG USR_HOME=/home/${USR_NAME}
ARG USR_PWD=P455w0rd

# ------------------------------------------------------------------------------------------ #
# End of Pre-stage: Arguments
# ------------------------------------------------------------------------------------------ #
#
##############################################################################################
#
# ------------------------------------------------------------------------------------------ #
# Stage 01 - Base
# This stage is used to install the system dependencies and add create the user
# ------------------------------------------------------------------------------------------ #
FROM python:3.12.0-bullseye AS base

# * Re declare arguments
ARG POETRY_VERSION
ARG UID
ARG GID
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME
ARG USR_PWD

# * Install the system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends && \
    apt-get install -y sudo && \
    apt autoclean && \
    apt autoremove && \
    rm -rf /var/lib/apt/lists/*

# * Create a user and group to run the application
RUN groupadd -g ${GID} ${GRP_NAME} && \
    useradd -rm -d ${USR_HOME} -s /bin/bash -u ${UID} -g ${GRP_NAME} ${USR_NAME} && \
    echo "${USR_PWD}\n${USR_PWD}\n" | passwd ${USR_NAME} && \
    sudo adduser ${USR_NAME} sudo

# * Update Path
ENV PATH="${USR_HOME}/.local/bin:$PATH"

# * Use the new user and install poetry
USER ${USR_NAME}

# * Install poetry in order to manage the dependencies
RUN pip install --upgrade pip && \
    pip install poetry==${POETRY_VERSION} && \
    poetry config virtualenvs.options.always-copy true && \
    poetry config virtualenvs.prompt "venv" && \
    poetry config virtualenvs.in-project true

# * Import entrypoints
COPY --chown=${USR_NAME}:${GRP_NAME} .docker/build-app/entrypoints/docker-entrypoint* /bin/
RUN chmod +x /bin/docker-entrypoint*

# ------------------------------------------------------------------------------------------ #
# End of Stage 01 - Base
# ------------------------------------------------------------------------------------------ #
#
##############################################################################################
#
# ------------------------------------------------------------------------------------------ #
# Stage DEV - Development Build
# This stage is used to run the application in development
# ------------------------------------------------------------------------------------------ #
FROM base AS development

# * Re declare arguments
ARG RSC_DIR
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME

# * Set the user
USER ${USR_NAME}

# * Create and set the working directory
# ? No need to copy the files, as they will be in the workspace through the volume
WORKDIR ${USR_HOME}/app

# * Copy poetry files to the working directory
COPY --chown=${USR_NAME}:${GRP_NAME} ${RSC_DIR}/pyproject.toml ${RSC_DIR}/poetry.lock ${RSC_DIR}/

# * Install the dependencies
RUN cd ${RSC_DIR} &&\
    poetry install --no-root --no-interaction --no-ansi -vvv

# * Install Task (https://taskfile.dev/#/) for dev purposes
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# * Set the entrypoint for the development container
ENTRYPOINT ["docker-entrypoint-dev"]

# ------------------------------------------------------------------------------------------ #
# End of Stage DEV - Development Build
# ------------------------------------------------------------------------------------------ #
#
##############################################################################################
#
# ------------------------------------------------------------------------------------------ #
# Stage 02 - Runtime
# This stage is used to run the application in production
# ------------------------------------------------------------------------------------------ #
FROM base AS runtime

# * Re declare arguments
ARG PRJ_NAME
ARG RSC_DIR
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME

# * Set the user
USER ${USR_NAME}

# * Copy the application files
# ? Local `__pycache__` and `.pytest_cache` are not copied to the container thanks to the `.dockerignore` file
COPY --chown=${USR_NAME}:${GRP_NAME} ${RSC_DIR}/ ${USR_HOME}/app/${RSC_DIR}

# * Set the working directory
WORKDIR ${USR_HOME}/app/${RSC_DIR}

# * Install the dependencies
RUN poetry install --no-root --no-interaction --no-ansi -vvv

# * Set the entrypoint for the runtime container
ENTRYPOINT ["docker-entrypoint"]

# * Expose the port
EXPOSE 80

# ------------------------------------------------------------------------------------------ #
# End of Stage 02 - Runtime
# ------------------------------------------------------------------------------------------ #
#
##############################################################################################
#
# ------------------------------------------------------------------------------------------ #
# Default Stage
# This is the default stage used to build the image if no target is specified
# ------------------------------------------------------------------------------------------ #
FROM runtime

# ------------------------------------------------------------------------------------------ #
# End of Default Stage
# ------------------------------------------------------------------------------------------ #