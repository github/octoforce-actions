const core = require("@actions/core");
const github = require("@actions/github");
const lodash = require("lodash");

(function start() {
  try {
    const issuePrefix = process.env?.ISSUE_PREFIX;
    const safeIssuePrefix = lodash.escapeRegExp(issuePrefix);
    let ref = process.env?.BRANCH_NAME;
    if (!ref) {
      ref = github.context.ref;
    }
    const branchName = ref.substring(ref.lastIndexOf("/") + 1);
    console.log(`branchName = ${branchName}`);
    core.setOutput("branchName", branchName);
    const re = new RegExp("^" + safeIssuePrefix + "(\\d+)");
    const prefixMatches = branchName.match(re);
    let matches = "false";
    let issueNumber = "";
    if (prefixMatches) {
      matches = "true";
      issueNumber = prefixMatches[1];
    }
    core.setOutput("matches", matches);
    core.setOutput("issueNumber", issueNumber);
    console.log(`matches = ${matches}; issueNumber = ${issueNumber}`);
  } catch (e) {
    core.setFailed(e.message);
  }
})();
