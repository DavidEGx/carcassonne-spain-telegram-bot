FROM python:alpine3.17

RUN apk update && apk add bash vim g++ make git curl py3-autopep8 ctags fzf py3-pylint

COPY . /app
WORKDIR /app
ENV PYTHONPATH="/app:$PYTHONPATH"

# Python development dependencies setup
RUN pip install -r dev/requirements.txt
RUN ["ln", "-s", "/usr/local/bin/flake8", "/usr/bin/flake8"]

# Vim setup
COPY dev/.vimrc /root/.vimrc
RUN ["curl", "-sfLo", "/root/.vim/autoload/plug.vim", "--create-dirs", "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"]
RUN bash -c 'vim +PlugInstall +qall > /dev/null'

ENTRYPOINT /bin/bash
