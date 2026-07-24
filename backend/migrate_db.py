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
    'ALTER TABLE releases DROP CONSTRAINT IF EXISTS releases_github_release_id_key;'
]

def run_migration():
    with engine.connect() as conn:
        for cmd in commands:
            try:
                conn.execute(text(cmd))
                conn.commit()
                print("Executed successfully:", cmd[:50])
            except Exception as e:
                print("Notice for", cmd[:30], ":", e)
    print("Database migration completed successfully!")

if __name__ == "__main__":
    run_migration()
