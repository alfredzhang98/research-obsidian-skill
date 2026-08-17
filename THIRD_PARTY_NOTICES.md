# Third-party notices

This repository contains integration instructions and patches for third-party
projects. The installers fetch those projects into a machine-local dependency
directory; their source code, credentials, virtual environments, and Git
history are not committed to this repository.

## paper-search-mcp

- Upstream: <https://github.com/openags/paper-search-mcp>
- Pinned revision: `d499d014db0cfe4b76328716788e5fb12fb80eed`
- License: MIT
- Copyright: 2025 OPENAGS

The upstream license is retained in the installed dependency checkout.

## claude-defuddle

- Upstream: <https://github.com/spaceage64/claude-defuddle>
- Pinned revision: `3610ca4fd8fc1b6d5d896cf0f3cabaac68951c45`
- License: MIT
- Copyright: 2026 spaceage64

The installer applies the small portability patch stored in
`integrations/claude-defuddle/portable.patch`. The upstream license is retained
in the installed skill directory.

## Python packages

The `paper-figures` installer creates an isolated environment containing
PyMuPDF and Pillow. These packages are not redistributed by this repository
and remain subject to their own licenses. Review their current license terms
before redistributing an environment or using it in a product.

