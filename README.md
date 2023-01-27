## `octoforce-actions`

A lightweight open-source template Salesforce CI/CD built on the [`GitHub` actions platform](https://github.com/features/actions).

### Features

- Automation to create a development sandbox and UAT sandbox for each issue created.
- Automation to deploy metadata changes to UAT sandboxes for each pull request created against a release branch.
- Automation to compile release notes when changes are merged into a release branch.
- Script to authenticate against sandboxes using `SFDX` and encrypt the credentials for use in GitHub Actions.
- Setup script for MacOS to setup `SFDX` and `NodeJS` as well other development dependencies.
- Basic Docker for configuration for use in [`Codespaces`](https://github.com/features/codespaces).

### Limitations

- No automation to deploy changes to production.
- Setup script does not support Windows.

## Background

This project is meant to be helpful guide and starting for Salesforce developers who want to automate their CI/CD process using GitHub Actions. It is not meant to be a complete solution for all Salesforce development teams.

## Requirements

NodeJS 14.x is the minimum requirement for this project. More recent versions of NodeJS are still being tested. We are currently testing Node 18.x and have found issues with authentication against sandboxes using `SFDX` web auth flow.
The setup scripts require MacOS to run locally, however is not required to make use of this template.
The sandbox authentication script requires `SFDX` to be installed and configured and requires a bash environment.

## License

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE.md) for the full terms.

## Maintainers

[Owners](./CODEOWNERS)

## Support

This template will receive basic maintenace such as bug fixes and security updates.

![GitHub Logo](./github-mark.png)
