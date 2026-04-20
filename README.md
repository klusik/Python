# Python Playground and Learning Repository

This repository is a long running collection of Python exercises, workshop materials, experiments, utility scripts, and small side projects. It grew over time from study sessions, PyLadies practice, programming meetups, coding challenges, and practical tools built for specific situations.

The codebase is broad rather than uniform. Some folders contain small beginner exercises, some contain half-finished ideas, and some are more polished standalone scripts or GUI tools.

## What You Will Find Here

- Introductory Python exercises
- Algorithms and data structure practice
- Object oriented programming experiments
- Tkinter desktop apps
- Parsing and file processing utilities
- Numeric and math related scripts
- Small personal tools and one-off automation
- Training materials and external reference files

## Repository Structure

### Numbered lesson folders

The folders `001` through `020` mainly contain educational tasks and practice code. These are grouped by topic and usually include one or more alternative solutions.

Examples:

- `001 -- Doplnění čísel do pole`
- `002 -- Listy`
- `003 -- if, while, for`
- `006 -- Dict`
- `007 -- Bisection Method`
- `011 -- OOP`
- `012 -- Numerical Integration`
- `014 -- Hangman`
- `015 -- Collatz`
- `018 -- Histogram`
- `018 -- Threads`
- `020 -- Exception handling`

These folders are useful if you want to follow the learning path from basic control flow up to classes, recursion, numerical tasks, and simple object models.

### `Bonusy`

`Bonusy` is the largest mixed collection in the repository. It contains side projects, experiments, prototypes, challenge solutions, and utility scripts. The quality and completeness vary a lot by folder.

Examples of notable subprojects:

- `Bonusy/FTP downloader app`
  Tkinter application for browsing selected FTP directories and downloading them locally.
- `Bonusy/HTML linearizer`
  CLI utility for merging an HTML file and its linked local CSS and JS files into one text output.
- `Bonusy/inlineEasyCalculator`
  Small desktop calculator built with Tkinter.
- `Bonusy/GenerateSAPHours`
  Early utility for working with SAP hour distribution.
- `Bonusy/PDF Merger`
  Script for merging PDF files.
- `Bonusy/GPUZ log reader`
  Reader for GPU-Z sensor logs.
- `Bonusy/IMDB_movies`
  Small project working with movie rating data.
- `Bonusy/Sudoku`
  Sudoku related code.
- `Bonusy/romanNumerals`
  Roman numeral conversion work.

There are also many folders focused on games, random generators, parsers, school tasks, C or C# experiments, and coding challenge solutions.

### `geometry`

Custom geometry related code with classes such as `Point`, `Rectangle`, `Circle`, and `Abscisse`, plus a small Tkinter demo for drawing shapes.

### `XML handling`

Experiments with XML creation and parsing using the standard library.

### `Slovník`

Dictionary related scripts and Czech word data.

### `Python setkávání`

Practice code and meetup style exercises.

### `pyladies_klusik`

PyLadies related materials, examples, and exercises grouped by topic.

### `codewars`

Challenge solutions and small coding exercise files.

### `michal`

A separate larger collection of exercises, experiments, and imported project trees. This area includes both practice code and third party style source trees.

### `_ Zdroje a materiály`

Reference material such as cheat sheets, PDFs, notes, and study resources.

## Recommended Starting Points

If you want to explore the repository without getting lost, these are good places to start:

1. `Bonusy/HTML linearizer`
   One of the cleaner standalone scripts in the repository.
2. `Bonusy/FTP downloader app`
   A practical GUI tool with a clear purpose.
3. `geometry`
   Good for understanding the object oriented experiments.
4. `pyladies_klusik`
   Useful if you want structured learning examples.
5. The numbered folders `001` to `020`
   Best if you want the historical learning path.

## What This Repository Is Good For

- Browsing Python learning progress over time
- Reusing small utility scripts
- Studying beginner and intermediate examples
- Looking at different approaches to similar tasks
- Revisiting workshop and meetup exercises
- Extracting one-off tools into separate standalone projects

## Current State

This repository is actively useful as an archive and playground, but it is not organized as a single packaged application.

Important notes:

- The root structure contains many unrelated projects
- Some scripts are polished, some are drafts, and some are incomplete
- Not every file is expected to run without cleanup
- Some subfolders contain old experiments or external code snapshots
- The root `README.md` is intended as a guide, not full documentation for every subproject

## Running Code

Most scripts are plain Python files and can be run directly with Python 3.

Example:

```bash
python3 path/to/script.py
```

Some tools may require:

- `tkinter` for GUI applications
- local input files such as `.txt`, `.csv`, `.xml`, or `.pdf`
- manual configuration inside the script
- platform specific adjustments, especially for older Windows oriented scripts

## Notes on Quality and Maintenance

This repository mixes learning code with practical scripts. Because of that:

- coding style is not fully consistent
- naming conventions differ between folders
- documentation coverage varies
- some files contain unfinished ideas
- a few files contain syntax errors or old code that needs repair before use

If you want to turn parts of this repository into cleaner standalone projects, the best candidates are the focused utility folders inside `Bonusy`.

## Suggested Cleanup Direction

If this repository is going to stay public on GitHub, a sensible next step would be:

1. keep the current repository as the archive of learning and experiments
2. extract the best standalone tools into separate repositories
3. add short README files to the strongest subprojects
4. separate finished tools, educational materials, and abandoned experiments more clearly

## Language Notes

Folder names and comments are a mix of Czech and English. That reflects how the repository was built over time and the environments where the code was written.

## Summary

This repository is a personal Python lab. It documents a lot of hands-on work across beginner exercises, utility scripts, GUI tools, algorithm practice, and practical experiments. The value is in the breadth, the history, and the collection of small usable ideas.
