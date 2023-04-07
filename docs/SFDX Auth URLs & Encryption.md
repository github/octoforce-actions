### SFDX Auth URL Encryption/Decryption

The octoforce-actions project leverages SFDX auth URLs that are stored within files in order to deploy changes to UAT sandboxes. These SFDX auth URLs are generated when you run `scripts/sandbox_auth`.

In order to safely store and use these SFDX auth URLs, we leverage the [`age` encryption tool](https://github.com/FiloSottile/age) to encrypt the file content using a public key and decrypt these files in our GitHub Actions using a private key. The public key is stored within our repository, and the private key is stored as a GitHub Action secret. In other words, everyone with access to the repo has the public key and can encrypt files that contain an SFDX auth URL, but the file can only be decrypted in execution of the appropriate GitHub Actions.

To generate `age` private and public keys, please follow these steps:
1. Install `age` if it is not already installed
1. Generate the public and private key:
   - `age-keygen -o key.txt`
1. Copy the public key that is printed in your terminal and replace the old public key with the new public key in the `auth/public-key.txt` file
1. Create or replace the value of the `SFDX_AUTH_SECRET_KEY` GitHub Action secret with the contents of the `key.txt` file you created in the first step
1. Securely remove the `key.txt` file you created in the first step from your machine
