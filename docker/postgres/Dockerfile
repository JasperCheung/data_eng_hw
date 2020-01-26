FROM postgres:11.3 AS postgres

ENV POSTGRES_PASSWORD=password

COPY init.sql /docker-entrypoint-initdb.d/
