# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2023-02-19

### Added

- Added a script to generate thumbnails from current samples

### Changed

- Updated README.md to include helpful instructions

## [0.0.2] - 2023-02-02

### Added

- Added info to episodes, such as air date, star date, option to report problems with info displayed 
- Added the 'show detailed info' button, which will show a screen capture during the sample you heard, and a description of the episode
- Added a script to create tables in PostgreSQL from JSON data

### Changed

- Switched from Redis to PostgreSQL

## [0.0.1] - 2023-01-20

### Fixed

- Fixed timer not starting
- Fixed samples repeating themselves even though the user was supposed to be hearing a different one
- Fixed an issue where clicking next would correctly answer the question
- Fixed an issue in string normalization which caused accents to be handled improperly
- Fixed a problem where the same episode would sometimes play after you successfully guessed it

[0.0.1]: https://github.com/olivierlacan/keep-a-changelog/releases/tag/v0.0.1