##############################################################################################
# IMPORTANT NOTE: This file is used to build the application image
# The context for the build is the root of the repository
##############################################################################################

# ------------------------------------------------------------------------------------------ #
# Pre-stage: Arguments
# ------------------------------------------------------------------------------------------ #

# Set the default arguments
ARG PROJECT_NAME=auth-squared
ARG PROJECT_FOLDER=resources
ARG VENV_PARENT_DIR=/opt
ARG POETRY_VERSION=1.7.1
ARG UID=1000
ARG GID=${UID}
ARG USR_NAME=${PROJECT_NAME}
ARG GRP_NAME=${USR_NAME}
ARG USR_HOME=/home/${USR_NAME}
ARG USER_PWD=p455w0rd

# ------------------------------------------------------------------------------------------ #
# End of Pre-stage: Arguments
# ------------------------------------------------------------------------------------------ #

# ------------------------------------------------------------------------------------------ #
# Stage 01 - Build
# This stage is used to build the application (for development and production)
# ------------------------------------------------------------------------------------------ #
FROM python:3.12.0-bullseye AS build

# Re declare arguments
ARG PROJECT_NAME
ARG PROJECT_FOLDER
ARG VENV_PARENT_DIR
ARG POETRY_VERSION

# Set the environment variables
ENV VENV_PATH="${VENV_PARENT_DIR}/.venv"

# Install the system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends && \
    apt-get install -y sudo && \
    apt autoclean && \
    apt autoremove && \
    rm -rf /var/lib/apt/lists/*

# Copy the poetry files
COPY ${PROJECT_FOLDER}/poetry.lock ${PROJECT_FOLDER}/pyproject.toml ${VENV_PARENT_DIR}/

# Set the working directory
WORKDIR ${VENV_PARENT_DIR}

# Create the virtual environment, install poetry and build the application
RUN python -m venv $VENV_PATH && \
    pip install --upgrade pip && \
    bash -c  "source ${VENV_PATH}/bin/activate" && \
    pip install poetry==${POETRY_VERSION} && \
    poetry install --no-root

# Copy the docker entrypoints and set them executable
COPY .docker/${PROJECT_NAME}/entrypoints/docker-entrypoint* /bin/
RUN chmod +x /bin/docker-entrypoint*


# ------------------------------------------------------------------------------------------ #
# End of Stage 01 - Build
# ------------------------------------------------------------------------------------------ #

##############################################################################################

# ------------------------------------------------------------------------------------------ #
# Stage 02-DEV - Development Build
# This stage is used to run the application in development
# ------------------------------------------------------------------------------------------ #
FROM build AS development

# Re declare arguments
ARG VENV_PARENT_DIR
ARG UID
ARG GID
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME
ARG USER_PWD

# Set the environment variables
ENV VENV_PATH="${VENV_PARENT_DIR}/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"

# Create a user and group to run the application
RUN groupadd -g ${GID} ${GRP_NAME} && \
    useradd -rm -d ${USR_HOME} -s /bin/bash -u ${UID} -g ${GRP_NAME} ${USR_NAME} && \
    echo "${USER_PWD}\n${USER_PWD}\n" | passwd ${USR_NAME} && \
    sudo adduser ${USR_NAME} sudo

# Set the user
USER ${USR_NAME}

# Copy the whole repository to the workspace
ADD --chown=${USR_NAME}:${GRP_NAME} . ${USR_HOME}/workspace

# Set the working directory
# No need to copy the files again, as they are already in the workspace through the volume
WORKDIR ${USR_HOME}/workspace

# Copy the venv and the docker entrypoints from the build stage
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} ${VENV_PARENT_DIR}/.venv ${VENV_PARENT_DIR}/.venv
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} /bin/docker-entrypoint* /bin/

# Install Task (https://taskfile.dev/#/) for dev purposes
ENV PATH="${USR_HOME}/.local/bin:$PATH"
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin

# Set the entrypoint
ENTRYPOINT ["docker-entrypoint-dev"]

# ------------------------------------------------------------------------------------------ #
# End of Stage 02-DEV - Development Build
# ------------------------------------------------------------------------------------------ #

##############################################################################################

# ------------------------------------------------------------------------------------------ #
# Stage 02 - Runtime
# This stage is used to run the application in production
# ------------------------------------------------------------------------------------------ #
FROM python:3.12.0-bullseye AS runtime

# Re declare arguments
ARG VENV_PARENT_DIR
ARG UID
ARG GID
ARG USR_NAME
ARG GRP_NAME
ARG USR_HOME
ARG USER_PWD
ARG PROJECT_NAME
ARG PROJECT_FOLDER

# Set the environment variables
ENV VENV_PATH="${VENV_PARENT_DIR}/.venv"
ENV PATH="$VENV_PATH/bin:$PATH"

# Install the system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends && \
    apt-get install -y sudo && \
    apt autoclean && \
    apt autoremove && \
    rm -rf /var/lib/apt/lists/*

# Create a user and group to run the application
RUN groupadd -g ${GID} ${GRP_NAME} && \
    useradd -rm -d ${USR_HOME} -s /bin/bash -u ${UID} -g ${GRP_NAME} ${USR_NAME} && \
    echo "${USER_PWD}\n${USER_PWD}\n" | passwd ${USR_NAME} && \
    sudo adduser ${USR_NAME} sudo

# Copy the venv and the docker entrypoints from the build stage
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} ${VENV_PARENT_DIR}/.venv ${VENV_PARENT_DIR}/.venv
COPY --from=build --chown=${USR_NAME}:${GRP_NAME} /bin/docker-entrypoint* /bin/

# Copy the application files
COPY --chown=${USR_NAME}:${GRP_NAME} ${PROJECT_FOLDER}/ ${USR_HOME}/apps/${PROJECT_NAME}/

# Set the working directory
WORKDIR ${USR_HOME}/apps/${PROJECT_NAME}/

# Set the entrypoint
ENTRYPOINT ["docker-entrypoint"]

# Expose the port
EXPOSE 80

# ------------------------------------------------------------------------------------------ #
# End of Stage 02 - Runtime
# ------------------------------------------------------------------------------------------ #

##############################################################################################

# ------------------------------------------------------------------------------------------ #
# Default Stage
# This is the default stage used to build the image if no target is specified
# ------------------------------------------------------------------------------------------ #
FROM runtime

# ------------------------------------------------------------------------------------------ #
# End of Default Stage
# ------------------------------------------------------------------------------------------ #
