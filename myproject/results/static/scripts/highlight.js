var trace = document.querySelector("card")

trace.addEventListener("mouseover", highlightTrace)

function highlightTrace(event){
    console.log(event.target);
}
