FROM openwhisk/python3action:nightly

# lapack-dev is available in community repo.
RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

# add package build dependencies
RUN apk add --no-cache \
        g++ \
        lapack-dev \
        gfortran \
        lapack \
        openblas-dev 

# ENV PYTHON_PACKAGES="\
#     numpy \
#     matplotlib \
#     scikit-learn \
# " 

# RUN apk add --no-cache --virtual build-dependencies python --update py-pip \
#     && apk add --virtual build-runtime \
#     build-base python-dev openblas-dev freetype-dev pkgconfig gfortran \
#     && ln -s /usr/include/locale.h /usr/include/xlocale.h \
#     && pip install --upgrade pip \
#     && pip install --no-cache-dir $PYTHON_PACKAGES \
#     && apk del build-runtime \
#     && apk add --no-cache --virtual build-dependencies $PACKAGES \
#     && rm -rf /var/cache/apk/*

# add python packages
RUN pip install pip setuptools wheel -U
RUN pip install numpy
# RUN pip install pandas

RUN pip install scikit-learn
# RUN pip install scipy