##############################################################################################
# IMPORTANT NOTE: This file is used to build the application image
# The context for the build is the root of the repository
##############################################################################################

# ------------------------------------------------------------------------------------------ #
# Pre-stage: Arguments
# ------------------------------------------------------------------------------------------ #

# * Set the default arguments values
ARG PRJ_NAME=project
ARG RSC_DIR=./resources
ARG VENV_DIR=/opt/.venv
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
# Stage 00 - Base
# This stage is used to install the system dependencies and add create the user
# ------------------------------------------------------------------------------------------ #
FROM python:3.12.0-bullseye AS base

# * Re declare arguments
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

# ------------------------------------------------------------------------------------------ #
# End of Stage 00 - Base
# ------------------------------------------------------------------------------------------ #
#
##############################################################################################
#
# ------------------------------------------------------------------------------------------ #
# Stage 01 - Build
# This stage is used to build the application (for development and production)
# ------------------------------------------------------------------------------------------ #
FROM base AS build

# * Re declare arguments
ARG PRJ_NAME
ARG RSC_DIR
ARG VENV_DIR
ARG POETRY_VERSION
ARG PIP_USR
ARG PIP_PWD
ARG PIP_URL

# * Copy the poetry files to the temporary folder
COPY ${RSC_DIR}/poetry.lock ${RSC_DIR}/pyproject.toml /tmp/

# * Set the working directory to the temporary folder
WORKDIR /tmp

# * Create the virtual environment, install poetry and the dependencies
RUN python -m venv ${VENV_DIR} && \
    pip install --upgrade pip && \
    bash -c  "source ${VENV_DIR}/bin/activate" && \
    pip install poetry==${POETRY_VERSION} && \
    poetry install --no-root --no-interaction --no-ansi -vvv

# * Copy the docker entrypoints and set them executable
COPY .docker/build-app/entrypoints/docker-entrypoint* /bin/
RUN chmod +x /bin/docker-entrypoint*

# ------------------------------------------------------------------------------------------ #
# End of Stage 01 - Build
# ------------------------------------------------------------------------------------------ #
#
##############################################################################################
#
# ------------------------------------------------------------------------------------------ #
# Stage DEV - Development Build
# This stage is used to run the application in development
# ------------------------------------------------------------------------------------------ #
FROM build AS development

# * Re declare arguments
ARG VENV_DIR
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME

# * Update Path
ENV PATH="${VENV_DIR}/bin:$PATH"
ENV PATH="${USR_HOME}/.local/bin:$PATH"

# * Set the user
USER ${USR_NAME}

# * Create and set the working directory
# ? No need to copy the files, as they will be in the workspace through the volume
RUN mkdir -p ${USR_HOME}/workspace
WORKDIR ${USR_HOME}/workspace

# * Copy the venv and the docker entrypoints from the build stage
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} ${VENV_DIR} ${VENV_DIR}
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} /bin/docker-entrypoint* /bin/

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
ARG VENV_DIR
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME

# * Update Path
ENV PATH="${VENV_DIR}/bin:$PATH"
ENV PATH="${USR_HOME}/.local/bin:$PATH"

# * Set the user
USER ${USR_NAME}

# * Copy the application files
# ? Local `__pycache__` and `.pytest_cache` are not copied to the container thanks to the `.dockerignore` file
COPY --chown=${USR_NAME}:${GRP_NAME} ${RSC_DIR}/ ${USR_HOME}/apps/${PRJ_NAME}/

# * Copy the venv and the docker entrypoints from the build stage
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} ${VENV_DIR} ${VENV_DIR}
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} /bin/docker-entrypoint* /bin/

# * Set the working directory
WORKDIR ${USR_HOME}/apps/${PRJ_NAME}/

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