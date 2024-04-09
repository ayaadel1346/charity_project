//caresolpage

document.addEventListener('DOMContentLoaded', function() {
    var myCarousel = document.querySelector('#carouselExampleCaptions');
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval:4000, 
        pause: "hover" 
    });

   
    function showCaptions() {
        var headers = document.querySelectorAll('.slideHeader');
        var paragraphs = document.querySelectorAll('.slideParagraph');
        var captions = document.querySelectorAll('.slideCaption');
        headers.forEach(function(header) {
            header.style.opacity = "1";
        });

        paragraphs.forEach(function(paragraph) {
            paragraph.style.opacity = "1";
        });

        captions.forEach(function(caption) {
            caption.style.opacity = "1";
        });
    }

   
    showCaptions();

    
    myCarousel.addEventListener('slide.bs.carousel', function () {
        var headers = document.querySelectorAll('.slideHeader');
        var paragraphs = document.querySelectorAll('.slideParagraph');
        var captions = document.querySelectorAll('.slideCaption');

        headers.forEach(function(header) {
            header.style.opacity = "0";
        });

        paragraphs.forEach(function(paragraph) {
            paragraph.style.opacity = "0";
        });

        captions.forEach(function(caption) {
            caption.style.opacity = "0";
        });

        setTimeout(function(){
            headers.forEach(function(header) {
                header.style.opacity = "1";
            });

            paragraphs.forEach(function(paragraph) {
                paragraph.style.opacity = "1";
            });

            captions.forEach(function(caption) {
                caption.style.opacity = "1";
            });
        },1000);
    });
});








//progress bar
document.addEventListener('DOMContentLoaded', function() {
    var loaders = document.querySelectorAll('.loader-progress');

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting && !entry.target.dataset.animated) {
                var progress = parseFloat(entry.target.dataset.progress);
                if (progress > 0) {
                    entry.target.innerHTML = '0%'; 
                    animateProgressBar(entry.target, progress);
                    entry.target.dataset.animated = true;
                } else {
                    entry.target.style.width = '0%';
                }
            }
        });
    }, { threshold: 0.5 }); 

    loaders.forEach(function(loader) {
        observer.observe(loader);
    });
});

function animateProgressBar(loader, progress) {
    var counter = 0;
    var increment = 1;
    var width = 0; 
    var timer = setInterval(function() {
        width += increment;
        loader.style.width = width + '%';
        counter++;
        loader.innerHTML = counter + '%';
        if (counter >= progress) {
            clearInterval(timer);
        }
    }, 30); 
}








