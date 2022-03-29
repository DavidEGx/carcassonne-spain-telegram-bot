FROM python:alpine3.14

RUN apk update && apk add bash vim g++ make git curl py3-autopep8 ctags fzf

COPY . /app
WORKDIR /app

# Python development dependencies setup
RUN pip install --no-cache-dir -r dev/requirements.txt
RUN ["ln", "-s", "/usr/local/bin/flake8", "/usr/bin/flake8"]

# Vim setup
COPY dev/.vimrc /root/.vimrc
RUN ["curl", "-sfLo", "/root/.vim/autoload/plug.vim", "--create-dirs", "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"]
RUN bash -c 'vim +PlugInstall +qall > /dev/null'

ENTRYPOINT /bin/bash
