# scripts/content_optimizer.py
import pandas as pd
from openai import OpenAI
import markdown
import json

class ContentOptimizer:
    def __init__(self):
        self.keywords = [
            "intelligence artificielle cloud",
            "plateforme IA SaaS",
            "automatisation intelligente",
            "analyse prédictive",
            "solution IA entreprise"
        ]
        
    def analyze_content(self, audit_file='seo_audit_results.csv'):
        df = pd.read_csv(audit_file)
        recommendations = []
        
        for _, row in df.iterrows():
            rec = {
                'url': row['url'],
                'issues': []
            }
            
            # Title analysis
            if row['title'] == 'MISSING':
                rec['issues'].append("Missing title tag")
            elif len(row['title']) > 60:
                rec['issues'].append(f"Title too long ({row['title_length']} chars)")
                
            # Meta description analysis
            if row['meta_description'] == 'MISSING':
                rec['issues'].append("Missing meta description")
            elif len(row['meta_description']) < 50 or len(row['meta_description']) > 160:
                rec['issues'].append(
                    f"Meta description length inadequate ({row['meta_desc_length']} chars)"
                )
                
            # Heading analysis
            if row['h1_count'] == 0:
                rec['issues'].append("Missing H1 tag")
            elif row['h1_count'] > 1:
                rec['issues'].append(f"Multiple H1 tags ({row['h1_count']})")
                
            # Image optimization
            if row['images_missing_alt'] > 0:
                rec['issues'].append(
                    f"{row['images_missing_alt']} images missing alt text"
                )
                
            if row['lazy_loading'] < row['image_count']:
                rec['issues'].append(
                    f"Consider adding lazy loading to {row['image_count'] - row['lazy_loading']} images"
                )
                
            if len(rec['issues']) > 0:
                recommendations.append(rec)
        
        self.generate_report(recommendations)
        return recommendations
    
    def generate_report(self, recommendations):
        md_content = "# SEO Content Recommendations\n\n"
        md_content += "Generated on: {}\n\n".format(pd.Timestamp.now().strftime('%Y-%m-%d'))
        
        for rec in recommendations:
            md_content += f"## Page: [{rec['url']}]({rec['url']})\n"
            md_content += "### Issues found:\n"
            for issue in rec['issues']:
                md_content += f"- {issue}\n"
            
            md_content += "\n### Suggested optimizations:\n"
            md_content += self.generate_optimization_suggestions(rec)
            md_content += "\n---\n"
        
        with open('content_recommendations.md', 'w') as f:
            f.write(md_content)
    
    def generate_optimization_suggestions(self, page_data):
        suggestions = []
        
        if "Missing title tag" in page_data['issues']:
            suggestions.append(
                "Add a compelling title tag (50-60 chars) including primary keywords"
            )
        
        if "Missing meta description" in page_data['issues']:
            suggestions.append(
                "Craft a persuasive meta description (150-160 chars) with value proposition"
            )
        
        if "Missing H1 tag" in page_data['issues']:
            suggestions.append(
                "Add a clear H1 tag that matches search intent and includes keywords"
            )
        
        if any(img_issue in page_data['issues'] for img_issue in ["images missing alt text", "lazy loading"]):
            suggestions.append(
                "Optimize images by adding descriptive alt text and implementing lazy loading"
            )
        
        return "\n".join(f"- {suggestion}" for suggestion in suggestions)

if __name__ == "__main__":
    optimizer = ContentOptimizer()
    optimizer.analyze_content()