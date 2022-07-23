const activePage = location.href;
console.log(activePage);
const navLinks = document.querySelectorAll('a').
forEach(link => {
    if (link.href.includes('${activePage}')) {
        link.classList.add('active');
    }
})