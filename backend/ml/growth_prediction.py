import os
import joblib
import pandas as pd

class GrowthPredictor:

    def __init__(self, model_path="growth_model.pkl"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_path = model_path
        if not os.path.isabs(model_path):
            if not os.path.exists(model_path):
                resolved_path = os.path.join(current_dir, model_path)
                if not os.path.exists(resolved_path):
                    workspace_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
                    resolved_path = os.path.join(workspace_root, model_path)

        self.model = None
        if os.path.exists(resolved_path):
            try:
                self.model = joblib.load(resolved_path)
            except Exception:
                pass

    def heuristic_predict(
        self,
        stars,
        forks,
        watchers,
        contributors,
        commits,
        issues,
        closed_issues,
        pull_requests,
        merged_prs,
        releases,
        merge_rate,
        community_engagement,
    ):
        score = 0.0
        score += min(contributors * 3.0, 30.0)
        score += min(commits * 0.1, 25.0)
        if pull_requests > 0:
            score += (merge_rate / 100.0) * 20.0
        popularity = (stars * 0.05) + (forks * 0.1)
        score += min(popularity, 15.0)
        score += min(releases * 2.0, 10.0)
        return round(max(min(score, 100.0), 5.0), 2)

    def predict(
        self,
        stars,
        forks,
        watchers,
        contributors,
        commits,
        issues,
        closed_issues,
        pull_requests,
        merged_prs,
        releases,
        merge_rate,
        community_engagement,
    ):
        if self.model is None:
            return self.heuristic_predict(
                stars, forks, watchers, contributors, commits, issues,
                closed_issues, pull_requests, merged_prs, releases,
                merge_rate, community_engagement
            )

        data = pd.DataFrame([{
            "stars": stars,
            "forks": forks,
            "watchers": watchers,
            "contributors": contributors,
            "commits": commits,
            "issues": issues,
            "closed_issues": closed_issues,
            "pull_requests": pull_requests,
            "merged_prs": merged_prs,
            "releases": releases,
            "merge_rate": merge_rate,
            "community_engagement": community_engagement
        }])

        try:
            prediction = self.model.predict(data)[0]
            return round(prediction, 2)
        except Exception:
            return self.heuristic_predict(
                stars, forks, watchers, contributors, commits, issues,
                closed_issues, pull_requests, merged_prs, releases,
                merge_rate, community_engagement
            )
