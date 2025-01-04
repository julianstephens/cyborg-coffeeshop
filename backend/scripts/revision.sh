#!/bin/bash

msg=$1

alembic revision --autogenerate -m "$msg"
