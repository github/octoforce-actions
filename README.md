## `octoforce-actions`

A lightweight open-source template Salesforce CI/CD built on the [`GitHub` actions platform](https://github.com/features/actions).

### Features

- Automation to create a development sandbox and UAT sandbox for each issue created.
- Automation to deploy metadata changes to UAT sandboxes for each pull request created against a release branch.
- Automation to compile release notes when changes are merged into a release branch.
- Automation to deploy changes to production.
- Support for including desctructive changes in deployments.
- Script to authenticate against sandboxes using `SFDX` and encrypt the credentials for use in GitHub Actions.
- Setup script for MacOS to setup `SFDX` and `NodeJS` as well other development dependencies.
- Basic Docker configuration for use in [`Codespaces`](https://github.com/features/codespaces).

### Limitations

- Setup script does not support Windows.
- The number of dev sandboxes you are entitled to will determine how many issues your team can work on simultaneously.

## Background

This project is meant to be a starting point for Salesforce developers who want to automate their CI/CD process using GitHub Actions. It is not meant to be a complete solution for all Salesforce development teams.

## Requirements

NodeJS 14.x is the minimum requirement for this project. More recent versions of NodeJS are still being tested. We are currently testing Node 18.x and have found issues with authentication against sandboxes using `SFDX` web auth flow.
The setup scripts require MacOS to run locally, however is not required to make use of this template.
The sandbox authentication script requires `SFDX` to be installed and configured and requires a bash environment.

These actions rely on several repository secrets and variables to be set in the repository settings. Please refer to the [Required Configurations](./docs/Getting%20Started.md#required-configurations) section of our getting started doc for more details.

Your team will be required to follow the dev flow outlined [here](docs/Dev_Flow.md) in order for the workflows in this repo to function as expected.

## Getting Started

See the [setup guide](docs/Getting%20Started.md).

## License

This project is licensed under the terms of the MIT open source license. Please refer to [MIT](./LICENSE.md) for the full terms.

## Maintainers

[Owners](./CODEOWNERS)

## Support

This template will receive basic maintenace such as bug fixes and security updates.

![GitHub Logo](./github-mark.png)
