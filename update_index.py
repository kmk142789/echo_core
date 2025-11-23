import os

html_content = ""
with open("index.html", "r") as f:
    html_content = f.read()

if "AETERNA EXPLORER" not in html_content:
    # Insert link in the footer area or tabs
    link = '<a href="explorer.html" style="display:block; margin-top:20px; color:#D4AF37; text-align:center; border:1px solid #D4AF37; padding:10px;">VIEW LIVE BLOCK EXPLORER</a>'
    # Simple string insertion before footer
    html_content = html_content.replace("<footer>", link + "\n        <footer>")
    
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Main Portal linked to Explorer.")
