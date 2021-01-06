FROM openwhisk/python3action:nightly

# lapack-dev is available in community repo.
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# add package build dependencies
RUN apk add --no-cache \
        g++ \
        lapack-dev \
        gfortran \
        lapack \
        openblas-dev \
        yasm \
        ffmpeg
COPY requirement.txt /
# add python packages
RUN pip install pip setuptools wheel -U
RUN pip install -r requirement.txt