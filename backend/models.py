from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime
)

from sqlalchemy.orm import relationship

from database import Base


class Repository(Base):
    __tablename__ = "repositories"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # GitHub Information
    github_id = Column(Integer, unique=True, nullable=False, index=True)

    owner = Column(String(100), nullable=False)

    name = Column(String(200), nullable=False)

    full_name = Column(String(255), unique=True, nullable=False)

    description = Column(Text)

    language = Column(String(100))

    license = Column(String(100))

    stars = Column(Integer, default=0)

    forks = Column(Integer, default=0)

    watchers = Column(Integer, default=0)

    open_issues = Column(Integer, default=0)

    default_branch = Column(String(100))

    html_url = Column(String(500))

    # GitHub Dates
    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # -----------------------------
    # Relationships
    # -----------------------------

    contributors = relationship(
        "Contributor",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    commits = relationship(
        "Commit",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    issues = relationship(
        "Issue",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    pull_requests = relationship(
        "PullRequest",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    releases = relationship(
        "Release",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    branches = relationship(
        "Branch",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    tags = relationship(
        "Tag",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    languages = relationship(
        "Language",
        back_populates="repository",
        cascade="all, delete-orphan"
    )

    analytics = relationship(
        "RepositoryAnalytics",
        back_populates="repository",
        uselist=False,
        cascade="all, delete-orphan"
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship

from database import Base

class Contributor(Base):
    __tablename__ = "contributors"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # GitHub Information
    github_id = Column(Integer, unique=True, nullable=False, index=True)

    username = Column(String(100), nullable=False, index=True)

    profile_url = Column(String(500))

    avatar_url = Column(String(500))

    account_type = Column(String(50))      # User / Organization / Bot

    site_admin = Column(Boolean, default=False)

    # Contribution Statistics
    contributions = Column(Integer, default=0)

    followers = Column(Integer, default=0)

    following = Column(Integer, default=0)

    public_repos = Column(Integer, default=0)

    public_gists = Column(Integer, default=0)

    # Profile Information
    company = Column(String(255))

    location = Column(String(255))

    email = Column(String(255))

    blog = Column(String(500))

    bio = Column(Text)

    twitter_username = Column(String(100))

    # GitHub Dates
    github_created_at = Column(DateTime)

    github_updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="contributors"
    )

class Commit(Base):
    __tablename__ = "commits"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # GitHub Commit Details
    sha = Column(String(100), unique=True, nullable=False, index=True)

    author_name = Column(String(255))

    author_username = Column(String(255))

    committer_name = Column(String(255))

    committer_username = Column(String(255))

    message = Column(Text)

    url = Column(String(500))

    html_url = Column(String(500))

    comments_url = Column(String(500))

    # Dates
    commit_date = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="commits"
    )
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean
)
from sqlalchemy.orm import relationship

from database import Base


class Issue(Base):
    __tablename__ = "issues"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # GitHub Issue Details
    github_issue_id = Column(Integer, unique=True, nullable=False, index=True)

    issue_number = Column(Integer, nullable=False)

    title = Column(String(500), nullable=False)

    body = Column(Text)

    state = Column(String(50))          # open / closed

    state_reason = Column(String(100))

    author = Column(String(255))

    assignee = Column(String(255))

    labels = Column(Text)               # Store as comma-separated string or JSON

    comments = Column(Integer, default=0)

    locked = Column(Boolean, default=False)

    url = Column(String(500))

    html_url = Column(String(500))

    # Dates
    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    closed_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="issues"
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class PullRequest(Base):
    __tablename__ = "pull_requests"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # GitHub PR Details
    github_pr_id = Column(Integer, unique=True, nullable=False, index=True)

    pr_number = Column(Integer, nullable=False)

    title = Column(String(500), nullable=False)

    body = Column(Text)

    state = Column(String(50))          # open / closed

    author = Column(String(255))

    is_draft = Column(Boolean, default=False)

    is_merged = Column(Boolean, default=False)

    merge_commit_sha = Column(String(100))

    commits = Column(Integer, default=0)

    additions = Column(Integer, default=0)

    deletions = Column(Integer, default=0)

    changed_files = Column(Integer, default=0)

    comments = Column(Integer, default=0)

    review_comments = Column(Integer, default=0)

    url = Column(String(500))

    html_url = Column(String(500))

    # Dates
    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    closed_at = Column(DateTime)

    merged_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="pull_requests"
    )

    from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class Release(Base):
    __tablename__ = "releases"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # GitHub Release Details
    github_release_id = Column(Integer, unique=True, nullable=False, index=True)

    tag_name = Column(String(100), nullable=False)

    name = Column(String(255))

    body = Column(Text)

    author = Column(String(255))

    draft = Column(Boolean, default=False)

    prerelease = Column(Boolean, default=False)

    is_latest = Column(Boolean, default=False)

    tarball_url = Column(String(500))

    zipball_url = Column(String(500))

    html_url = Column(String(500))

    # Dates
    published_at = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="releases"
    )
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class Branch(Base):
    __tablename__ = "branches"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # Branch Details
    name = Column(String(255), nullable=False)

    protected = Column(Boolean, default=False)

    last_commit_sha = Column(String(100))

    last_commit_url = Column(String(500))

    # Dates
    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="branches"
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class Tag(Base):
    __tablename__ = "tags"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # Tag Details
    name = Column(String(255), nullable=False)

    commit_sha = Column(String(100), nullable=False)

    commit_url = Column(String(500))

    zipball_url = Column(String(500))

    tarball_url = Column(String(500))

    node_id = Column(String(255))

    # Dates
    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="tags"
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    BigInteger,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class Language(Base):
    __tablename__ = "languages"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False
    )

    # Language Details
    language_name = Column(String(100), nullable=False)

    bytes_of_code = Column(BigInteger, default=0)

    percentage = Column(Integer, default=0)   # Calculated later

    # Dates
    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="languages"
    )

from sqlalchemy import (
    Column,
    Integer,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.orm import relationship

from database import Base


class RepositoryAnalytics(Base):
    __tablename__ = "repository_analytics"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    repository_id = Column(
        Integer,
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # Health Metrics
    health_score = Column(Float, default=0.0)

    commit_frequency = Column(Float, default=0.0)

    contributor_growth = Column(Float, default=0.0)

    contributor_retention = Column(Float, default=0.0)

    merge_rate = Column(Float, default=0.0)

    issue_resolution_time = Column(Float, default=0.0)

    average_pr_merge_time = Column(Float, default=0.0)

    release_frequency = Column(Float, default=0.0)

    community_engagement = Column(Float, default=0.0)

    bus_factor = Column(Float, default=0.0)

    # Metadata
    last_calculated = Column(DateTime)

    created_at = Column(DateTime)

    updated_at = Column(DateTime)

    # Relationship
    repository = relationship(
        "Repository",
        back_populates="analytics"
    )