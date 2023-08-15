import setuptools

setuptools.setup(
    name="HackerServer",
    install_requires=[
        "flask",
        "flask-wtf",
        "sqlite",
        "gunicorn",
        "psycopg2-binary",
        "peewee",
    ],
)
