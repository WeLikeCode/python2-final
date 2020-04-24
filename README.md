# python2-final
Final python 2 - Python 2.7.18 in a docker alpine version; Based on  jfloff / alpine-python 

## Docker 
Alpine Python 2.7.18 - the last version of Python 2. We will miss you Python 2 ..

#### Pip Dependencies
Pip dependencies can be installed by the `-p` switch, or a `requirements.txt` file.

If the file is at `/requirements.txt` it will be automatically read for dependencies. If not, use the `-P` or `-r` switch to specify a file.
```shell
# This runs interactive Python with 'simplejson' and 'requests' installed
docker run --rm -ti jfloff/alpine-python:2.7-slim -p simplejson -p requests

# Don't forget to add '--' after your dependencies to run a custom command:
docker run --rm -ti jfloff/alpine-python:2.7-slim -p simplejson -p requests -- python hello.py

# This accomplishes the same thing by mounting a requirements.txt in:
echo 'simplejson' > requirements.txt
echo 'requests' > requirements.txt
docker run --rm -ti \
  -v requirements.txt:/requirements.txt \
  jfloff/alpine-python:2.7-slim python hello.py

# This does too, but with the file somewhere else:
echo 'simplejson requests' > myapp/requirements.txt
docker run --rm -ti \
  -v myapp:/usr/src/app \
  jfloff/alpine-python:2.7-slim \
    -r /usr/src/app/requirements.txt \
    -- python /usr/src/app/hello.py
```

#### Run-Time Dependencies
Alpine package dependencies can be installed by the `-a` switch, or an `apk-requirements.txt` file.

If the file is at `/apk-requirements.txt` it will be automatically read for dependencies. If not, use the `-A` switch to specify a file.

You can also try installing some Python modules via this method, but it is possible for Pip to interfere if it detects a version problem.
```shell
# Unknown why you'd need to do this, but you can!
docker run --rm -ti jfloff/alpine-python:2.7-slim -a openssl -- python hello.py

# This installs libxml2 module faster than via Pip, but then Pip reinstalls it because Ajenti's dependencies make it think it's the wrong version.
docker run --rm -ti jfloff/alpine-python:2.7-slim -a py-libxml2 -p ajenti
```

#### Build-Time Dependencies
Build-time Alpine package dependencies (such as compile headers) can be installed by the `-b` switch, or a `build-requirements.txt` file. They will be removed after the dependencies are installed to save space.

If the file is at `/build-requirements.txt` it will be automatically read for dependencies. If not, use the `-B` switch to specify a file.

`build-base`, `linux-headers` and `python-dev` are always build dependencies, you don't need to include them.
```shell
docker run --rm -ti jfloff/alpine-python:2.7-slim \
  -p gevent \
  -p libxml2 \
  -b libxslt-dev \
  -b libxml-dev \
  -- python hello.py
```

#### Creating Images
Similar to the onbuild images, dependencies can be baked into a new image by using a custom `Dockerfile`, e.g:
```dockerfile
FROM jfloff/alpine-python:2.7-slim
RUN /entrypoint.sh \
  -p ajenti-panel \
  -p ajenti.plugin.dashboard \
  -p ajenti.plugin.settings \
  -p ajenti.plugin.plugins \
  -b libxml2-dev \
  -b libxslt-dev \
  -b libffi-dev \
  -b openssl-dev \
&& echo
CMD ["ajenti-panel"]
# you won't be able to add more dependencies later though-- see 'Debugging'
```

#### Debugging
The `/entrypoint.sh` script that manages dependencies in the slim images creates an empty file, `/requirements.installed`, telling the script not to install any dependencies after the container's first run. Removing this file will allow the script to work again if it is needed.

You can use the `-x` flag to see everything the `/entrypoint.sh` script is doing.

You can also access `bash` inside the container:
```shell
docker run --rm -ti jfloff/alpine-python:2.7-slim bash
```

#### Additional Arguments

`-q`: silences output from `/entrypoint.sh`
`-x`: turns on Bash debugging, making the output very verbose.

## Ecosystem

These are some of the images that use `jfloff/alpine-python` as base image. *If you have another image that uses this as base image, please submit an issue or PR for it to be added. Image has to be published on Docker Hub.*

- **[jfloff/alscipy](https://github.com/jfloff/docker-alscipy)** [![Docker Stars](https://img.shields.io/docker/stars/jfloff/alscipy.svg)][alscipy-hub] [![Docker Pulls](https://img.shields.io/docker/pulls/jfloff/alscipy.svg)][alscipy-hub] : image with common packages for Science in Alpine Python.
- **[jfloff/pywfm](https://github.com/jfloff/docker-pywfm)** [![Docker Stars](https://img.shields.io/docker/stars/jfloff/pywfm.svg)][pywfm-hub] [![Docker Pulls](https://img.shields.io/docker/pulls/jfloff/pywfm.svg)][pywfm-hub] : image from the python wrapper for Steffen Rendle's factorization machines library libFM.
- **[bismuthfoundation/Bismuth-Docker](https://github.com/bismuthfoundation/Bismuth-Docker)** [![Docker Stars](https://img.shields.io/docker/stars/eggdrasyl/bismuth-node.svg)][busmuth-hub] [![Docker Pulls](https://img.shields.io/docker/pulls/eggdrasyl/bismuth-node.svg)][busmuth-hub] : node and associated services, from scratch crypto-currency with Python codebase.

[alscipy-hub]: https://hub.docker.com/r/jfloff/alscipy/
[pywfm-hub]: https://hub.docker.com/r/jfloff/pywfm/
[busmuth-hub]: https://hub.docker.com/r/eggdrasyl/bismuth-node/


## Contribution
Feel free to contribute with whatever you feel like this image is missing. There is also some changes that happen often like, updating Alpine or Python versions. Do not forget that this repo folders mirror **Python** version and **_not_** Alpine versions.
