# Deploy using Docker

## Build a Docker image
The docker build command builds an image from a Dockerfile . Run the following command from the app/ directory on your server to build the image:
```
docker build -t streamlit .
```

The -t flag is used to tag the image. Here, we have tagged the image streamlit. If you run:

```
docker images
```

You should see a streamlit image under the REPOSITORY column. For example:

```
REPOSITORY   TAG       IMAGE ID       CREATED              SIZE
streamlit    latest    70b0759a094d   About a minute ago   1.3GB
```

## Run the Docker container
Now that you have built the image, you can run the container by executing:

```
docker run -p 8501:8501 streamlit
```

The -p flag publishes the container’s port 8501 to your server’s 8501 port.

If all went well, you should see an output similar to the following:

```
$ docker run -p 8501:8501 streamlit

  You can now view your Streamlit app in your browser.

  URL: http://0.0.0.0:8501
```
