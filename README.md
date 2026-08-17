# Doctor of Credit archive

Daily snapshots of selected [Doctor of Credit](https://www.doctorofcredit.com/) pages (main content only).

## Current page

- Source: https://www.doctorofcredit.com/high-interest-savings-to-get/
- Archive file: [`archive/high-interest-savings-to-get.html`](archive/high-interest-savings-to-get.html)

## Local run

```bash
pip install -r requirements.txt
python scripts/archive_page.py
```

## GitHub Actions

Workflow: [`.github/workflows/archive.yml`](.github/workflows/archive.yml)

- Runs daily (12:00 UTC)
- Also runnable manually: **Actions → Archive Doctor of Credit page → Run workflow**

On change, the workflow commits and pushes updates to `archive/*`.
