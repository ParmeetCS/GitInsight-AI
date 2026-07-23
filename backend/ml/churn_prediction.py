import os
import joblib
import pandas as pd

class ChurnPredictor:

    def __init__(self, model_path="churn_model.pkl"):
        self.model = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_path = model_path
        if not os.path.isabs(model_path):
            if not os.path.exists(model_path):
                resolved_path = os.path.join(current_dir, model_path)
                if not os.path.exists(resolved_path):
                    workspace_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
                    resolved_path = os.path.join(workspace_root, model_path)

        if os.path.exists(resolved_path):
            try:
                self.model = joblib.load(resolved_path)
            except Exception:
                pass

    def rule_based_prediction(self, commits, contributors, merge_rate, releases, issues, closed_issues):
        score = 0
        if commits < 50:
            score += 1
        if contributors < 5:
            score += 1
        if merge_rate < 60:
            score += 1
        if releases < 2:
            score += 1

        resolution_rate = (closed_issues / issues * 100) if issues > 0 else 0
        if resolution_rate < 50:
            score += 1

        if score <= 1:
            return {"risk": "Low", "status": "Healthy Repository", "churn_probability": 10}
        elif score <= 3:
            return {"risk": "Medium", "status": "Repository Needs Attention", "churn_probability": 50}
        else:
            return {"risk": "High", "status": "Repository At Risk", "churn_probability": 90}

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
            return self.rule_based_prediction(commits, contributors, merge_rate, releases, issues, closed_issues)

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

        prediction = self.model.predict(data)[0]
        probability = self.model.predict_proba(data)[0][1]

        return {
            "prediction": int(prediction),
            "churn_probability": round(probability * 100, 2)
        }
