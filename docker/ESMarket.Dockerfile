FROM python:3.8

COPY ./ /app
WORKDIR app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN ls -l

CMD celery -A feed.tasks worker --loglevel=info
CMD python celery_run.py