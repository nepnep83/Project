function showMore() {
    var text = document.getElementById("txt")
    var button = document.getElementById("more")

    if (button.innerHTML.indexOf("&ltshow more>") !== -1) {
        button.innerHTML = "&ltshow less>";
        text.style.display = "inline";
    } else {
        button.innerHTML = "&ltshow more>";
        text.style.display = "none";
    }
}
document.getElementById("more").addEventListener("click", showMore)
