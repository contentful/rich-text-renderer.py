# CHANGELOG

## Unreleased

## v0.2.7
* Changed CI/CD vendor from Travis to CircleCi
* Use Twine for publishing on PYPI
* Added author and changed author email
* Updated `tox.ini` to test for `py37`

## v0.2.6
### Fixed
* Fixed packaging script to include Readme

## v0.2.5
### Added
* Add support for Rich Text Tables

## v0.2.4
### Fixed
* Fixed a typo which was causing the wrong exception to be bubbled up when assets were missing on an embedded asset block. [#12](https://github.com/contentful/rich-text-renderer.py/pull/12)

## v0.2.3
### Fixed
* Add support for Unicode in Python 2.7. [#9](https://github.com/contentful/rich-text-renderer.py/issues/9)

## v0.2.2
### Fixed
* Default `EntryBlockRenderer` now properly stringifies `data.target` instead of just data.

## v0.2.1

### Fixed
* Fixed Asset Hyperlink not respecting text from the node when link is not an Asset object.

## v0.2.0

### Added
* Add Asset support

## v0.1.0 (`rich_text_renderer`)

As `RichText` moves from `alpha` to `beta`, we're treating this as a feature release.

### Changed
* Renamed `StructuredText` to `RichText`.

## v0.0.2 (`structured_text_renderer`)

### Fixed
* Fixed rendering logic for block type nodes

## v0.0.1

* Initial Release
