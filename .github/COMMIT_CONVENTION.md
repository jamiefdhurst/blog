# Commit Message Convention

This project uses a commit message convention to automatically determine version bumps and generate changelogs.

## Format

All commit messages must follow this format:

```
<type>[optional scope]: <description>
```

## Commit Types

### Version Bumps

These commit types will trigger a new release, and therefore a deployment to the live site:

| Type                        | Version Bump      | Description                    | Example                             |
| --------------------------- | ----------------- | ------------------------------ | ----------------------------------- |
| `feat:`, `feature:`, `add:` | **Minor** (0.X.0) | New articles, pages, features  | `feat: Add article on static sites` |
| `fix:`, `bug:`              | **Patch** (0.0.X) | Bug fixes, article corrections  | `fix: Correct broken article link`  |
| `update:`, `refactor:`      | **Patch** (0.0.X) | Code improvements              | `refactor: Simplify generator`      |
| `improve:`, `perf:`         | **Patch** (0.0.X) | Performance improvements       | `perf: Optimise image handling`     |
| `breaking:`, `major:`       | **Major** (X.0.0) | Breaking changes               | `breaking: Drop Python 3.12`        |
| `<type>!:`                  | **Major** (X.0.0) | Breaking change (conventional) | `feat!: Restructure templates`      |

### No Version Bump

These commit types will NOT trigger a release, so the live site will not be updated:

| Type              | Description             | Example                       |
| ----------------- | ----------------------- | ----------------------------- |
| `docs:`, `doc:`   | Documentation changes   | `docs: Update README`         |
| `test:`, `tests:` | Test changes only       | `test: Add generator tests`   |
| `chore:`          | Maintenance tasks       | `chore: Update dependencies`  |
| `build:`          | Build system changes    | `build: Update Docker config` |
| `ci:`             | CI/CD changes           | `ci: Add new workflow step`   |
| `style:`          | Code style/formatting   | `style: Reformat templates`   |
| `revert:`         | Revert previous commits | `revert: Revert feature X`    |

Note that `docs:` refers to project documentation such as the README — a new or
updated **article** is site content, so it should use `feat:` or `fix:` in order
to be published.

## Scopes (Optional)

You can add a scope to provide more context:

```
feat(articles): Add article on static sites
fix(templates): Resolve footer alignment
chore(deps): Update packages
```

## Examples

### Good Commit Messages

```
feat: Add article on cheap hosting
fix(articles): Correct dependency count in journal article
docs: Update development instructions
chore(deps): Bump jinja2 from 3.1.5 to 3.1.6
refactor: Extract markdown parsing logic
perf: Reduce generation time for article index
breaking: Remove support for Python 3.12
build: Update nginx config
ci: Add code coverage reporting
style: Tidy template indentation
revert: Revert "Add experimental feature"
```

### Bad Commit Messages (Will be Rejected)

```
Update files
WIP
quick fix
Fixed bug
Added feature
```

## Automatic Validation

Commit messages are validated in two places:

1. **Locally (git hook)**: When you commit, a git hook validates your message. If invalid, you'll see a helpful error message with examples. Enable the hooks once per clone with:

   ```bash
   git config core.hooksPath .githooks
   ```

2. **In CI (GitHub Actions)**: All commits in a pull request are validated using the same hook. The PR will fail if any commits don't follow the convention.

This ensures everyone follows the same standards, whether they have git hooks installed or not.

## Version Calculation

- Pull requests show a comment indicating what version bump will occur
- When merged to main, the version is automatically calculated, released and deployed
- Only commits with releasable types trigger new versions
- The version is written to `blog/config.py` and `setup.cfg`, and the changelog is generated into `CHANGELOG.md`

## Special Cases

- Merge commits are automatically skipped from validation
- `[skip ci]` commits (auto-generated) are skipped from validation
- Only non-releasable changes (docs/test/chore/build/ci/style/revert) won't trigger a release
- If a PR contains both releasable and non-releasable commits, a release will be triggered
- Dependabot is configured to use `chore(deps):` format automatically, so dependency updates do not deploy on their own
