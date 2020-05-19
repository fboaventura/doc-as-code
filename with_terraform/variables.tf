variable "host_path" {
  default = "/home/frederico/dev/projetos/pyfredericocf"
}

variable "app_env" {
  //  type = "list"
  default = [
    "DB_PASS=dbP@ssw0rd",
    "DB_SCHEMA=postgres",
    "DB_HOST=postgres",
    "DB_PORT=5432",
    "DB_NAME=fredericocf",
    "DB_USER=fredericocf",
    "DB_BACKEND=postgresql_psycopg2",
    "DEBUG=1",
    "REDIS_URL=redis://redis:6379/0",
    "REDIS_CACHE=redis://redis:6379/1",
    "CELERY_HOST=rabbitmq",
  ]
}

variable "db_env" {
  //  type = "list"
  default = [
    "POSTGRES_PASSWORD=dbP@ssw0rd",
    "DB_SCHEMA=postgres",
    "POSTGRES_HOST=postgres",
    "POSTGRES_PORT=5432",
    "POSTGRES_DB=fredericocf",
    "POSTGRES_USER=fredericocf",
    "PGDATA=/var/lib/postgresql/data/pgdata",
    "DATABASE_URL=postgres://$${POSTGRES_USER}:$${POSTGRES_PASSWORD}@$${POSTGRES_HOST}:$${POSTGRES_PORT}/$${POSTGRES_DB}",
  ]
}

variable "rabbit_env" {
  //  type = "list"
  default = [
    "RABBITMQ_DEFAULT_USER=frederico",
    "RABBITMQ_DEFAULT_PASS=p@ssw0rd",
    "RABBITMQ_USERNAME=frederico",
    "RABBITMQ_PASSWORD=p@ssw0rd",
    "RABBITMQ_VHOST=/",
  ]
}
