GithubAdaptor Object Types
==========================

**All Objects Must Have An ID** (but it can be null)

### title
- `type`: `title`
- `body`: `title text would go here`
- `id`: Unsure, timestamp associated with the fetch is tempting. Leave None for now.

### body
- `type`: `body`
- `body`: `body of the issue goes here`
- `id`: Unsure, timestamp associated with the fetch is tempting. Leave None for now.

### comment
- `type`: `comment`
- `body`: `body of the comment`
- `id`: None
- `user`: `github username`
* created and updated timestamps currently discarded
