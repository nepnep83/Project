function showMore(num) {
    var text = document.getElementById("txt"+ num)
    var button = document.getElementById("more"+ num)
    var dots = document.getElementById("dots"+ num)

    if (dots.style && dots.style.display === "none") {
        button.innerHTML = "&ltshow more>";
        text.style.display = "none";
        dots.style.display = "inline";
    } else {
        button.innerHTML = "&ltshow less>";
        text.style.display = "inline";
        dots.style.display = "none";
    }
}

function prefShowMore(num) {
    var prefText = document.getElementById("pref_txt"+ num)
    var prefButton = document.getElementById("pref_more"+ num)
    var prefDots = document.getElementById("pref_dots"+ num)

    if (prefDots.style && prefDots.style.display === "none") {
        prefButton.innerHTML = "&ltshow more>";
        prefText.style.display = "none";
        prefDots.style.display = "inline";
    } else {
        prefButton.innerHTML = "&ltshow less>";
        prefText.style.display = "inline";
        prefDots.style.display = "none";
    }
}

for (let i = 1; i < 6; i++){
    if (document.getElementById("more" + i)){
        document.getElementById("more" + i).addEventListener("click", ()=>{showMore(i)})
    }
    if (document.getElementById("pref_more" + i)){
        document.getElementById("pref_more" + i).addEventListener("click", ()=>{prefShowMore(i)})
    }
}
