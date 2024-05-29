FROM ultralytics/ultralytics:8.2.2-python

WORKDIR /plate_detection

# Without this setting, Python never prints anything out.
ENV PYTHONUNBUFFERED=1


# Copy files
COPY ./ /plate_detection/
# COPY ./app.py /code/
# COPY ./camera_pb2_grpc.py /code/
# COPY ./camera_pb2.py /code/
# COPY ./camera_pb2.pyi /code/


# Copy directories
# COPY saved_images /code/saved_images
# COPY my_yolo_v8 /code/my_yolo_v8

RUN python -m pip install --upgrade pip
# COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r /plate_detection/requirements.txt

# ENTRYPOINT ["python3"]
CMD ["python", "/plate_detection/app.py"]
# CMD ["pip", "list"]
