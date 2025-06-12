# Google to DuckDuckGo Bookmarklet

This is a simple bookmarklet that improves your web search experience.  
Click it while on a **Google search results page**, and it will automatically open the same query in **DuckDuckGo**.

---

## How It Works

It extracts the current search query from the Google URL, then opens a new tab with that same query in DuckDuckGo.

---

## Installation

1. Create a new bookmark in your browser
2. Set the name to something like `Try DuckDuckGo`
3. Paste the following code into the URL field:

```javascript
javascript:(function(){
  const params = new URLSearchParams(window.location.search);
  const query = params.get("q");
  if (query) {
    window.open("https://duckduckgo.com/?q=" + encodeURIComponent(query), "_blank");
  } else {
    alert("No search query found.");
  }
})();

