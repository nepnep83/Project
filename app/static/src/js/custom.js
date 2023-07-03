function showMore(num) {
    var text = document.getElementById("txt"+ num)
    var button = document.getElementById("more"+ num)
    var dots = document.getElementById("dots"+ num)

    if (dots.style.display === "none") {
        button.innerHTML = "&ltshow more>";
        text.style.display = "none";
        dots.style.display = "inline";
    } else {
        button.innerHTML = "&ltshow less>";
        text.style.display = "inline";
        dots.style.display = "none";
    }
}
for (let i = 1; i < 9; i++){
    if (document.getElementById("more" + i)){
        document.getElementById("more" + i).addEventListener("click", ()=>{showMore(i)})
    }
    else{
        break
    }
}
