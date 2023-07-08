window.addEventListener('load', function () {
    new Glider(document.querySelector('.glider'), {
        slidesToScroll: 1,
        slidesToShow: 3,
        dots: '.dots',
        arrows: {
            prev: '.glider-prev',
            next: '.glider-next'
        }
    })
})