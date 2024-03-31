# Changelog

All notable changes to this project will be documented in this file. See [commit-and-tag-version](https://github.com/absolute-version/commit-and-tag-version) for commit guidelines.

## [1.3.1](https://github.com/DCsunset/pandoc-include/compare/v1.3.0...v1.3.1) (2024-03-31)


### Bug Fixes

* fix file lookup by always also searching in paths provided in include-resources ([1eee193](https://github.com/DCsunset/pandoc-include/commit/1eee193d7537291a90cb5d9efe460b2fe0d63c10))


### Misc

* add test for nixpkgs result bin ([9c228eb](https://github.com/DCsunset/pandoc-include/commit/9c228eb8bad849e4d83e4cf00c38b4fec667fe42))
* update installation doc in readme ([bd0183d](https://github.com/DCsunset/pandoc-include/commit/bd0183de6ad7628abdc33e2b139b232cbf4de322))


## [1.3.0](https://github.com/DCsunset/pandoc-include/compare/v1.2.1...v1.3.0) (2024-02-10)


### ⚠ BREAKING CHANGES

* emit a warning if file not found by default

### Features

* Adding handling of resource-paths for includes by adding `include-resources` as meta data variable. ([f5c0644](https://github.com/DCsunset/pandoc-include/commit/f5c064451f8e42045de9710a53a71ee866a723bc))
* Adding possibility to include `XML` files while applying a `XSL` transformation ([fd001f9](https://github.com/DCsunset/pandoc-include/commit/fd001f981fced76684ea39cec04f8bbefb78533f))
* emit a warning if file not found by default ([560f850](https://github.com/DCsunset/pandoc-include/commit/560f85028bb4b5fbd753f1107225f5a175a46a39))


### Bug Fixes

* convert to strict markdown to test include line ([adfe00e](https://github.com/DCsunset/pandoc-include/commit/adfe00e1ac4abedcc78ade4266d23e456f9e36fe))
* fix not found error for code include ([6260381](https://github.com/DCsunset/pandoc-include/commit/62603811ab687b7e9cf73b032d29fc0c3fb31303))
* merge options with default to prevent missing keys ([b21fb71](https://github.com/DCsunset/pandoc-include/commit/b21fb71606abad1ccfb96943253e7813e81a923d))


### Misc

* add docs for environment variables ([d5d82e0](https://github.com/DCsunset/pandoc-include/commit/d5d82e07b5d05c1f41bcb26e212480becd859b9d))
* add nix flake for dev environment ([6c6422d](https://github.com/DCsunset/pandoc-include/commit/6c6422d684530f4047b30e7abd4c6d36b978bfe4))
* add todo items ([0c5e8fd](https://github.com/DCsunset/pandoc-include/commit/0c5e8fd8e0936ff49c86e7f3cfecf6fca3a46abd))
* allow manual dispatch ([f7a6be3](https://github.com/DCsunset/pandoc-include/commit/f7a6be3c2e3a7d812debc5cbb8f6ec91ff440425))
* fix github action ([63c5c62](https://github.com/DCsunset/pandoc-include/commit/63c5c6298897faabb89b50709503d171ce34f5de))

## [1.2.1](https://github.com/DCsunset/pandoc-include/compare/v1.2.0...v1.2.1) (2023-11-08)


### Bug Fixes

* improve efficiency and refactor code ([9cde6de](https://github.com/DCsunset/pandoc-include/commit/9cde6de71a5c17e4fcf0db124468c5137bc9a278))


### Misc

* add config for venv ([f94e4c1](https://github.com/DCsunset/pandoc-include/commit/f94e4c19d0845c86433fbe3b619dbe8d5e3d7726))
* add doc for special filenames ([45b65df](https://github.com/DCsunset/pandoc-include/commit/45b65df64d4b857792f9a8701d707b6cdd33d4d2))
* add minimum pandoc version ([7136d06](https://github.com/DCsunset/pandoc-include/commit/7136d066cb429fb3c9c1afc39e71846c4ab2eaf7))
* add test for sepecial filenames ([29ed6e7](https://github.com/DCsunset/pandoc-include/commit/29ed6e71e7a28425bb570aeb4ae64a2a943c822b))
* update description of format field ([f0cd4fe](https://github.com/DCsunset/pandoc-include/commit/f0cd4fe98532d1df79882eec2c81dc1fc9e27770))
* update version updater ([c21df5f](https://github.com/DCsunset/pandoc-include/commit/c21df5feca32f646db0d4198d105169d2616870f))

## [1.2.0](https://github.com/DCsunset/pandoc-include/compare/v1.1.0...v1.2.0) (2021-10-23)


### Features

* allow include as raw blocks ([fcc6193](https://github.com/DCsunset/pandoc-include/commit/fcc61937dc091022921cd1f9d3fb21995d397935))

## [1.1.0](https://github.com/DCsunset/pandoc-include/compare/v1.0.1...v1.1.0) (2021-08-30)


### ⚠ BREAKING CHANGES

* rewrite relative paths

### Features

* rewrite relative paths ([a36ca20](https://github.com/DCsunset/pandoc-include/commit/a36ca20ebc970c2484bbc9e6887187406495b512))


### Bug Fixes

* fix code include check ([2af041a](https://github.com/DCsunset/pandoc-include/commit/2af041a4ebd37a037b5255180a0d7caa3f952593))

### [1.0.1](https://github.com/DCsunset/pandoc-include/compare/v1.0.0...v1.0.1) (2021-08-27)


### Bug Fixes

* fix attribute error ([1436483](https://github.com/DCsunset/pandoc-include/commit/143648375e1714692346b8c4230f4dbe59720d12))

## [1.0.0](https://github.com/DCsunset/pandoc-include/compare/v0.8.7...v1.0.0) (2021-08-26)


### ⚠ BREAKING CHANGES

* change parsing logic

### Features

* add dedent ([a51f74e](https://github.com/DCsunset/pandoc-include/commit/a51f74ed707fce9a38239d2e8800ba378ec7bd47))
* add support for different formats ([52c316a](https://github.com/DCsunset/pandoc-include/commit/52c316a2c9bddccb1eb8c7b5331d358cc0bff434))
* add type for config key ([2a64547](https://github.com/DCsunset/pandoc-include/commit/2a64547c07d8291e71e91736c04d4aa8c611e8b8))
* allow negative line numbers ([a6792e7](https://github.com/DCsunset/pandoc-include/commit/a6792e7ee7e9610b160426ed7b9d483d9c7eb63f))
* change parsing logic ([53fce08](https://github.com/DCsunset/pandoc-include/commit/53fce08829444f30cd4c293b281b3621454d6fc4))
* ignore rest of line when including ([5e09040](https://github.com/DCsunset/pandoc-include/commit/5e0904011f6e135ce20eed68d52c03cfcf51ab67))
* improve snippet include ([82115a6](https://github.com/DCsunset/pandoc-include/commit/82115a6f227e1228e011b0bc8640552ffffb2e69))
* move name and config parsing ([1c03dfe](https://github.com/DCsunset/pandoc-include/commit/1c03dfeee7aa101fda1e5f9b5cb9cc909146c78f))
* support options for partial include ([3e3d0fc](https://github.com/DCsunset/pandoc-include/commit/3e3d0fc95d84457ce5c60bfb0f984b4af40082af))


### Bug Fixes

* add missing modules ([ba0c3e5](https://github.com/DCsunset/pandoc-include/commit/ba0c3e58f67d6f5df4871ab6c9fb2830d5b35a75))
* add package import in __init__ ([7fa9641](https://github.com/DCsunset/pandoc-include/commit/7fa96419f031d8a7a360c36f8c42b7b923305489))
* fix a bug ([dcced91](https://github.com/DCsunset/pandoc-include/commit/dcced913d4bcf2dfb857c361abe6dadf53d5ca18))
* fix a typo ([e2ee9ab](https://github.com/DCsunset/pandoc-include/commit/e2ee9abf900008a012058df5328a2d61d5bf740c))
* fix invalid indexing ([24383d8](https://github.com/DCsunset/pandoc-include/commit/24383d8b3c4a10dbaa395cf2b777f59bbc90c3c9))
* fix module import ([a01bdf2](https://github.com/DCsunset/pandoc-include/commit/a01bdf22e5ed0be7d636c3cd1dcda6ebab120b11))
* fix setup.py ([bc6a0fe](https://github.com/DCsunset/pandoc-include/commit/bc6a0fe0b44f3b001e0b03ebf1df5cc59149d89b))
* rename dir name ([5c41e2c](https://github.com/DCsunset/pandoc-include/commit/5c41e2c6c3ae784cb067dae55c5db39ecafd909c))

### [0.8.7](https://github.com/DCsunset/pandoc-include/compare/v0.8.6...v0.8.7) (2021-04-11)


### Bug Fixes

* remove unnecessary dependencies ([cae8184](https://github.com/DCsunset/pandoc-include/commit/cae8184e0ade96e279a890b6ce325de90939034a))

### [0.8.6](https://github.com/DCsunset/pandoc-include/compare/v0.8.5...v0.8.6) (2021-04-11)


### Bug Fixes

* fix raw header-includes ([3caa003](https://github.com/DCsunset/pandoc-include/commit/3caa0032a4f3d66d6c10da5f8405733c3d9c37c8))

### [0.8.5](https://github.com/DCsunset/pandoc-include/compare/v0.8.4...v0.8.5) (2021-03-09)


### Features

* add code including ([b90177d](https://github.com/DCsunset/pandoc-include/commit/b90177d945cd7e25893d2dbde1badd7338b69a0f))


### Bug Fixes

* pass pandoc_options only when necessary ([a9b5b8a](https://github.com/DCsunset/pandoc-include/commit/a9b5b8adfa0b416406479a1c16e979cc03f32326))

### [0.8.4](https://github.com/DCsunset/pandoc-include/compare/v0.8.3...v0.8.4) (2020-11-25)

### [0.8.3](https://github.com/DCsunset/pandoc-include/compare/v0.8.2...v0.8.3) (2020-09-30)


### ⚠ BREAKING CHANGES

* fix the option name

### Bug Fixes

* fix the option name ([7277158](https://github.com/DCsunset/pandoc-include/commit/7277158d5aec403518de6c6ab83877b185518b24))

### [0.8.2](https://github.com/DCsunset/pandoc-include/compare/v0.8.1...v0.8.2) (2020-09-29)


### ⚠ BREAKING CHANGES

* remove default extension

### Bug Fixes

* remove default extension ([7d1eb12](https://github.com/DCsunset/pandoc-include/commit/7d1eb12208663ae9459d774103d4237dc5919ebf))

## [0.8.1](https://github.com/DCsunset/pandoc-include/compare/v0.8.0...v0.8.1) (2020-09-29)


### Bug Fixes

* fix dependencies ([7650adb](https://github.com/DCsunset/pandoc-include/commit/7650adb76b57424ddd6d60215ff464606e23c9b1))



# [0.8.0](https://github.com/DCsunset/pandoc-include/compare/v0.7.3...v0.8.0) (2020-09-29)


### Features

* add support for shell-style wildcards ([6134ae6](https://github.com/DCsunset/pandoc-include/commit/6134ae6135a7aac57c4d859e7bacd2da0ccfbc5e))



## [0.7.3](https://github.com/DCsunset/pandoc-include/compare/v0.7.2...v0.7.3) (2020-06-27)


### Bug Fixes

* fix deprecated load function ([e536320](https://github.com/DCsunset/pandoc-include/commit/e5363203375dd279913e12aab1ed81bbc3d95f83))



## [0.7.2](https://github.com/DCsunset/pandoc-include/compare/v0.7.1...v0.7.2) (2020-04-30)



## [0.7.1](https://github.com/DCsunset/pandoc-include/compare/v0.7.0...v0.7.1) (2020-04-30)


### Bug Fixes

* remove temp file if it exists ([610ab42](https://github.com/DCsunset/pandoc-include/commit/610ab42f6a12397a379c55eb04f8f3f5e1cd84d0))



# [0.7.0](https://github.com/DCsunset/pandoc-include/compare/v0.6.3...v0.7.0) (2020-02-26)


### Features

* add pandoc-options ([7afcd61](https://github.com/DCsunset/pandoc-include/commit/7afcd61290ce15fffee6e3d17ac7a50be92583aa))



## [0.6.3](https://github.com/DCsunset/pandoc-include/compare/v0.6.2...v0.6.3) (2020-01-07)


### Bug Fixes

* remove debug info ([5ddf096](https://github.com/DCsunset/pandoc-include/commit/5ddf0968c4bae5836c56cfd39625ba8d9fcfe929))



## [0.6.2](https://github.com/DCsunset/pandoc-include/compare/v0.6.0...v0.6.2) (2020-01-07)


### Bug Fixes

* fix latex in header ([69b60e1](https://github.com/DCsunset/pandoc-include/commit/69b60e1dfd54f08e1bc5fbc122252965eb7bc0bd))



# [0.6.0](https://github.com/DCsunset/pandoc-include/compare/v0.5.1...v0.6.0) (2019-09-28)



## [0.5.1](https://github.com/DCsunset/pandoc-include/compare/v0.5.0...v0.5.1) (2019-09-28)



# [0.5.0](https://github.com/DCsunset/pandoc-include/compare/v0.4.1...v0.5.0) (2019-09-28)



## [0.4.1](https://github.com/DCsunset/pandoc-include/compare/v0.4.0...v0.4.1) (2019-09-25)



# 0.4.0 (2019-07-15)
