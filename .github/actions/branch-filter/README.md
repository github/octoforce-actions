# Branch Filter javascript action

This action tests whether the current branch name matches a pattern and outputs the related issue number.

## Inputs

### `issuePrefix`

**Required** The text that precedes issue numbers in issue-related, actionable branch names. Default `issue-`.

### 'branchName'

The name of the branch to be parsed. If ommitted, `github.context.ref` will be used.

## Outputs

### `matches`

Whether the branch name matches the pattern `${issuePrefix}/d+$`.

### `issueNumber`

The related issue number parsed from the branch name.

### `branchName`

The name of the current branch.

## Example usage

uses: actions/branch-filter@v1
with:
regex: '^issue-\d+$'
