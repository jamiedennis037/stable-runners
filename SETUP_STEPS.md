# Upcoming runners - GitHub setup (one time, about 10 minutes, same as the Breezers)

This repo only holds the public declared runners (horse, trainer, course, time).
No stable tour text or book text goes here.

1. GitHub > **+** > **New repository**. Name it exactly **stable-runners**. Public. Create.
2. **Add file > Upload files**. Drag in everything from this `github_runners` folder
   (`runners.py`, `index.html`, `SETUP_STEPS.md`, and the `.github` folder). Commit.
   If the `.github` folder doesn't upload: **Add file > Create new file**, name it
   `.github/workflows/runners.yml`, paste the contents of `runners.yml` from this folder, commit.
3. **Settings > Secrets and variables > Actions > New repository secret**, twice:
   - `RP_API_KEY` = the RP_TOURS_API_KEY value from your .env
   - `RP_JWT_KEY` = the RP_TOURS_JWT_KEY value from your .env
4. **Settings > Pages**: Deploy from a branch, `main`, `/ (root)`, Save.
5. **Actions > Refresh runners > Run workflow**. Wait for the green tick (a minute or two).

Done. It refreshes at 07:00, 11:00 and 16:00 UK time with your PC off, and the
Upcoming runners tab (local page and the shared link) reads from
https://jamiedennis037.github.io/stable-runners/
