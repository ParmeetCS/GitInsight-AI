import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from database import engine
from sqlalchemy import text

commands = [
    'ALTER TABLE repositories ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE;',
    'ALTER TABLE repositories DROP CONSTRAINT IF EXISTS repositories_github_id_key;',
    'ALTER TABLE repositories DROP CONSTRAINT IF EXISTS repositories_full_name_key;',
    'ALTER TABLE commits DROP CONSTRAINT IF EXISTS commits_sha_key;',
    'ALTER TABLE issues DROP CONSTRAINT IF EXISTS issues_github_issue_id_key;',
    'ALTER TABLE pull_requests DROP CONSTRAINT IF EXISTS pull_requests_github_pr_id_key;',
    'ALTER TABLE releases DROP CONSTRAINT IF EXISTS releases_github_release_id_key;',
    'DROP INDEX IF EXISTS ix_repositories_github_id;',
    'DROP INDEX IF EXISTS ix_repositories_full_name;',
    'DROP INDEX IF EXISTS ix_commits_sha;',
    'DROP INDEX IF EXISTS ix_issues_github_issue_id;',
    'DROP INDEX IF EXISTS ix_pull_requests_github_pr_id;',
    'DROP INDEX IF EXISTS ix_releases_github_release_id;',
    'CREATE INDEX IF NOT EXISTS ix_repositories_github_id ON repositories (github_id);',
    'CREATE INDEX IF NOT EXISTS ix_repositories_full_name ON repositories (full_name);',
    'CREATE INDEX IF NOT EXISTS ix_commits_sha ON commits (sha);',
    'CREATE INDEX IF NOT EXISTS ix_issues_github_issue_id ON issues (github_issue_id);',
    'CREATE INDEX IF NOT EXISTS ix_pull_requests_github_pr_id ON pull_requests (github_pr_id);',
    'CREATE INDEX IF NOT EXISTS ix_releases_github_release_id ON releases (github_release_id);'
]

def run_migration():
    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                conn.commit()
                print("Executed successfully:", cmd[:60])
            except Exception as e:
                print("Notice for", cmd[:30], ":", e)
    print("Database migration completed successfully!")

if __name__ == "__main__":
    run_migration()
