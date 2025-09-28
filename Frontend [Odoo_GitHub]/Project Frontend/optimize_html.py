from bs4 import BeautifulSoup

# Load and optimize your HTML
with open("creative_platform.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Minify and clean code
optimized_html = soup.prettify().replace("\n", "").strip()

# Save the changes
with open("optimized_creative_platform.html", "w", encoding="utf-8") as file:
    file.write(optimized_html)

print("Optimization Complete!")