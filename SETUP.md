# Publish your GitHub profile (Jad-RAMOSS)

This package creates the root README and original animated artwork for your **public profile repository**. There is no need to expose or connect any private organization repository.

## What goes public

- `README.md`: public profile, open projects, and deliberately anonymized engineering cases.
- `assets/hero.svg`: original animated header and monogram.
- `assets/capabilities.svg`: original animated symbols for intelligence, infrastructure, and digital craft.
- `assets/workflow-demo.svg`: conceptual illustration; **not** production architecture.
- `assets/contribution-signal.svg`: starter card; the scheduled workflow replaces it after first run.
- `.github/workflows/contribution-signal.yml`: public GitHub Actions workflow.
- `scripts/generate_signal.py`: pure Python calendar-to-SVG generator.

No company access tokens, internal endpoints, private repository URLs, customer information, or real transaction data are included.

## Exact steps: first-time publishing from your Mac

1. Sign in to **https://github.com/Jad-RAMOSS**.
2. Open **https://github.com/new**. Under owner **Jad-RAMOSS**, enter repository name **Jad-RAMOSS** (exact match, including spelling and capitalization). Choose **Public** and leave **Add a README**, `.gitignore`, and **License** unselected, then click **Create repository**.
3. Download `jad-github-profile.zip` and unzip it. Open Terminal in the extracted `jad-github-profile` directory (Finder > right-click folder > Services > New Terminal at Folder), or `cd` to it manually.
4. Run the commands below in the extracted folder (where `README.md` and `assets/` are directly visible):

   ```bash
   git init
   git branch -M main
   git add .
   git commit -m "feat: launch GitHub profile"
   git remote add origin https://github.com/Jad-RAMOSS/Jad-RAMOSS.git
   git push -u origin main
   ```

   If Git says it needs a username/email for commits, configure your own Git author identity first. If push authentication fails, sign in with GitHub Desktop or `gh auth login` (GitHub CLI) and repeat `git push -u origin main`; GitHub no longer accepts account passwords as Git credentials.

5. Visit **https://github.com/Jad-RAMOSS** and hard-refresh if needed. GitHub should render the root README because the repo is public and its name exactly matches your username.
6. Open **https://github.com/Jad-RAMOSS/Jad-RAMOSS/actions**, choose **Update contribution signal**, and click **Run workflow** on branch **main**.
7. After the workflow completes successfully, return to your profile. `assets/contribution-signal.svg` will be regenerated from GitHub's contribution calendar. It will also refresh automatically each day (scheduled GitHub Actions workflows can sometimes be delayed).
8. If the workflow reports `Resource not accessible by integration` / push denied, go to the profile repository **Settings → Actions → General → Workflow permissions** and select **Read and write permissions**, if your account lets you change it. The workflow itself also declares `contents: write`.
9. Optional: visit your profile, click **Customize your pins**, and pin `qwen2.5-VL-inference-openai`, `hr_dashboard`, and `ForgeAI_Identity`.

## Important GitHub/animation notes

- SVG animations are rendered as ordinary images. Some browsers, themes, reduced-motion settings, and GitHub renderers may display a static frame; all visuals have readable static content.
- The contribution workflow uses `GITHUB_TOKEN` supplied automatically by GitHub Actions. **Do not create or paste a personal access token.**
- The activity visualization uses the user's contribution calendar **levels**, not private repo names or commit messages. The GitHub API controls how private contributions are represented. The generated SVG avoids individual repository details.
- The workflow does not inspect any work organization's code and does not need org access.
- Before publishing, review the anonymized project summaries with your employer's confidentiality policy. These are high-level capability descriptions, not direct disclosures from inaccessible org repositories.

## Updating later

After editing locally:

```bash
git add .
git commit -m "docs: refine profile"
git push
```

The profile updates when GitHub receives the new `README.md` and SVG assets. You do not need to run the animation workflow after ordinary README edits.
