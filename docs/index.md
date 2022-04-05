# Welcome to the Web Akari Documentation

This documentation has been written to guide users in tweaking the experience of the game and as a guideline for developers to follow when contributing to the project.

# MkDocs

As you may have noticed, this documentation is built by a software called MkDocs, that lets you create beautiful pages using markdown, a very simple language. View the full documentation at [mkdocs.org](https://www.mkdocs.org).

### MkDocs Commands

The only command that you'll need while adding stuff to the documentation is the following:

* `mkdocs serve` - This will start the live-reloading docs server. You will see changes to the documentation live whenever you save a file.

## Project layout (File structure)

    # The Akari website
    ./client      # The client-side website files
    ./server      # The backend server application files (Flask)

    # MkDocs
    mkdocs.yml    # The configuration file for MkDocs.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
