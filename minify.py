from bs4 import BeautifulSoup
import requests
import cssmin
from jsmin import jsmin
import htmlmin


destination = "dist/index.html"
base_file = "index.html"


main_html = open(base_file,"r").read()
soup = BeautifulSoup(main_html,"lxml")

css_imports = []
scripts_import = []

for css in soup.find_all('link'):
    href = (css.get("href"))
    if "http://" in href or "https://" in href:
        r = requests.get(href)
        content = r.text


    else:
        content = open(href,"r").read()
    content = cssmin.cssmin(content)
    print("PROCEED : "+href)
    new_style = BeautifulSoup("<style>%s</style>" % content,"lxml")
    css.replace_with(new_style)

for script in soup.find_all("script"):
    source = script.get("src")
    if source != None:
        if "http://" in source or "https://" in source:
            r = requests.get(source)
            content = r.text
        else:
             content = open(source,"r").read()
        content = jsmin(content)
        print("PROCEED : "+source)
        new_script = BeautifulSoup("<script>%s</script>" % content,"lxml")
        script.replace_with(new_script)

with open(destination, "w") as file:
    print("Minifying....")
    result = htmlmin.minify(str(soup))
    file.write(result)
    print("Done")


