var divs = document.getElementsByClassName('error-HEAD');

var mainDiv = document.getElementById('trace-view')

for (var i = 0; i < divs.length; i++) {
    divs[i].addEventListener('mouseover', function () {
        mainDiv.style.backgroundColor = window.getComputedStyle(this).backgroundColor;
    });
    divs[i].addEventListener('mouseleave', function () {
        mainDiv.style.backgroundColor = 'white';
    });
}
