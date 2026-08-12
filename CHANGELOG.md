# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.2] - 2026-08-12

### Fixed

- fix: restore article intros, fix mobile viewport, unstick footer year (2e9743c)

### Other

- chore: update actions to align with other projects (b594b08)
- chore: update dependabot settings (c903716)
- chore: mass update (cf9620a)
- chore: bump the linting group with 3 updates (3cba163)
- chore: pin astroid to 4.0.4 for pylint compatibility (4295462)
- chore: bump the rendering group with 2 updates (39e6f79)
- chore: bump the testing group with 4 updates (226a6f5)
- chore: bump appleboy/ssh-action from 1.0.3 to 1.2.5 (01ba21f)
- chore: bump im-open/process-code-coverage-summary (311cac4)
- chore: bump im-open/code-coverage-report-generator (16eca37)
- chore: bump actions/setup-python from 4 to 7 (56f19ea)
- chore: bump actions/upload-artifact from 4 to 7 (0faaae8)
- chore: bump setuptools from 78.1.1 to 84.0.0 (bd208fd)
- chore: bump packaging from 24.2 to 26.3 (0ddc93f)
- chore: bump dill from 0.3.9 to 0.4.1 (f99bc6c)
- chore: bump tomlkit from 0.13.2 to 0.15.1 (cded5a4)
- chore: bump platformdirs from 4.3.6 to 4.11.1 (93876f1)
- chore: pin only direct dependencies (f0d3685)
- chore: bump actions/checkout from 4 to 7 (225f739)
- ci: enforce the code coverage thresholds (f845674)
- ci: lower branch threshold to 70 for headroom (9bed9a4)
- ci: make the deploy script idempotent and drop the wget typo (7f155d6)

## [1.5.1] - 2026-08-07

### Added

- add cheap to build article (cab8944)

## [1.5.0] - 2026-05-24

### Added

- feat: add job article over the last 3 years changing (ae999b4)

## [1.4.3] - 2026-05-01

### Fixed

- fix: journal article link broken (987ab10)

## [1.4.2] - 2026-04-30

### Fixed

- fix: update journal article to have correct number of dependencies (fb813a4)

## [1.4.1] - 2026-04-29

### Added

- feat: add journal blog entry and separate page, update now page (d022d71)

## [1.4.0] - 2026-02-15

### Added

- feat: add pragmatic summit article (b977d38)

## [1.3.1] - 2025-05-20

### Dependencies

- Bump setuptools from 75.6.0 to 78.1.1 (3b956f7)

## [1.3.0] - 2025-05-20

### Added

- Add AI article (372c34b)

## [1.2.3] - 2025-05-15

### Dependencies

- Bump jinja2 from 3.1.5 to 3.1.6 (6c67f48)

## [1.2.2] - 2025-05-11

### Changed

- Update actions to latest version (4c20f65)
- Update Python to 3.13 (9553bd8)

### Other

- Retro programming article and update to now page (7c5da65)

## [1.2.1] - 2025-01-28

### Changed

- Update now article 28th Jan 2025 (2c70274)

## [1.2.0] - 2025-01-28

### Added

- Add article on returning to work from paternity leave (38caa24)

## [1.1.0] - 2024-12-31

### Added

- Add PKM plugins article (fbd0f58)

## [1.0.6] - 2024-12-24

### Changed

- Update to Jinja2 3.1.5 (509d075)

## [1.0.5] - 2024-12-21

### Added

- Add Mac Setup article with static assets (197d0c7)

## [1.0.4] - 2024-12-12

### Added

- Add setup.cfg and build script around it (25e5767)

### Changed

- Update version run to ensure it replaces in all files (814ae04)

### Other

- Workflow needs to cancel in progress (c3a793e)
- Workflow on PRs only (8330011)
- Proven working so reset 80/90 threshold (eca6dd2)
- Try a different coverage action (da51b38)
- Try a different coverage action (b85125c)
- Try a different coverage action (61386c7)
- Another different PR action (e5443da)
- Another different PR action (5922f88)
- Another different PR action (77bcf1c)
- Remove tests folder from coverage (40d1471)
- Remove tests folder from coverage (a96914b)
- Force setup.cfg to be simpler, not going to be installed (fca5391)

### Testing

- Test PR comment failure (f27ebc8)

## [1.0.3] - 2024-12-09

### Changed

- Update dependencies (51e2beb)

## [1.0.2] - 2024-11-12

### Added

- Add static site article and update Now to Nov 2024 (beeabf7)

### Changed

- Update deploy workflow to use DO server (254d9db)

### Other

- A bit more debugging (ea1f1a0)
- Remove -o (a449439)
- Remove need to upload release - server can download public code (f511129)

## [1.0.1] - 2024-08-29

### Added

- Add article on moving from Terraform to CDK (fce4f0e)

## [1.0.0] - 2024-08-12

### Added

- Add Nginx config for local hosting (12ca7ea)

### Changed

- Improve nginx by using rewrite instead of redirect (6699d75)
- Tidy up articles and config files slightly from pylint (278952b)

### Other

- Move format to f-strings and tify up generate script (58ecaa5)
- Simpler package management with pip requirements (fb6074b)

## [0.24.15] - 2024-08-10

### Other

- Discovery stolen article (e9db91b)

## [0.24.14] - 2024-07-07

### Changed

- Update DynamoDB article to use partition and sort keys correctly with a query (f9ce302)

## [0.24.13] - 2024-07-07

### Changed

- Update now - July 2024 (842fa25)

## [0.24.12] - 2024-07-07

### Other

- Emergency image name fix (7569b47)

## [0.24.11] - 2024-07-07

### Added

- Add DynamoDB test containers article (40707c8)

## [0.24.10] - 2024-06-14

### Dependencies

- Bump braces and gulp in /blog/assets (073e493)

## [0.24.9] - 2024-04-04

### Other

- Remove ZIP before upload (4911ae5)

## [0.24.8] - 2024-04-04

### Other

- Clear static before upload (242c35f)

## [0.24.7] - 2024-04-04

### Other

- Reset workflow release downloader to v1.8 to solve extract (42f9198)

## [0.24.6] - 2024-04-04

### Other

- Set overwrite (cf098cc)

## [0.24.5] - 2024-04-04

### Added

- Add . for sync (9a93eec)
- Add . for sync (ae7cdf6)

## [0.24.4] - 2024-04-04

### Other

- Deploy AWS creds not working (6f48071)

## [0.24.3] - 2024-04-04

### Added

- Add deploy workflow (e82b878)

## [0.24.2] - 2024-02-24

### Other

- Zip file contains version name (3712a84)

## [0.24.1] - 2024-02-24

### Other

- Zip wasn't recursive (6fbce9b)

## [0.24.0] - 2024-02-20

### Added

- Add build config to generate dist and ZIP file in release (e8a5223)

### Changed

- Switch to generating a static site (ef39de8)

### Other

- Build on PRs temporarily (db87142)
- Build on PRs temporarily (aee4fc8)
- Only build on main again (3ae0f63)

## [0.23.1] - 2024-02-14

### Other

- Force update Dockerfile to use package labels (3f5a0e8)

## [0.22.1] - 2024-02-14

### Added

- Add GitHub Actions test workflow (7243b99)
- Add build workflow to ensure versions update (09a3c64)

### Other

- Ensure setuptools is installed (f878f50)
- Ensure correct version is calculated (e93c2be)

## [0.22.0] - 2024-02-10

### Added

- Add GitHub settings (f8b8e2f)

### Other

- Skip CI: updated version number (e64a318)

## [0.21] - 2024-02-10

### Changed

- Update Now page for Feb 2024 (1a01e15)

### Other

- Skip CI: updated version number (be26120)

## [0.20] - 2023-12-29

### Added

- Add developer experience article and change date of copyright (be4f0a4)

### Fixed

- Fix version number (0692087)

### Other

- Skip CI: updated version number (9675e46)
- Skip CI: updated version number (b5abeea)

## [0.19] - 2023-09-17

### Added

- Add PKM article (58ae235)

### Other

- Skip CI: updated version number (a39ba04)

## [0.18.1.2] - 2023-07-30

### Other

- Cheeky test add to rerun main (33d0b96)
- Skip CI: updated version number (6b20a73)

## [0.18.1.1] - 2023-07-30

### Other

- Don't need requests anymore (3fd6d2c)
- Skip CI: updated version number (004742a)

## [0.18.1] - 2023-07-30

### Fixed

- Fix GitHub version (d8b0911)

### Other

- Skip CI: updated version number (07a5b1e)

## [0.18.0.1] - 2023-07-30

### Other

- Remove GitHub version call (1bded30)

## [0.18] - 2023-07-23

### Added

- Add lambda article (f627041)

## [0.17.1] - 2023-07-21

### Fixed

- Fix missing post titles (ba61b0f)

## [0.17] - 2023-07-20

### Added

- Add mobile and SEO improvements (319fa20)

## [0.16] - 2023-05-18

### Changed

- Update now page for May 2023 (51c53e3)

## [0.15] - 2023-02-13

### Changed

- Update now page with developments (ee02405)

## [0.14.0.1] - 2022-12-21

### Dependencies

- Bump decode-uri-component from 0.2.0 to 0.2.2 in /blog/assets (7e7068a)

## [0.14] - 2022-11-18

### Added

- Add GH and Mastodon links (97b4093)

## [0.13] - 2022-11-18

### Added

- Add DevHub North post (6c4380d)

## [0.12.0.1] - 2022-11-13

### Dependencies

- Bump minimatch from 3.0.4 to 3.1.2 in /blog/assets (568c255)

## [0.12] - 2022-10-23

### Added

- Add now page (a1b995c)

## [0.11.1.1] - 2022-08-27

### Dependencies

- Bump yargs-parser from 5.0.0-security.0 to 5.0.1 in /blog/assets (64a5b61)

## [0.11.1] - 2022-08-27

### Dependencies

- Bump copy-props from 2.0.4 to 2.0.5 in /blog/assets (325d255)

### Fixed

- Fix test to work with public repo (2451952)
- Fix Jenkinsfile and flaky test (87795e8)

## [0.11] - 2022-08-27

### Added

- Add Makefile (5adb0b0)

## [0.10] - 2022-08-26

### Added

- Add part 3 car history (181de48)

### Other

- Spelling mistake (e946f61)

## [0.9.1] - 2022-08-19

### Fixed

- Fix to use jenkiuns lib: (aa29cca)

## [0.9] - 2022-08-15

### Added

- Add part 2 of car history (283d0f9)

### Fixed

- Fix existing history article to have continuation (bb7cfdf)

## [0.8] - 2022-08-07

### Added

- Add initial car history blog (5a09503)

## [0.7] - 2022-06-01

### Added

- Add version releases (3b53d3e)

## [0.6] - 2022-03-13

### Added

- Add Azure Terraform article (2d0f15e)

## [0.5.1] - 2022-02-06

### Fixed

- Fix typo (bb543fa)

## [0.5] - 2022-02-06

### Added

- Add Go/Docker article (b667912)

## [0.4.0.1] - 2022-01-24

### Testing

- Test elements (bcb6908)

## [0.4] - 2022-01-19

### Added

- Add Google Analytics (64f8541)

## [0.3] - 2022-01-15

### Added

- Add TF and Ansible article (680aab6)

### Changed

- Update TF article and add correct imagery (7904e45)

### Other

- Remove test article (4a587cb)

## [0.2.2] - 2022-01-08

### Fixed

- Fix date on motivation article (7beafb4)

## [0.2.1] - 2022-01-08

### Fixed

- Fix article sorting (ae52e84)

## [0.2] - 2022-01-08

### Added

- Add motivation article (fef9646)

## [0.1.1] - 2022-01-05

### Other

- Rework build to ensure Dockerfile is released, not test version (643ec94)

## [0.1.0.1] - 2022-01-05

### Other

- Remove one test article (2862009)

## [0.1] - 2022-01-04

### Changed

- Update flask to run on all hosts (40e2c52)

### Fixed

- Fix dockerfile run command (9876688)
- Fix docker commands (f07c1e9)
- Fix pipeline deploy issue (de90052)

### Other

- Initial commit with basic build (7745931)
- Attempt an initial build (b2f35d5)
- Cleanup correctly (1a919af)
- Ensure docker runs in background (daae964)
- Pipeline syntax (2cd7e44)
- Attempt release build (4db60fd)
- Correct branch name (c1fe9af)
- Migrate to ghcr (916c87e)
- Rework pipeline to release and deploy (6edab25)


