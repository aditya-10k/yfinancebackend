// Navigation function
function navigate(path) {
    window.location.href = path;
}

// Google Search functionality
document.getElementById("search-bar").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        const query = this.value.trim();
        if (query) {
            const searchUrl = "https://yfinancebackend.onrender.com/api/stock/search/" + encodeURIComponent(query);
            window.location.href = searchUrl;
        }
    }
});
