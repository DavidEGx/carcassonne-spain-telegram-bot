FROM python:alpine3.19 as base

COPY . /app
WORKDIR /app

ENV PYTHONPATH="/app:$PYTHONPATH"
RUN pip install -r requirements.txt


FROM base as dev
RUN apk update && apk add bash vim g++ make git curl py3-autopep8 ctags fzf

# Python development dependencies setup
RUN pip install -r dev/requirements.txt
RUN ["ln", "-s", "/usr/local/bin/flake8", "/usr/bin/flake8"]
RUN ["ln", "-s", "/usr/local/bin/pylint", "/usr/bin/pylint"]

# Vim setup
COPY dev/.vimrc /root/.vimrc
RUN ["curl", "-sfLo", "/root/.vim/autoload/plug.vim", "--create-dirs", "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"]
RUN bash -c 'vim +PlugInstall +qall > /dev/null'

ENTRYPOINT /bin/bash

FROM base as pro
ENTRYPOINT /app/bin/telegram_bot
