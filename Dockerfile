#Base Image
FROM python:3.7

#Working Directory
WORKDIR /code

#Copy Dependencies
COPY ./code/requirements.txt .

#Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy python code to dir
COPY ./code/pipeline.py /code

#Excute on container start
CMD ["python", "./pipeline.py"]