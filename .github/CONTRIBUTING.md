# Contributing Guidelines

Thank you for your interest in contributing to our project. Whether it's a bug report, new feature, correction, or additional documentation, we greatly value feedback and contributions from our community.

Please read through this document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your bug report or contribution.

## Reporting Bugs/Feature Requests

We welcome you to use the GitHub issue tracker to report bugs or suggest features.

When filing an issue, please check existing open, or recently closed, issues to make sure somebody else hasn't already reported the issue. Please try to include as much information as you can. Details like these are incredibly useful:

- A reproducible test case or series of steps
- The version of our code that you're using
- Any pertinent information about your local environment

## Contributing via Pull Requests

Contributions via pull requests are much appreciated. Before sending us a pull request, please ensure that:

1. You are working against the latest source on the main branch.
2. You check existing open, and recently merged, pull requests to make sure someone else hasn’t addressed the problem already.
3. You open an issue to discuss any significant work - we would hate for your time to be wasted.

To send us a pull request, please:

1. Fork the repository.
2. Modify the source; please focus on the specific change you are contributing. If you also reformat all the code, it will be hard for us to focus on your change.
3. Ensure local tests pass.
4. Commit to your fork using clear commit messages.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification. This leads to more readable messages that are easy to follow when looking through the project history. If you're not familiar with the Conventional Commits specification, the following is an example of a commit message that uses the convention:

A commit message should be structured as follows:

```text
[optional scope]:

[optional body]

[optional footer(s)]
```

Here's an example:

```text
feat(user): add ability to delete account

This change allows the user to delete their account. Once the account is deleted, the user will be redirected to the homepage.

BREAKING CHANGE: The deleteUser function now takes two arguments. The second argument is a callback function.
```

The commit contains the following structural elements:

- **fix**: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in semantic versioning).
- **feat**: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in semantic versioning).
- **BREAKING CHANGE**: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in semantic versioning). A BREAKING CHANGE can be part of commits of any type.
- Others: commit types other than fix: and feat: are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.

If you are not familiar with the Conventional Commits specification, you can also install the [**Conventional Commits**](https://marketplace.visualstudio.com/items?itemName=vivaxy.vscode-conventional-commits) extension for Visual Studio Code. This extension provides a button in the Source Control view to commit staged changes following the Conventional Commits specification.

We also use the [semantic-release](https://github.com/semantic-release/semantic-release) tool for automatic version management and package publishing. It uses the commit messages to determine the type of changes in the codebase. Following formalized conventions for commit messages, semantic-release automatically determines the next semantic version number, generates a changelog and publishes the release to GitHub.

## Thank You

We greatly appreciate your effort towards improving our project. Each contribution helps make our project better. Thank you for taking the time to read these guidelines and we look forward to receiving your contributions.
