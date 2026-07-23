from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RepositoryBase(BaseModel):
    owner: str
    name: str

class RepositoryResponse(RepositoryBase):
    id: int
    github_id: int
    full_name: str
    description: Optional[str] = None
    language: Optional[str] = None
    license: Optional[str] = None
    stars: int
    forks: int
    watchers: int
    open_issues: int
    default_branch: str
    html_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ContributorResponse(BaseModel):
    id: int
    github_id: int
    username: str
    contributions: int

    class Config:
        from_attributes = True

class CommitResponse(BaseModel):
    id: int
    sha: str
    message: str
    author_name: Optional[str]
    commit_date: datetime

    class Config:
        from_attributes = True

class IssueResponse(BaseModel):
    id: int
    github_issue_id: int
    title: str
    state: str
    created_at: datetime
    closed_at: Optional[datetime]

    class Config:
        from_attributes = True

class PullRequestResponse(BaseModel):
    id: int
    github_pr_id: int
    title: str
    state: str
    is_merged: bool
    created_at: datetime
    merged_at: Optional[datetime]

    class Config:
        from_attributes = True

class ReleaseResponse(BaseModel):
    id: int
    github_release_id: int
    tag_name: str
    release_name: Optional[str]
    published_at: Optional[datetime]

    class Config:
        from_attributes = True

class BranchResponse(BaseModel):
    id: int
    name: str
    protected: bool

    class Config:
        from_attributes = True

class TagResponse(BaseModel):
    id: int
    name: str
    commit_sha: str

    class Config:
        from_attributes = True

class LanguageResponse(BaseModel):
    id: int
    language: str
    bytes_of_code: int

    class Config:
        from_attributes = True

class RepositoryAnalyticsResponse(BaseModel):
    id: int
    health_score: float
    commit_frequency: float
    contributor_growth: float
    contributor_retention: float
    merge_rate: float
    issue_resolution_time: float
    average_pr_merge_time: float
    release_frequency: float
    community_engagement: float
    bus_factor: float

    class Config:
        from_attributes = True

class RepositoryRequest(BaseModel):
    owner: str
    repo: str

class RepositoryRefreshRequest(BaseModel):
    owner: str
    repo: str
