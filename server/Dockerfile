FROM jjanzic/docker-python3-opencv

WORKDIR /code

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1


EXPOSE 50051

COPY ./app.py /code/
COPY ./files /files/

COPY ./camera_pb2_grpc.py /code/
COPY ./camera_pb2.py /code/
COPY ./camera_pb2.pyi /code/

RUN python -m pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

# ENTRYPOINT ["python3"] 
CMD ["python", "/code/app.py"]
