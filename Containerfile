# Docker/Podman/OCI container build specfication file.
#
# References:
# - [Gist](https://gist.github.com/gautada/bd71914073b8e3a89ad13f0320b33010)
# - [Buildah Containerfile](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/building_running_and_managing_containers/assembly_building-container-images-with-buildah_building-running-and-managing-containers#proc_building-an-image-from-a-containerfile-with-buildah_assembly_building-container-images-with-buildah)
# - [Dockerfile](https://docs.docker.com/engine/reference/builder/)

ARG ALPINE_VERSION=3.17.0

# ╭――――――――――――――――-------------------------------------------------------――╮
# │                                                                         │
# │ STAGE 2: container                                                      │
# │                                                                         │
# ╰―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――╯
FROM gautada/alpine:$ALPINE_VERSION

# ╭――――――――――――――――――――╮
# │ METADATA           │
# ╰――――――――――――――――――――╯
LABEL source="https://github.com/gautada/dynip-container.git"
LABEL maintainer="Adam Gautier <adam@gautier.org>"
LABEL description="This is a dynamic ip client for Hover.com"

# ╭――――――――――――――――――――╮
# │ STANDARD CONFIG    │
# ╰――――――――――――――――――――╯

# USER:
ARG USER=dyndns

ARG UID=1001
ARG GID=1001
RUN /usr/sbin/addgroup -g $GID $USER \
 && /usr/sbin/adduser -D -G $USER -s /bin/ash -u $UID $USER \
 && /usr/sbin/usermod -aG wheel $USER \
 && /bin/echo "$USER:$USER" | chpasswd

# PRIVILEGE:
# COPY wheel  /etc/container/wheel

# BACKUP: This container's state is maintained in configuration files'
COPY backup /etc/container/backup

# ENTRYPOINT: No entrypoint this container just uses crond
RUN rm -v /etc/container/entrypoint
COPY entrypoint /etc/container/entrypoint

# FOLDERS
RUN /bin/chown -R $USER:$USER /mnt/volumes/container \
 && /bin/chown -R $USER:$USER /mnt/volumes/backup \
 && /bin/chown -R $USER:$USER /var/backup \
 && /bin/chown -R $USER:$USER /tmp/backup


# ╭――――――――――――――――――――╮
# │ APPLICATION        │
# ╰――――――――――――――――――――╯
RUN apk add --no-cache --update python3
RUN apk add --no-cache py3-pip py3-requests py3-yaml
RUN pip install fastapi
RUN pip install "uvicorn[standard]"

RUN /bin/ln -fsv /mnt/volumes/container/dyndns.yml /mnt/volumes/configmaps/dyndns.yml
RUN /bin/ln -fsv /mnt/volumes/configmaps/dyndns.yml /etc/container/dyndns.yml

COPY client.py /home/$USER/client.py
COPY server.py /home/$USER/server.py
COPY dyndns.py /home/$USER/dyndns.py
COPY dyndns_plugin.py /home/$USER/dyndns_plugin.py
COPY hover_plugin.py /home/$USER/hover_plugin.py
COPY dyndns-update-ip /usr/bin/dyndns-update-ip
RUN /bin/ln -fsv /usr/bin/dyndns-update-ip /etc/periodic/15min/dyndns-update-ip

# COPY check.py /home/$USER/check.py


# ╭――――――――――――――――――――╮
# │ CONTAINER          │
# ╰――――――――――――――――――――╯
USER $USER
VOLUME /mnt/volumes/backup
VOLUME /mnt/volumes/configmaps
VOLUME /mnt/volumes/container
# EXPOSE 8080/tcp # Container has no interface
WORKDIR /home/$USER
