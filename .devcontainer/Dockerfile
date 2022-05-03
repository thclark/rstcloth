# A useful base repository based on ms devcontainer but with a bunch of fixes
# and useful installs (geo tools are unnecessary for this project, but all the other tweaks are helpful)
FROM windpioneers/gdal-python:familiar-catshark-gdal-2.4.1-python-3.9-dev

# Tell zsh where you want to store history
#     We leave you to decide, but if you put this into a folder that's been mapped
#     into the container, then history will persist over container rebuilds :)
#
#     !!!IMPORTANT!!!
#     Make sure your .zsh_history file is NOT committed into your repository, as it can contain
#     sensitive information. So in this case, you should add
#         .devcontainer/.zsh_history
#     to your .gitignore file.
#
ENV HISTFILE="/workspaces/rstcloth/.devcontainer/.zsh_history"

# Switch to vscode user
USER vscode
WORKDIR /workspaces/rstcloth

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH "/home/vscode/.poetry/bin:$PATH"
RUN poetry config virtualenvs.create false

# Install python dependencies. Note that poetry installs any root packages by default,
# But this is not available at this stage of caching dependencies. So we do a dependency-only install here
# to cache the dependencies, then a full poetry install post-create to install any root packages.
COPY pyproject.toml poetry.lock ./
RUN poetry install --extras docs --no-ansi --no-interaction --no-root
