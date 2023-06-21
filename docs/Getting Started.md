## Setup Guide

### Preliminary decisions
Before you begin setting up your new project, you'll need to make a few important decisions about how you use this project and set some repo variables accordingly.

#### Branch naming conventions
The workflows in this repo execute only on branches whose names match certain user-configurable patterns. For example, when issue branches are created, dev and UAT sandboxes will be created. And when pull requests are opened against a release branch, the pull request will be deployed to a UAT org. Therefore, you'll need to decide upon the branch name prefixes that those workflows will use to identify issue and release branches. Once you've decided on your naming conventions, you'll need to set repository variables to store the branch prefixes. If you're unsure what values to use, we recommend the following:
| Branch type | Prefix | Repo variable name |
| ----------- | ------ | ------------------ |
| Issue       | issue- | ISSUE_BRANCH_PREFIX |
| Release     | REL-   | RELEASE_BRANCH_PREFIX |

#### Profile and permissionset format
If enabled in this project, an [sfdx plugin](https://www.npmjs.com/package/@rdietrick/sfdx-profile-decompose) can translate monolithic Salesforce profiles and permissionsets into more granular XML files in your project. We've found that this makes managing diffs and conflict resolution in these files much easier. When the plugin is enabled, each profile will, for instance, be broken down into separate files for each object that the profile maintains FLS for. To turn it on, set the repository variable `SALESFORCE_FORMATTED_PROFILES_AND_PERMS` to true. If the plugin is disabled, you will also need to remove or comment out the line in `scripts/retrieve` that executes the profiles:decompose plugin. If you choose to store only profiles or only permissionsets in your repo but wish to use this plugin, you'll need to pass the `--md-types=profiles` or `--md-types=permissionsets` argument to the profiles:decompose command in the retrieve script.

#### Release tracking
If enabled, each time a release branch is merged to your main branch, a [release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository) will be automatically created in your repo with release notes for each issue included in the release. To turn this on, set the repository variable `GENERATE_RELEASE` to `true`.

### Setup

These step-by-step instructions will walk you through your initial project setup. At the end of this process, you should have a fully functioning deploy chain from UAT to production to template and your repo will contain all of the Salesforce metadata you wish to track in version control.

1. [Create a new repository](https://github.com/new?owner=&template_name=octoforce-actions&template_owner=github) from this repo. Check out your new repo locally.
2. If you haven't already, [enable DevHub](https://help.salesforce.com/s/articleView?id=sf.sfdx_setup_enable_devhub.htm&type=5) in your production Salesforce org. Workflows in this repo will use your org's DevHub to provision development and test sandboxes for your project.
3. Create (or repurpose an existing) an admin user in your production org that will be used for deployments and sandbox provisioning. Store the username of this user in a repo secret named `SALESFORCE_PROD_USERNAME`.
4. Create a [private key and certificate for use in the app you'll create in the next step](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_auth_key_and_cert.htm)
5. Create a connected app in your production Salesforce org for the octoforce CI/CD application that will be provisioning sandboxes and deploying to production.
    - Name your app 'octoforce' or something similar.
    - Set the `Permitted Users` field to "Admin approved users are pre-authorized"
    - Relax IP restrictions
    - Check the "Enable OAuth Settings" field and grant the app the following permissions:
      - Perform requests at any time
      - Manage user data via APIs
    - For the Callback URL field, enter https://localhost
    - Grant the "system administrator" profile (or whichever profile the user designated in step 3 is assigned) access to the new connected app
    - Store the following secrets in your repo:
      - `SALESFORCE_JWT_KEY` - use the contents of the server.key file generated in step 4 above
      - `SALESFORCE_PROD_CLIENT_ID` - use the Consumer Key of the connected app you just created
6. Clone your production org to create a sandbox named "template". This is the org that will be cloned to create your dev and uat sandboxes.
7. When your newly created template sandbox is provisioned, configure it identically to how you did in step 5 above. You can use the same certificate and key pair or generate new ones. Create two repo secrets with the following values from your template sandbox:
    - `SALESFORCE_TEMPLATE_CLIENT_ID` - use the consumer key of the octoforce connected app replicated from production to your template sandbox
    - `SALESFORCE_TEMPLATE_JWT_SECRET_KEY` - use the value of the server.key file related to your template certificate
    - `SALESFORCE_TEMPLATE_USERNAME` - use the username of the salesforce admin user replicated in your template sandbox
9. [Follow these directions](https://github.com/github/octoforce-actions/blob/add-setup-docs/docs/SFDX%20Auth%20URLs%20%26%20Encryption.md) to generate and store your age encryption keys. Be sure to store the generated private key in the `SFDX_AUTH_SECRET_KEY` repo secret and to replace the contents of `auth/public-key.txt`.
10. Create a GitHub PAT with "repo" scope and store its value as a secret in your repo with the key `SCOPED_PAT`.
11. Configure the repository variables listed at the bottom of this document to your liking.
12. Create a release branch in line with the release branch naming strategy you've decided upon.
13. In your local copy of your new repo, run the `scripts/setup` script to install all required plugins.
14. Import your Salesforce org's metadata into your repo:
    - Create an issue to import your Salesforce metadata into your repo.
    - Create a new branch for your issue, following the issue branch naming convention (e.g., issue-1 for your repo). **Wait for your dev and uat sandboxes to be fully provisioned before proceeding.**
    - Check out your new issue branch locally and run the `scripts/sandbox_auth` script. You will be prompted to log into your newly created dev and uat sandboxes.
    - Commit the newly created `.age` file to your repo.
    - If you are are tracking profiles and/or permissionsets in your repo and wish to use the `profiles:decompose` plugin, you will need to:
      - Uncomment the following lines in .gitignore 
        - force-app/main/default/profiles/*-meta.xml
        - force-app/main/default/permissionsets/*-meta.xml
      - Run the following command: `mkdir -p force-app/main/default/profiles/decomposed force-app/main/default/permissionsets/decomposed`
    - Adjust your package.xml file accordingly, so that it includes all of the metadata types you wish to store in your project.
    - Retrieve your metadata with `scripts/retrieve -u issue-# -x package.xml` (replacing "issue-#" with the correct issue branch prefix and issue number)
    - Add your org's metadata to your repo with the following git commands:
        - `git add force-app`
        - `git commit -m "initial metadata import"`
        - `git push origin`
    - Open a pull request for your issue branch against your release branch. A workflow will attempt to deploy your PR to the UAT org for your issue. You may need to refine your package.xml and .forceignore files and re-retrieve your org's metadata to get your deployment to pass.
15. Once your UAT deployment passes, you can merge the pull request created above and create and merge a new pull request that merges your release branch to your main branch. This will deploy your metadata to your production org.

Consult the [dev flow](./Dev_Flow.md) documentation to learn how your team should use this project once it has been set up.


## Required Configurations

### Secrets

The following secrets are required to be set in the repository settings:

- `SCOPED_PAT`
  - This is a personal access token with the `repo` scope. This is used to checkout the repository and push any changes.
- `SALESFORCE_JWT_KEY`
  - This is the private key used to generate the JWT token. This is used to authenticate with Salesforce production.
- `SALESFORCE_PROD_CLIENT_ID`
  - This is the client ID used to generate the JWT token. This is used to authenticate with Salesforce production.
- `SALESFORCE_PROD_USERNAME`
  - This is the username of the admin user of your DevHub/production org. This is used to authenticate with Salesforce production.
- `SALESFORCE_TEMPLATE_CLIENT_ID`
  - This is the consumer key of the template org. This is used to authenticate with the template sandbox.
- `SALESFORCE_TEMPLATE_USERNAME`
  - This is the username of the template org. This is used to authenticate with the template sandbox.
- `SALESFORCE_TEMPLATE_JWT_SECRET_KEY`
  - This is the private key used to generate the JWT token. This is used to authenticate with the template sandbox.
- `SFDX_AUTH_SECRET_KEY`
  - This is the age private key used to encrypt sfdx auth URLs. The encrypted sfdx auth URLs are required to deploy pull requests to UAT sandboxes and are generated by running `scripts/sandbox_auth`. Please see [SFDX Auth URLs & Encryption.md](SFDX%20Auth%20URLs%20%26%20Encryption.md) for more information.

### Repository Variables

The following repository variables are required to be set in the repository settings:

- `ISSUE_BRANCH_PREFIX`
  - This is the prefix used for issue branches. This is used to identify branches that require a sandbox.
- `RELEASE_BRANCH_PREFIX`
  - This is the prefix used for the release branch. This is used to identify branches where pull requests should be deployed to test sandbox.
- `GENERATE_RELEASE`
  - This is a boolean feature flag that determines whether release notes should be generated.
- `SALESFORCE_FORMATTED_PROFILES_AND_PERMS`
  - This is a feature flag that is a boolean value that determines whether profiles and permissions should be formatted using the `profile:decompose` plugin.
- `DEPLOYMENT_TIMEOUT`
  - The number of minutes to wait for the `force:source:deploy` command to complete and display results.
