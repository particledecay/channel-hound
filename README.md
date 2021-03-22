# channel-hound
A comparison tool for channel-based streaming services

## What exactly does this do?
This project scrapes data from all the major channel-based streaming services to find the various packages, pricing options, and channels, and aggregates it all into a consolidated database.

The goal is to let you always have an updated look at which streaming services have the channels you really want, at the best price.

## Live application
This project is not currently live anywhere. But you can run it locally!

## Setup
### Requirements
- Database (PostgreSQL)
- Python 3.6+
- [Poetry](https://python-poetry.org/)

### Database init script
If you have a postgres installation, you can run the `init_db.sh` script on the running server to create the necessary user and database. The following variables can be set to your preference:
- PG_USER
- PG_HOST
- PG_PORT

Additionally, setting the `PG_PASS` environment variable will cause the 'houndadmin' database user to be created with the non-default password.

### Initial migration
Once the database has been set up, set the `PG_PASS` environment variable to the password for the 'houndadmin' database account. You should then run the available database migrations:

```bash
./manage.py migrate
```

## Usage
Once the database is ready to go, you simply run a crawl command for the spider that you want to trigger:

```bash
scrapy crawl hulu
```

This will automatically retrieve any channels and packages for that service and insert them into your database.

## Supported streaming services (currently)
- DIRECTV NOW
- Sling
- YouTube TV
- Playstation Vue
- Hulu w/ Live TV
- Philo

## Contributing
Please read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
