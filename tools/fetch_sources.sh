#!/bin/sh
# Download the 29 source PDFs and the app's index from the GitHub release and verify them.
# Needs the GitHub CLI (gh); run from the repository root.
set -e
TAG=${1:-sources-v1}
gh release download "$TAG" --repo bthar-mx/tipitaka-abhidhana --pattern '*.pdf' --dir pdfs --skip-existing
gh release download "$TAG" --repo bthar-mx/tipitaka-abhidhana --pattern '*.db'  --dir db   --skip-existing
(cd pdfs && shasum -a 256 -c SHA256SUMS)
(cd db   && shasum -a 256 -c SHA256SUMS)
