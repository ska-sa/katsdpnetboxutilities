FROM       python:3
MAINTAINER Martin Slabber <martin@ska.ac.za>

RUN mkdir /docs
WORKDIR /docs

#COPY requirements.txt ./
RUN pip install --no-cache-dir mkdocs Pygments pymdown-extensions
# MKDOCS Plugins
RUN pip install --no-cache-dir \
      mkdocs-awesome-pages-plugin \
      mkdocs-kroki-plugin \
      git+https://github.com/jldiaz/mkdocs-plugin-tags \
      autolink-references-mkdocs-plugin \
      mkdocs-pdf-export-plugin \
      mkdocs-ezlinks-plugin

# EXPOSE 3333

ENTRYPOINT ["mkdocs"]
# CMD ["serve", "--dev-addr=0.0.0.0:3333"]
