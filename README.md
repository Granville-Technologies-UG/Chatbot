## Git Workflows

- production (Code pushed to production should have a tag)
  - hotfixes (branches that are quick fixes)
- staging (blue / green - duplicate of our production environment and if all tests pass we'll swap it with production)
- main (main branch where we are going to merge all our features)
  - features
- qa (perform tests before merging into staging)
