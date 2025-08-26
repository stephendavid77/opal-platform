# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Centralized configuration management:
  - Created `shared/config/shared_config_manager.py` for centralized config access.
  - Updated `BuildPilot`, `CalMind`, and `XrayQC` to use the new centralized config manager.
  - Moved various subproject config files to `shared/config/` and converted them to `.sample` files where appropriate.
  - Updated `BuildPilot`, `CalMind`, and `XrayQC` code to reference centralized config.
  - Removed sensitive data and user-specific paths from committed config files, replacing them with placeholders in `.sample` files.
  - Updated `.gitignore` files in affected subprojects to ignore local config files.

### Changed
- Refactored `CalMind` Google Calendar authentication to use `shared/secrets_manager/`.
- Updated `CalMind` `README.md` and `config.yaml.sample` for centralized config and secrets management.

### Fixed
- Corrected import paths in `BuildPilot` modules.
- Fixed import paths in `shared/secrets_manager` modules.
