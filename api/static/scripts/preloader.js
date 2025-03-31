function preloaderAnim(task){
    let tl = gsap.timeline({
        paused: true,
        defaults: {
            ease: 'none',
            duration: 1,
        },
    });
    tl.fromTo(['#preloader','.loader'],{
        opacity: 1,
        display: 'grid',
    },{
        opacity: 0,
        display: 'none',
        duration: 0.5,
    });
    if (task=='page_out') {
        tl.reverse()
    } else {
        tl.resume()
    }
}