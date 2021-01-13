ARG KATSDPDOCKERBASE_REGISTRY=quay.io/ska-sa

FROM $KATSDPDOCKERBASE_REGISTRY/docker-base-build as build

# Switch to Python 3 environment
ENV PATH="$PATH_PYTHON3" VIRTUAL_ENV="$VIRTUAL_ENV_PYTHON3"

# Install dependencies
COPY --chown=kat:kat requirements.txt /tmp/install/requirements.txt
RUN install-requirements.py -d ~/docker-base/base-requirements.txt -r /tmp/install/requirements.txt

# Install the current package
COPY --chown=kat:kat . /tmp/install/katsdpnetboxutilities
WORKDIR /tmp/install/katsdpnetboxutilities
RUN python ./setup.py clean
RUN pip install --no-deps .
RUN pip check

#######################################################################

FROM $KATSDPDOCKERBASE_REGISTRY/docker-base-runtime
LABEL maintainer="sdpdev+katsdpnetboxutilities@ska.ac.za"

RUN mkdir -p /srv
RUN mkdir -p /tmp/netbox-cache
COPY --chown=kat:kat src/katsdpnetboxutilities/service/* /srv/

COPY --from=build --chown=kat:kat /home/kat/ve3 /home/kat/ve3
ENV LANG C.UTF-8  
# ENV LANGUAGE en_US:en  
ENV LC_ALL C.UTF-8     
ENV PATH="$PATH_PYTHON3" VIRTUAL_ENV="$VIRTUAL_ENV_PYTHON3"
WORKDIR /srv
CMD ["/home/kat/ve3/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
