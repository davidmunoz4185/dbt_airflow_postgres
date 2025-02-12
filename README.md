# DBT AIRFLOW

In this repo's branch is detailed how to integrate the following tools:

- AirFlow
- DBT
- Postgres

in order to have a productive ELT environment.

To avoid SO dependencies, docker is used to integrate the components.

## REQUIREMENTS

As commented previously, docker must be installed beforehand.

If you are on Windows Platform, I recommend the use of _git bash_ or any linux commands extensions.

## SETUP

### 1ST STEP

Init env:

```BASH
./init_env.sh
```

At the end you should see a message like

```BASH
airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.8.0
start_airflow-init_1 exited with code 0
```

and a structure of folders created:

```BASH
logs/
dags/
plugins/
config/
postgres-db-volume/
```

These folders are created for AirFlow and Postgres DataBase purposes.

### 2ND STEP

Just execute

```BASH
./start_env.sh
```

and the rest of images will be started up.

## AirFlow Resources

The following [guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) offers all necessary to configure current project.

## DBT Resources

### DBT Jaffle Shop

Project example with its [repo](https://github.com/dbt-labs/jaffle_shop).
