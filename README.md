# Python Repository

This repository is a consolidated workspace for Python learning, experimentation, utility scripting, and small standalone projects. It contains several years of exercises, meetup materials, PyLadies practice, algorithm work, GUI prototypes, parsing tools, and one purpose automation.

The repository is organized as a collection of topic folders and subprojects rather than as one deployable application. Most directories are independent. Some contain short educational exercises, some contain incomplete prototypes, and some are reusable tools with a clear scope.

## Contents

- [Repository Profile](#repository-profile)
- [Top Level Structure](#top-level-structure)
- [Numbered Learning Track](#numbered-learning-track)
- [Notable Project Areas](#notable-project-areas)
- [Highlighted Utility Folders](#highlighted-utility-folders)
- [How To Navigate This Repository](#how-to-navigate-this-repository)
- [Running Code](#running-code)
- [Technical Characteristics](#technical-characteristics)
- [Current Caveats](#current-caveats)
- [Recommended Cleanup Path](#recommended-cleanup-path)

## Repository Profile

Main themes represented in the repository:

- Python fundamentals
- loops, conditions, lists, dictionaries, and strings
- sorting and numeric exercises
- object oriented programming
- basic numerical methods
- text processing and parsing
- XML and HTML related scripting
- Tkinter GUI applications
- coding challenge practice
- small personal automation and utility tools

Language and naming are mixed between Czech and English. This reflects how the repository evolved over time across different learning contexts and side projects.

## Top Level Structure

### Numbered folders

The folders `001` through `020` form the most structured part of the repository. They represent topic based learning units and practice assignments.

Examples:

- `001 -- Doplnění čísel do pole`
- `002 -- Listy`
- `003 -- if, while, for`
- `005 -- SelectSort`
- `006 -- Dict`
- `007 -- Bisection Method`
- `011 -- OOP`
- `012 -- Numerical Integration`
- `014 -- Hangman`
- `015 -- Collatz`
- `018 -- Histogram`
- `018 -- Threads`
- `020 -- Exception handling`

### Mixed project and utility areas

These folders contain broader experiments and practical tools:

- `Bonusy`
- `geometry`
- `Slovník`
- `XML handling`
- `Python setkávání`
- `pyladies_klusik`
- `codewars`
- `michal`
- `_ Zdroje a materiály`

### Other standalone folders

Additional smaller areas include:

- `Danny`
- `FTP Upload`
- `KlusParser`
- `LukasMichal`
- `klusik_phone_number`
- `HTML`

## Numbered Learning Track

The numbered folders are the closest thing this repository has to a curriculum. They are useful if you want a chronological or topic driven path through the material.

### Early fundamentals

- `001 -- Doplnění čísel do pole`
  Basic list and array style tasks.
- `002 -- Listy`
  Introductory list work and prime related exercises.
- `003 -- if, while, for`
  Control flow, loops, simple file reading, and beginner logic.
- `004 -- Trénovací den 001`
  Early practice tasks including generation, reading, and sorting exercises.

### Core algorithm practice

- `005 -- SelectSort`
  Selection sort and related beginner algorithm tasks.
- `006 -- Dict`
  Dictionary practice and lookup style exercises.
- `007 -- Bisection Method`
  Basic numerical method implementation.
- `008 -- Substring in String`
  String inspection and substring logic.
- `009 -- Rozložení na prvočísla etc`
  Prime factorization related work.

### Intermediate exercises

- `010 -- Setkani`
  Mixed meetup or seminar style exercises.
- `011 -- OOP`
  Object oriented programming practice and small object models.
- `012 -- Numerical Integration`
  Numerical integration implementations.
- `013 -- Dešifrování Lukášovy zprávy`
  Caesar cipher and message decoding exercises.
- `014 -- Hangman`
  Hangman implementations.
- `015 -- Collatz`
  Collatz sequence related work.

### Later topic folders

- `016 -- Documentation`
  Documentation related practice.
- `017 -- Objects`
  Further object work, including score related examples.
- `018 -- Histogram`
  Histogram and related object oriented practice.
- `018 -- Threads`
  Early threading experiments.
- `019 -- Online Python`
  Miscellaneous exercises and challenge style scripts.
- `020 -- Exception handling`
  Basic exception handling examples.

## Notable Project Areas

### `Bonusy`

`Bonusy` is the largest and most varied area in the repository. It acts as a general holding area for side projects, focused experiments, topic folders, challenge work, prototypes, and utility scripts.

This folder includes work related to:

- GUI applications
- games and simulations
- math and number theory
- parsing and conversion tools
- coding challenges
- data processing
- FTP and file transfer tasks
- PDF and text utilities
- HTML and frontend related experiments
- aviation themed helpers
- miscellaneous personal tools

The quality level varies significantly across subfolders. Some folders are quick experiments, while others are strong candidates for extraction into standalone repositories.

### `geometry`

This area contains a custom geometry library and a small Tkinter visualization script. It focuses on objects such as:

- `Point`
- `Rectangle`
- `Circle`
- `Abscisse`

It is useful as a record of OOP and geometry related experimentation.

### `Slovník`

Contains dictionary related scripts and Czech language word data. This area combines text handling and lookup style logic.

### `XML handling`

Contains small XML creation and parsing experiments using the standard library.

### `Python setkávání`

Contains meetup style practice code and small exercises prepared for shared sessions.

### `pyladies_klusik`

Contains PyLadies related examples, grouped exercises, and topic based practice material. This is one of the more structured educational areas outside the numbered folders.

### `codewars`

Contains challenge solutions and practice scripts inspired by online coding platforms.

### `michal`

This is a larger separate collection containing practice code, experiments, imported project trees, and additional subprojects. It appears to function as a secondary workspace inside the repository.

### `_ Zdroje a materiály`

Stores reference documents, cheat sheets, notes, PDFs, and other learning materials.

## Highlighted Utility Folders

The following folders are the strongest entry points if you want to inspect more practical or tool oriented code.

### `Bonusy/HTML linearizer`

Purpose:

- merge an HTML entry file with linked local CSS and JavaScript files
- produce a single text output that preserves file boundaries

Why it stands out:

- clear scope
- command line utility shape
- focused file processing logic
- easy to understand input and output behavior

### `Bonusy/FTP downloader app`

Purpose:

- connect to an FTP server
- inspect selected top level paths
- download chosen directories locally

Why it stands out:

- practical GUI use case
- Tkinter based interface
- real world utility focus

### `Bonusy/inlineEasyCalculator`

Purpose:

- provide a basic desktop calculator interface

Why it stands out:

- compact Tkinter application
- readable event driven structure

### `Bonusy/GenerateSAPHours`

Purpose:

- assist with SAP number handling and work hour distribution logic

Why it stands out:

- domain specific utility concept
- clear real world motivation

### `Bonusy/PDF Merger`

Purpose:

- combine PDF inputs into one output file

### `Bonusy/GPUZ log reader`

Purpose:

- process and inspect GPU-Z sensor log data

### `Bonusy/codex_project`

Purpose:

- frontend style mini project with:
  `index.html`, CSS, JavaScript, image assets, gallery data, and source notes

Why it matters here:

- introduces a non pure Python project shape into the repository
- shows expansion beyond Python only exercises

## How To Navigate This Repository

Recommended paths depending on what you want:

### For structured learning material

Start with:

1. `001 -- Doplnění čísel do pole`
2. `002 -- Listy`
3. `003 -- if, while, for`
4. continue through the numbered folders in order

### For practical tools

Start with:

1. `Bonusy/HTML linearizer`
2. `Bonusy/FTP downloader app`
3. `Bonusy/inlineEasyCalculator`
4. `Bonusy/PDF Merger`

### For GUI work

Focus on:

- `Bonusy/inlineEasyCalculator`
- `Bonusy/FTP downloader app`
- `geometry/shapes.py`
- other Tkinter related folders inside `Bonusy`

### For parsing and text processing

Focus on:

- `Bonusy/HTML linearizer`
- `XML handling`
- `Slovník`
- parsing related folders inside `Bonusy`

### For educational archives and notes

Focus on:

- `pyladies_klusik`
- `Python setkávání`
- `_ Zdroje a materiály`

## Running Code

Most scripts can be run directly with Python 3.

Example:

```bash
python3 path/to/script.py
```

In practice, running code may require:

- local input files placed next to the script
- manual edits to file paths inside the source
- standard library GUI support such as `tkinter`
- environment assumptions from older machines or Windows based paths
- checking folder specific files such as `requirements.txt` or local notes

There is no single root level package, installer, or unified CLI entry point.

## Technical Characteristics

Repository level characteristics:

- multi project layout
- mostly plain script based Python
- no unified packaging strategy
- no central dependency management
- mixed naming conventions
- mixed language comments and folder names
- broad variation in code maturity

Visible technical patterns include:

- standalone `.py` scripts
- Tkinter GUI applications
- file parsing and transformation scripts
- numeric and algorithmic exercises
- small data processing utilities
- archived project snapshots

The repository also currently contains multiple `__pycache__` directories across the top level project folders.

## Current Caveats

Important expectations for anyone browsing or reusing the code:

- this is not a single production codebase
- some folders are clean and focused, others are exploratory
- some scripts are complete enough to run directly
- some scripts need cleanup before reuse
- documentation quality varies by folder
- naming and structure reflect growth over time rather than strict standardization

For GitHub visitors, the best approach is to treat the repository as a technical archive with several reusable subprojects inside it.

## Recommended Cleanup Path

If the repository continues to evolve, the most useful structural improvements would be:

1. add short local README files to the best subprojects
2. ignore or remove committed `__pycache__` directories
3. separate archived experiments from stronger reusable tools
4. standardize naming in selected public facing folders
5. extract the most mature utility folders into standalone repositories if needed

## Summary

This repository serves as a broad technical notebook and project archive. It captures learning progress, practice tasks, utility ideas, GUI experiments, and small real world scripts in one place. Its strength is range rather than uniformity, and its most useful parts are the focused subprojects and the clear educational progression in the numbered folders.
