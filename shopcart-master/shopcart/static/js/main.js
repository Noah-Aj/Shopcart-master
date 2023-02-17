var searching = $(".search-list").attr("data-url")

var searchTags = [

];
$.ajax({
    method: "GET",
    url: searching,
    success: function(response){
        startAutoSearch(response);
    }
});
function startAutoSearch(searchTags){
    $("#search-me").autocomplete({
        source: searchTags
    });
};

// Preloader //
const loader = document.getElementById("loader");

window.addEventListener("load", function(){
    loader.style.display = "none";
    const fadeOutEffect = setInterval(() => {
        if (!loader.style.opacity){
            loader.style.opacity = 1;
        }
        if (loader.style.opacity > 0){
            loader.style.opacity -= 0.1;
        }else {
            clearInterval(fadeOutEffect);
        }
    }, 100);
    
});

$(function (){
    setTimeout(function () {
        $(loader).fadeToggle();
    }, 10);
    loader.style.display = "block";
});


// scroll to top //
var  scrollBtn = document.querySelector(".scroll-top");

// When the user scrolls down 5px from the top of the document, show the button
window.onscroll = function() {
    scrollFunction()
};

function scrollFunction() {
    if (document.body.scrollTop > 5 || document.documentElement.scrollTop > 5) {
      scrollBtn.style.display = "block";
    } else {
      scrollBtn.style.display = "none";
    }
  }
  
  // When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
  }

