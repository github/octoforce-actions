# Dev Flow
This project requires teams that use it to follow the following development flow.  This assumes you have already followed the [setup guide](./Getting%20Started.md) and have a fully-configured, working project.

1. Developer creates a new branch for an issue.  This will kick off the project's first workflow, which will provision dev and UAT sandboxes for the issue.
2. Once the sandboxes have been provisioned, check out the issue branch locally and run the `scripts/sandbox_auth` script.  This will prompt the developer to authenticate to both the dev and uat sandboxes and will generate a ".age" file that should be committed to the repo.
3. Solve the issue in your dev sandbox.  Development may be done using the admin interface or via vscode.  Once development is complete, run the `scripts/retrieve` script to retrieve your changes.  The retrieve script is a thin wrapper around the `sfdx force:source:retrieve` 
command, so pass whichever arguments you would normally pass to that command to the retrieve script.  
E.g., `scripts/retrieve -u issue-100 -x package.xml` would retrieve from the sandbox with alias "issue-100" using your package.xml file to determine which metadata resources to retrieve.
4. Once you're satisfied with your development work and have retrieved your latest metadata, commit your new/modified metadata to the issue branch and push it to the remote repo.
5. Open a pull request against a release branch.  At this point, a second workflow will fire, which will deploy your pull request to your UAT sandbox.
6. Test your changes in the UAT sandbox where they were just deployed.
7. Once testing is complete, have your pull request reviewed and merge it to the release branch.
8. Once the pull requests for all of the issues in your release have been merged, merge your release branch to your main branch.  This will execute the final workflow, which deploys your release branch to your production org and then to your template org.  A release will also be created in your repo.
