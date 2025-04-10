# scripts/generate_structured_data.py
import json

def generate_smartcloud_ai_schema():
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "SmartCloud AI",
        "description": "Plateforme d'intelligence artificielle cloud pour entreprises",
        "operatingSystem": "Web",
        "applicationCategory": "BusinessApplication",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "42"
        }
    }
    
    with open('templates/structured_data.json', 'w') as f:
        json.dump(schema, f, indent=2)
    
    print("Structured data template generated")

if __name__ == "__main__":
    generate_smartcloud_ai_schema()