(function(){
  const params = new URLSearchParams(window.location.search);
  const query = params.get("q");
  if (query) {
    window.open("https://duckduckgo.com/?q=" + encodeURIComponent(query), "_blank");
  } else {
    alert("No search query found.");
  }
})();

