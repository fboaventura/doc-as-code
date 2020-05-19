provider "docker" {
  registry_auth {
    address = "registry.gitlab.com"
    config_file = pathexpand("~/.docker/config.json")
  }
}

resource "docker_image" "website-dev" {
  name         = "registry.gitlab.com/ffbdev/fboaventuradev:latest-dev"
  keep_locally = true
}

resource "docker_image" "website-prod" {
  name = "registry.gitlab.com/ffbdev/fboaventuradev:latest"
}

resource "docker_image" "postgres" {
  name = "postgres:12-alpine"
}

resource "docker_image" "rabbitmq" {
  name = "bitnami/rabbitmq:latest"
}

resource "docker_image" "redis" {
  name = "redis:latest"
}

resource "docker_volume" "ffbdev_pgsql" {
  name = "ffbdev_pgsql"
}

resource "docker_volume" "ffbdev_rabbit" {
  name = "ffbdev_rabbit"
}

resource "docker_container" "website" {
  image = docker_image.website-dev.latest
  name  = "website"
  env = var.app_env
  volumes {
    host_path      = var.host_path
    container_path = "/code"
    read_only      = false
  }
  ports {
    internal = 8001
    external = 8000
  }
  depends_on = [
    docker_container.postgres,
    docker_container.rabbitmq,
    docker_container.redis,
  ]
  must_run = true
  restart  = "always"
}

resource "docker_container" "postgres" {
  image = docker_image.postgres.latest
  name  = "postgres"
  hostname = "postgres"
  env = var.db_env
  volumes {
    volume_name    = docker_volume.ffbdev_pgsql.name
    container_path = "/var/lib/postgresql/data/pgdata"
  }
  ports {
    internal = 5432
    external = 5432
  }
  must_run = true
  restart  = "always"
}

resource "docker_container" "rabbitmq" {
  image = docker_image.rabbitmq.latest
  name  = "rabbitmq"
  env = var.rabbit_env
  volumes {
    volume_name    = docker_volume.ffbdev_rabbit.name
    container_path = "/bitnami"
  }
  ports {
    internal = 4369
    external = 4369
  }
  ports {
    internal = 5672
    external = 5672
  }
  ports {
    internal = 25672
    external = 25672
  }
  ports {
    internal = 15672
    external = 15672
  }
  must_run = true
  restart  = "always"
}

resource "docker_container" "redis" {
  image = docker_image.redis.latest
  name  = "redis"
  ports {
    internal = 6379
    external = 6379
  }
  must_run = true
  restart  = "always"
}

resource "docker_container" "beat" {
  image   = docker_image.website-dev.latest
  name    = "celery_beat"
  command = ["/start/beat.sh"]
  env = var.app_env
  volumes {
    host_path      = var.host_path
    container_path = "/code"
    read_only      = false
  }
  depends_on = [
    docker_container.postgres,
    docker_container.rabbitmq,
    docker_container.redis,
  ]
  must_run = true
  restart  = "always"
}

resource "docker_container" "worker" {
  image   = docker_image.website-dev.latest
  count   = 2
  name    = "celery_worker-${count.index + 1}"
  command = ["/start/beat.sh"]
  env = var.app_env
  volumes {
    host_path      = var.host_path
    container_path = "/code"
    read_only      = false
  }
  depends_on = [
    docker_container.postgres,
    docker_container.rabbitmq,
    docker_container.redis,
  ]
  must_run = true
  restart  = "always"
}

resource "docker_container" "flower" {
  image   = docker_image.website-dev.latest
  name    = "celery_flower"
  command = ["/start/beat.sh"]
  env = var.app_env
  volumes {
    host_path      = var.host_path
    container_path = "/code"
    read_only      = false
  }
  depends_on = [
    docker_container.postgres,
    docker_container.rabbitmq,
    docker_container.redis,
    docker_container.beat,
    docker_container.worker,
  ]
  must_run = true
  restart  = "always"
}
