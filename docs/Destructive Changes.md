## Overview

### Steps Taken by the developer:

Delete Metadata files -> Add them to appropriate destructive package xmls in `destructive-changes` directory

### This causes the deploy actions to do the following:

Converts source code in `force-app/main/default` to Metadata API format and place files in `destructive-changes` directory -> deploy using Metadata API -> skip `force:source:deploy` -> On merge to master only: Removes `destructive-changes` directory and commits removal to master

## Step by Step Guide

1. Identify all files that need to be deleted or updated. When deleting a custom field or object this can be quite a lot of files since you need to delete profile level FLS, permissions, and any references to them in Apex, Flows, etc. Here are some general guidelines/tips:

   - You should be able to run the `retrieve` after deleting the metadata in setup to handle most of the file updates.
   - Removing the `force-app/main/default/profiles/decomposed` BEFORE running the `retrieve` script will ensure that what ends up in that
     directory is exactly what's in your org.
   - If you delete an entire object, doing a retrieve won't delete those object definition files.
     - E.G. If you delete an object called `My_Object__c`, retrieving won't delete `force-app/main/default/objects/My_Object__c/`

2. Build your destructive package xmls and place them in a folder called `destructive-changes`. The folder must be in the project root. This folder is removed automatically once destructive changes are deployed to prod, so you will most likely have to create the folder.

   - [Here is a link to the official documentation on creating destructive change package.xml files](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_deploy_deleting_files.htm)

3. Test whenever possible. If you deleted the metadata using Setup, consider refreshing your sandbox and manually running the deploy to your sandbox. To manually deploy to your issue sandbox you can run the following commands, replacing `*ISSUE_NUMBER*` with the sandbox issue number. If you've set a different alias for your sandbox, pass that to the `-u` flag instead. Be sure to cleanup the converted metadata when running these commands locally! You can quickly cleanup converted metadata by recursively removing untracked files with `git clean -fd`

```
sfdx force:source:convert -r ./force-app/main/default/ -d ./destructive-changes
sfdx force:mdapi:deploy -d destructive-changes/ -l RunLocalTests -w 200 -u issue-*ISSUE_NUMBER*
```

4. Check in your changes and the action workflows will take it from there.
