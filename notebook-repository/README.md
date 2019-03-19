> sudo docker network create repo

> sudo docker run --rm --net repo -p 8000:8000 -p 8001:8001 \
>     -v /Users/tabor/PycharmProjects/notebook-docker/genepattern-repository/jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py \
>     -v /var/run/docker.sock:/var/run/docker.sock 4751e6ca49f3