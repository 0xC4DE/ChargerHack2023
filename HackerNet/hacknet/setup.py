import setuptools

setuptools.setup(
    name="hackerserver",
    install_requires=[
        "flask",
        "flask-wtf",
        "gunicorn",
        "psycopg2-binary",
        "peewee",
        "pycryptodome",
    ],
)
