"""
Insight Flow — Analytics Engine
Handles KPI calculations, trend analysis, growth metrics, and aggregations.
All computations are deterministic — Gemini never calculates metrics.
"""
import pandas as pd
import numpy as np

class AnalyticsEngine:
    def __init__(self, df, date_col, numeric_cols, categorical_cols):
        self.df = df.copy()
        self.date_col = date_col
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols

    def compute_kpis(self, filtered_df=None):
        data = filtered_df if filtered_df is not None else self.df
        kpis = {}
        for col in self.numeric_cols:
            series = data[col].dropna()
            kpis[col] = {
                'total': round(float(series.sum()), 2),
                'mean': round(float(series.mean()), 2),
                'median': round(float(series.median()), 2),
                'std': round(float(series.std()), 2) if len(series) > 1 else 0,
                'min': round(float(series.min()), 2),
                'max': round(float(series.max()), 2),
                'count': int(series.count()),
            }
        return kpis

    def compute_growth(self, filtered_df=None, metric=None):
        data = filtered_df if filtered_df is not None else self.df
        if metric is None:
            metric = self.numeric_cols[0] if self.numeric_cols else None
        if metric is None or metric not in data.columns:
            return None
        monthly = data.set_index(self.date_col).resample('ME')[metric].sum()
        if len(monthly) < 2:
            return {'current': float(monthly.iloc[-1]) if len(monthly) > 0 else 0,
                    'previous': 0, 'growth_pct': 0, 'direction': 'neutral'}
        curr, prev = float(monthly.iloc[-1]), float(monthly.iloc[-2])
        pct = round(((curr - prev) / prev * 100), 2) if prev != 0 else 0
        return {'current': curr, 'previous': prev, 'growth_pct': pct,
                'direction': 'up' if pct > 0 else ('down' if pct < 0 else 'neutral')}

    def monthly_aggregation(self, filtered_df=None, metric=None):
        data = filtered_df if filtered_df is not None else self.df
        if metric is None:
            metric = self.numeric_cols[0]
        monthly = data.set_index(self.date_col).resample('ME')[metric].sum().reset_index()
        monthly.columns = [self.date_col, metric]
        monthly['month_label'] = monthly[self.date_col].dt.strftime('%b %Y')
        return monthly

    def weekly_aggregation(self, filtered_df=None, metric=None):
        data = filtered_df if filtered_df is not None else self.df
        if metric is None:
            metric = self.numeric_cols[0]
        weekly = data.set_index(self.date_col).resample('W')[metric].sum().reset_index()
        weekly.columns = [self.date_col, metric]
        weekly['week_label'] = weekly[self.date_col].dt.strftime('%d %b %Y')
        return weekly

    def category_breakdown(self, filtered_df=None, metric=None, category=None):
        data = filtered_df if filtered_df is not None else self.df
        if metric is None:
            metric = self.numeric_cols[0]
        if category is None:
            category = self.categorical_cols[0] if self.categorical_cols else None
        if category is None or category not in data.columns:
            return None
        return data.groupby(category)[metric].sum().reset_index().sort_values(by=metric, ascending=False)

    def best_worst_periods(self, filtered_df=None, metric=None):
        data = filtered_df if filtered_df is not None else self.df
        if metric is None:
            metric = self.numeric_cols[0]
        monthly = data.set_index(self.date_col).resample('ME')[metric].sum()
        if monthly.empty:
            return {'best': 'N/A', 'worst': 'N/A', 'best_value': 0, 'worst_value': 0}
        best_idx = monthly.idxmax()
        worst_idx = monthly.idxmin()
        return {
            'best': best_idx.strftime('%B %Y'), 'best_value': round(float(monthly.max()), 2),
            'worst': worst_idx.strftime('%B %Y'), 'worst_value': round(float(monthly.min()), 2),
        }

    def correlation_matrix(self, filtered_df=None):
        data = filtered_df if filtered_df is not None else self.df
        num_data = data[self.numeric_cols].dropna()
        if len(num_data.columns) < 2:
            return None
        return num_data.corr()

    def generate_summary_text(self, filtered_df=None):
        data = filtered_df if filtered_df is not None else self.df
        kpis = self.compute_kpis(data)
        periods = self.best_worst_periods(data)
        lines = [f"Dataset contains {len(data)} records from {data[self.date_col].min().strftime('%Y-%m-%d')} to {data[self.date_col].max().strftime('%Y-%m-%d')}."]
        for col, vals in kpis.items():
            lines.append(f"- {col}: Total={vals['total']:,.2f}, Avg={vals['mean']:,.2f}, Min={vals['min']:,.2f}, Max={vals['max']:,.2f}")
        prim = self.numeric_cols[0]
        growth = self.compute_growth(data, prim)
        if growth:
            lines.append(f"- {prim} Growth: {growth['growth_pct']}% ({growth['direction']})")
        lines.append(f"- Best Month: {periods['best']} ({periods['best_value']:,.2f})")
        lines.append(f"- Worst Month: {periods['worst']} ({periods['worst_value']:,.2f})")
        if self.categorical_cols:
            for cat in self.categorical_cols[:2]:
                breakdown = self.category_breakdown(data, prim, cat)
                if breakdown is not None and len(breakdown) > 0:
                    top = breakdown.iloc[0]
                    lines.append(f"- Top {cat}: {top[cat]} ({top[prim]:,.2f})")
        return "\n".join(lines)
