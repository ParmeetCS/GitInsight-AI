from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
    Float
)
from sqlalchemy.orm import relationship
from database import Base

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(BigInteger, unique=True, nullable=False, index=True)
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
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    contributors = relationship("Contributor", back_populates="repository", cascade="all, delete-orphan")
    commits = relationship("Commit", back_populates="repository", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="repository", cascade="all, delete-orphan")
    pull_requests = relationship("PullRequest", back_populates="repository", cascade="all, delete-orphan")
    releases = relationship("Release", back_populates="repository", cascade="all, delete-orphan")
    branches = relationship("Branch", back_populates="repository", cascade="all, delete-orphan")
    tags = relationship("Tag", back_populates="repository", cascade="all, delete-orphan")
    languages = relationship("Language", back_populates="repository", cascade="all, delete-orphan")
    analytics = relationship("RepositoryAnalytics", back_populates="repository", uselist=False, cascade="all, delete-orphan")

class Contributor(Base):
    __tablename__ = "contributors"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    github_id = Column(BigInteger, nullable=False, index=True)
    username = Column(String(100), nullable=False, index=True)
    profile_url = Column(String(500))
    avatar_url = Column(String(500))
    account_type = Column(String(50))
    site_admin = Column(Boolean, default=False)
    contributions = Column(Integer, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    public_repos = Column(Integer, default=0)
    public_gists = Column(Integer, default=0)
    company = Column(String(255))
    location = Column(String(255))
    email = Column(String(255))
    blog = Column(String(500))
    bio = Column(Text)
    twitter_username = Column(String(100))
    github_created_at = Column(DateTime)
    github_updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="contributors")

class Commit(Base):
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    sha = Column(String(100), unique=True, nullable=False, index=True)
    author_name = Column(String(255))
    author_username = Column(String(255))
    committer_name = Column(String(255))
    committer_username = Column(String(255))
    message = Column(Text)
    url = Column(String(500))
    html_url = Column(String(500))
    comments_url = Column(String(500))
    commit_date = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="commits")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    github_issue_id = Column(BigInteger, unique=True, nullable=False, index=True)
    issue_number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    body = Column(Text)
    state = Column(String(50))
    state_reason = Column(String(100))
    author = Column(String(255))
    assignee = Column(String(255))
    labels = Column(Text)
    comments = Column(Integer, default=0)
    locked = Column(Boolean, default=False)
    url = Column(String(500))
    html_url = Column(String(500))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    closed_at = Column(DateTime)

    repository = relationship("Repository", back_populates="issues")

class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    github_pr_id = Column(BigInteger, unique=True, nullable=False, index=True)
    pr_number = Column(Integer, nullable=False)
    title = Column(String(500), nullable=False)
    body = Column(Text)
    state = Column(String(50))
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
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    closed_at = Column(DateTime)
    merged_at = Column(DateTime)

    repository = relationship("Repository", back_populates="pull_requests")

class Release(Base):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    github_release_id = Column(BigInteger, unique=True, nullable=False, index=True)
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
    published_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="releases")

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    protected = Column(Boolean, default=False)
    last_commit_sha = Column(String(100))
    last_commit_url = Column(String(500))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="branches")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    commit_sha = Column(String(100), nullable=False)
    commit_url = Column(String(500))
    zipball_url = Column(String(500))
    tarball_url = Column(String(500))
    node_id = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="tags")

class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    language_name = Column(String(100), nullable=False)
    bytes_of_code = Column(BigInteger, default=0)
    percentage = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="languages")

class RepositoryAnalytics(Base):
    __tablename__ = "repository_analytics"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, unique=True)
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
    last_calculated = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    repository = relationship("Repository", back_populates="analytics")