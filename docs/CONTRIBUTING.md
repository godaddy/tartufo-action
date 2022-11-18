## Issuing a New Release

While issuing a release please make sure the new tartufo-action version is in synchronization with [Tartufo][tartufo] released version.

This process is thankfully mostly automated. There are, however, a handful of manual steps that must be taken to kick
off that automation. It is all built this way to help ensure that issuing a release is a very conscious decision,
requiring peer review, and cannot easily happen accidentally. The steps involved currently are:

* Create a new branch locally for the release, for example:

  ```console
  > git checkout -b releases/v2.1.0
  ```

* Tell Poetry to [bump the version]:

  ```console
  > poetry version minor
  Bumping version from 2.0.1 to 2.1.0
  ```

  * Note: All this is doing, is updating the version number in the
    `pyproject.toml`. You can totally do this manually. This command just might be a bit quicker. And it's nice to
    have a command to do it for you. Yay automation!
* Update the CHANGELOG with the appropriate new version number and release date.
* Update the .pre-commit-config.yaml with new version.
* Update the Docker file to start using new tartufo version.
* Create a pull request for these changes, and get it approved!
* Once your PR has been merged, the final piece is to actually create the new release.

    1. Go to the `tartufo-action` [releases page][release-page] and click on `Draft a new release`.
    2. Enter an appropriate tag version (in this example, `v2.1.0`).
    3. Title the release. Generally these would just be in the form
       `Version 2.1.0`. (Not very creative, I know. But predictable!)
    4. Copy-paste the CHANGELOG entries for this new version into the description.
    5. Click `Publish release`!

Congratulations, you've just issued a new release for `tartufo-action`. The automation will take care of the rest! 🎉


[tartufo]: https://github.com/godaddy/tartufo/tags
[release-page]: https://github.com/godaddy/tartufo-action/releases
