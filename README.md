# gRPC-Yolov8-Camera

## How to run:

    - `docker-compose up --build`

## Services:

    - Camera

    - YOLOv8 (detection)



## Run:

- camera_webapp
    - `python camera_webapp/app.py`

- postgres
    - docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres:alpine
    - docker exec -it some-postgres
    - ```
        psql -U postgres
        ```
    - 